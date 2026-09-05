import amqp from "amqplib"

const AMQP_URL = 
  process.env.AMQP_URL ?? "amqp://app:apppass@localhost:5672"

const QUEUE_NANE = "video-jobs"
const WORKER_ID = process.env.WORKER_ID ?? "worker-1"

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms))
}

const connection = await amqp.connect(AMQP_URL)
const channel = await connection.createChannel()

await channel.assertQueue(QUEUE_NANE, {
  durable: true
})

// 완료하지 않은 작업을 한번에 하나만 받게 제한
await channel.prefetch(1)

console.log(`[${WORKER_ID}] 작업 대기중...`)

await channel.consume(
  QUEUE_NANE,
  async (message) => {
    if (message === null) {
      return
    }

    let job

    try {
      //[2026-07-17 18:54:55] 현재 producer.js의 경우에는
      // { id, type, durationMs, createdAt } 를 보내고 있음
      job = JSON.parse(message.content.toString())

    } catch (error) {
      console.error(`[${WORKER_ID}] 잘못된 메시지 형식`, error)

      channel.nack(message, false, false)
      return 
    }

    console.log(`[${WORKER_ID}] 작업 시작`, {
      jobId: job.id,
      durationMs: job.durationMs,
      redelivered: message.fields.redelivered // 아마 실패 후 다시 들어온거를 나타내는 boolean 값인가?

      // message(콜백 1번인자)에는 content(Buffer)과  fields(여러 속성을 가진 일반객체)가 있는 듯 함
    })

    try {
      // 실제로는 여기에서 작업을 하겠지만 그냥 쉬라는 시간만큼 일하는척 하고
      // 작업 완료 취급해주기
      await sleep(job.durationMs)

      console.log(`[${WORKER_ID}] 작업 완료: ${job.id}`)

      // 여기까지 제대로 성공 하였을 때에만 ack 보내주기
      channel.ack(message)
    } catch (error) {
      console.error(`[${WORKER_ID}] 작업 실패: ${job.id}`, error)

      channel.nack(message, false, false)
    }
  },
  {
    noAck: false
  }
)