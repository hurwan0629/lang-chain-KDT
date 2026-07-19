import amqp from "amqplib"

import {
  AMQP_URL,
  QUEUES,
  assertTopology
} from "./topology.js"

const role = process.argv[2] ?? "analysis"

if (!(role in QUEUES)) {
  throw new Error(
    `Worker 역할은 다음 중 하나여야 합니다: ${Object.keys(QUEUES).join(", ")}`
  )
}

const queueName = QUEUES[role] // role에 대한 큐 이름을 받아오기 (consume 하기 위해)

const workerId = 
  process.env.WORKER_ID ??
  `${role}-${process.pid}`

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const connection = await amqp.connect(AMQP_URL)
const channel = await connection.createChannel()

connection.on("error", (error) => {
  console.error(`[${workerId}] Connection 오류:`, error)
})

channel.on("error", (error) => {
  console.error(`[${workerId}] Channel 오류:`, error)
})

await assertTopology(channel)

// 해당 Channel이 ACK하지 않은 메시지를 최대 한개만 가지게 된다.
await channel.prefetch(1);

console.log(`[${workerId}] 대기 시작`, {
  role,
  queueName
})

// 자신의 역할에 맞는 이름의 큐만을 바라보게 된다.
await channel.consume(
  queueName,
  async (message) => {
    if (message === null) {
      console.log(`[${workerId}] Consumer가 취소되었습니다.`)
      return
    }

    let job;

    try {
      if( message.properties.contentType !== "application/json" ) {
        throw new Error(`지원하지 않는 contentType: ${message.properties.contentType}`)
      }

      job = JSON.parse(message.content.toString())
    } catch (error) {
      console.error(`[${workerId}] 메시지 해석 실패`, error)

      // 재시도하지 않고 Dead Letter로 보낸다.
      channel.nack(message, false, false)
      return 
    }

    const deliverInfo = {
      jobId: job.id,
      type: job.type,
      mode: job.mode,
      routingKey: message.fields.routingKey,
      redelivered: message.fields.redelivered,
      deliveryTag: message.fields.deliveryTag
    }

    console.log(`[${workerId}] 메시지 수신`, deliverInfo)

    /**
     * audit Worker은 작업을 수행하지 않고
     * 모든 video 이벤트를 기록만 한다. 
     * video.#
     */
    // audit의 경우에는 모든 작업이 lab.media.jobs -> lab.video.audit.q
    // 와 같이 들어오기 때문에 이에 대해서 작업을 하게 설정할 수 있습니다.
    if (role === "audit") {
      console.log(`[${workerId}] 감사 로그 기록`, {
        jobId: job.id,
        type: job.type
      })

      channel.ack(message)
      return 
    }

    /**
     * dead Worker은 최종 실패 메시지를 확인한다
     */
    if (role === "dead") {
      console.error(`[${workerId}] Dead Letter 수신`, {
        job,
        originalRoutingKey: message.fields.routingKey,
        deadInfo: message.properties.headers?.["x-death"]
      })

      channel.ack(message)
      return
    }

    // lab.video.analysis.q(video.analysis.*) 또는 lab.video.thumbnail.q(video.thumbnail.*)
    // 의 큐에 대해서는 아래와 같은 작업을 한다.
    try {
      if(
        job.mode === "retry-once" &&
        !message.fields.redelivered
      ) {
        // 작업이 최소로 왔는데 job.mode가 retry-once가 가능하면 그냥 테스트처럼 한번 되돌려보기
        console.warn(
          `[${workerId}] 첫 번째 자리를 고의로 실패시킵니다.`
        )

        // 현재 메시지만 다시 Queue에 넣기
        channel.nack(message, false, true)
        return
      }

      if (job.mode === "dead") {
        console.warn(
          `[${workerId}] 재시도 없이 Dead Letter로 보냅니다.`
        )

        // requeue:false이기 때문에 DLS가 설정된 Queue라면 DLX로 보내기
        channel.nack(message, false, false)
        return
      }

      if (
        job.mode === "crash-once" &&
        !message.fields.redelivered
      ) {
        console.error(
          `[${workerId}] ACK 전에 프로세스를 종료합니다.`
        )

        /**
         * ACK하지 않은 상태에서 Connection이 끊기면
         * RabbitMQ가 메시지를 다시 Queue에 넣는다.
         */
        setTimeout(() => {
          process.exit(1)
        }, 100)

        return
      }

      console.log(`[${workerId}] 작업 시작`, {
        jobId: job.id,
        durationMs: job.durationMs
      })

      await sleep(job.durationMs)

      console.log(`[${workerId}] 작업 성공`, {
        jobId: job.id
      })

      channel.ack(message)
    } catch (error) {
      console.error(`[${workerId}] 작업 중 예외`, error)

      channel.nack(message, false, false)
    }
  },
  {
    noAck: false
  }
)