// 여러 작업 (audit, video, thumbnail) 이벤트 메시지를 생산할 producer 스크립트
import crypto from "node:crypto"
import { once } from "node:events"
import amqp from "amqplib"

import {
  AMQP_URL,
  JOBS_EXCHANGE,
  assertTopology
} from "./topology.js"

// 어떤 작업을 할 것인지는 콘솔의 2번째 (node [producer.js] [라우팅 키 (작업)]) 인자로 알림
const routingKey = 
  process.argv[2] ?? "video.analysis.normal"


// 작업 시간은 설정 또는 2초로 설정하기 (가상의 작업)
const durationMs = 
  Number(process.argv[3] ?? 2000)

const mode = 
  process.argv[4] ?? "success"

const validModes = new Set([
  "success",
  "retry-once",
  "dead",
  "crash-once"
])

if (!Number.isFinite(durationMs) || durationMs < 0) {
  throw new Error("durationMs는 0 이상의 숫자여야 합니다.")
}

if (!validModes.has(mode)) {
  throw new Error(
    `mode는 다음 중 하나여야 합니다: ${[...validModes].join(", ")}`
  )
}

// 연결 작업 시작하기
const connection = await amqp.connect(AMQP_URL)
const channel = await connection.createConfirmChannel()

connection.on("error", (error) => {
  console.error("[Producer] Connection 오류:", error)
})

channel.on("error", (error) => {
  console.error("[Producer] Channel 오류:", error)
})

// mandatory:true 인데 어떤 Queue에도 라우팅되지 않으면 발생하는 이벤트
channel.on("return", (message) => {
  console.error("[Producer] 라우팅 실패:", {
    routingKey: message.fields.routingKey,
    body: message.content.toString()
  })
})

await assertTopology(channel);

const job = {
  id: crypto.randomUUID(),
  type: routingKey,
  durationMs,
  mode,
  createdAt: new Date().toISOString()
}

const content = Buffer.from(JSON.stringify(job))

// publish하는 경우, 성공/실패  -> false의 경우에는 버퍼가 가득 차서 `drain` 이벤트를 기다리는 상태가 됨
const canContinue = channel.publish(
  JOBS_EXCHANGE,
  routingKey,
  content,
  {
    persistent: true,
    mandatory: true,
    contentType: "application/json",
    messageId: job.id,
    type: job.type
  },
)

// Node.js의 Channel 쓰기 버퍼가 가득 찼을 때만 기다린다
if (!canContinue) {
  // channel.on("drain") 을 한번 기다린다 -> 다시 넣기
  await once(channel, "drain")
}

// RabbitMQ가 발행한 메시지를 확인할 대까지 대기한다.
await channel.waitForConfirms();

console.log("[Producer] 발행 확인:", {
  exchange: JOBS_EXCHANGE,
  routingKey,
  job
})

await new Promise((resolve) => setTimeout(resolve, 100))

await channel.close()
await connection.close()