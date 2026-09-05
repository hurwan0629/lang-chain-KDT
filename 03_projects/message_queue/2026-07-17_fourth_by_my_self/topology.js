// topology.js
// Exchange와 queue, binding-key, routing-key를 정의하기 위한 공간이다.

import amqp from "amqplib"

const connection = await amqp.connect(
  "amqp://app:apppass@localhost:5672"
)

const channel = await connection.createChannel()

const exchangeOptions = {
  durable: true,
  autoDelete: false,
  internal: false,
  // alternateExchange: "unrouted.x",
}

const queueOptions = {
  durable: true,
  exclusive: false,
  autoDelete: false,
  arguments: {
    "x-max-length": 10000,
    "x-max-length-bytes": 100 * 1024 * 1024, // 100GB
    "x-overflow": "reject-publish",
    "x-message-ttl": 30_000,
    "x-dead-letter-exchange": "hurwan.network.dlx",
    "x-dead-letter-routing-key": "hurwan.network.dead"
  }
}
// // // // // // // // // //  [네트워크 인증 큐 생성]  // // // // // // // // 

await channel.assertExchange(
  "hurwan.network.jobs",
  "topic", // "direct", "fanout"말고 binding-key.* 형태
  exchangeOptions
)

await channel.assertQueue(
  "hurwan.network.authentication.q",
  queueOptions
)

// 네트워크 인증 요청을 받아서 처리해주는 큐에 대한 바인딩
await channel.bindQueue(
  "hurwan.network.authentication.q", // queueName
  "hurwan.network.jobs", // exchange
  "hurwan.network.authentication.*"
)


// // // // // // // // // //  [오류 처리 exchange와 큐 생성] // // // // // // // // // // 
await channel.assertExchange(
  "hurwan.network.dlx",
  "direct",
  {
    durable: true,
    autoDelete: false,
    internal: false,
  }
)

await channel.assertQueue(
  "hurwan.network.dlq",
  {
    durable: true,
    exclusive: false,
    autoDelete: false
  }
)

await channel.bindQueue(
  "hurwan.network.dlq",
  "hurwan.network.dlx",
  "hurwan.network.dead" // hurwan.network.dead 라는 키로 hurwan.network.dlx에 넣으면 자동으로 hurwan.network.dlq로 가게 됨.
)

await channel.close()
await connection.close()