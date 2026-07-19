// hurwan.network.authentication.q 작업 큐 처리 워커

import amqp from "amqplib"

const connection = await amqp.connect(
  "amqp://app:apppass@localhost:5672"
)

const channel = await connection.createChannel()

channel.consume(
  "hurwan.network.authentication.q",
  async (message) => {
    console.log("[network authentication] message recieved")
    const job = JSON.parse(message.content.toString())
    console.log(job)
    console.log(`[${message.fields.routingKey}] [job-${job.messageId}] working started`)
    await setTimeout(() => {
      console.log(`[${message.fields.routingKey}] [job-${job.messageId}] working ended`)
    }, 3000)
    console.log("[network authentication] end")
    channel.ack(message, false)
  },
  {
    noAck: false
  }
)


const dlqChannel = await connection.createChannel()

dlqChannel.consume(
  "hurwan.network.dlq",
  async (message) => {
    console.log("[dead queue] dlq message recieved")
    const job = JSON.parse(message.content.toString())
    console.log(job)
    console.log(`[${message.fields.routingKey}] [job-${job.messageId}] working started`)
    await new Promise((resolve) => setTimeout(resolve, 2000))
    console.log(`[${message.fields.routingKey}] [job-${job.messageId}] working end`)
    dlqChannel.ack(message, false)
    console.log("[dead queue] end")
  },
  {
    noAck: false
  }
)