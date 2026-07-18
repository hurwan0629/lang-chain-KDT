import crypto from "node:crypto"
import amqp from "amqplib"

const AMQP_URL = // amqp에서 통신하기 위해서 사용하는 url (저는 로컬호스트 docker 사용 - image: rabbitmq:4-management)
  process.env.AMQP_URL ?? "amqp://app:apppass@localhost:5672"

const QUEUE_NAME = "video-jobs"

// 
const durationMs = Number(process.argv[2] ?? 3000)

if (!Number.isFinite(durationMs) || durationMs < 0) {
  throw new Error("작업 시간은 0 이상의 숫자여야 합니다.")
}

// 아마 연결을 잡아놓고 계속 보내는 방식일 듯? tcp:5672
const connection = await amqp.connect(AMQP_URL)

// RabbitMQ가 메시지를 받았는지 확인할 수 있는 Confirm Channel이라고 함.
const channel = await connection.createConfirmChannel()

// 해당 큐의 이름이 존재하면 그대로 두고 없으면 생성하라는 의미. durable=지속 가능성
// durable -> RabbitMQ 서버가 재시작되어도 큐 자체를 유지하겠다는 뜻
await channel.assertQueue(QUEUE_NAME, {
  durable: true
})

const job = {
  id: crypto.randomUUID(),
  type: "video-analysis",
  durationMs,
  createdAt: new Date().toISOString()
}

channel.sendToQueue(
  QUEUE_NAME,
  Buffer.from(JSON.stringify(job)),
  {
    persistent: true,
    contentType: "application/json"
  }
)

await channel.waitForConfirms()

console.log("[Producer] 작업 등록:", job)

await channel.close()
await connection.close()