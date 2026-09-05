import amqp from "amqplib"
import crypto from "node:crypto"

const userName = 
  process.argv[2] ?? "undefined_user"

const connection = await amqp.connect(
  "amqp://app:apppass@localhost:5672"
)

const channel = await connection.createConfirmChannel()

// 기존에 만들어둔 hurwan.network.authentication에 작업 등록하기
const canContinue = channel.publish(
  "hurwan.network.jobs",
  "hurwan.network.authentication.check-user",
  Buffer.from(
    JSON.stringify({
      messageId: crypto.randomUUID(),
      routingKey: "hurwan.network.authentication.check-user",
      createdAt: new Date().toISOString()
    })
  ),
  {
    persistent: true,
    contentType: "application/json",
    mandatory: true
  }
)

if(!canContinue) {
  await once(channel, "drain")
}

const confirmsResult = await channel.waitForConfirms()

console.log("confirmResult:", confirmsResult)

console.log("작업 발행 완료", {
  exchange:  "hurwan.network.jobs",
  routingKey: "hurwan.network.authentication.check-user",
  content: {
    messageId: crypto.randomUUID(),
    routingKey: "hurwan.network.authentication.check-user",
    createdAt: new Date().toISOString()
  }
})

await channel.close()
await connection.close()