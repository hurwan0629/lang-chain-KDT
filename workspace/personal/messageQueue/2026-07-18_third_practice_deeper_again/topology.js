// Exchange, Queue, Binding 구조를 한곳에 정의하는 공간

export const AMQP_URL = 
  process.env.AMQP_URL ?? "amqp://app:apppass@localhost:5672"

// 
export const JOBS_EXCHANGE = "lab.media.jobs"
export const DEAD_EXCHANGE = "lab.media.dlx"

export const QUEUES = {
  analysis: "lab.video.analysis.q",
  thumbnail: "lab.video.thumbnail.q",
  audit: "lab.video.audit.q",
  dead: "lab.video.dead.q"
}

export const DEAD_ROUTING_KEY = "dead.video"

// 채널을 이용해서 Exchange + Queue + binding_key 설정해주기
export async function assertTopology(channel) {
  // Producer가 작업을 발행하는 Topic Exchange
  await channel.assertExchange(JOBS_EXCHANGE, "topic", {
    durable: true
  })

  // 실패한 메시지를 받는 Dead Letter Exchange
  await channel.assertExchange(DEAD_EXCHANGE, "direct", {
    durable: true
  })

  const jobQueueOptions = {
    durable: true,
    arguments: {
      "x-dead-letter-exchange": DEAD_EXCHANGE,
      "x-dead-letter-routing-key": DEAD_ROUTING_KEY
    }
  }

  await channel.assertQueue(QUEUES.analysis, jobQueueOptions)
  await channel.assertQueue(QUEUES.thumbnail, jobQueueOptions)
  await channel.assertQueue(QUEUES.audit, jobQueueOptions)

  // 최종 실패 메시지가 들어오는 큐
  await channel.assertQueue(QUEUES.dead, {
    durable: true
  })

  /**
   * Topic Exchange Binding
   * 
   * *: 정확히 한 단어
   * #: 0개 이상의 단어
   */

  await channel.bindQueue(
    QUEUES.analysis, // 해당 큐를
    JOBS_EXCHANGE,   // 해당 exchange에서
    "video.analysis.*" // 라는 키로(들어올 때 넣어주는 규칙으로)써 관리하겠다.
  )

  await channel.bindQueue(
    QUEUES.thumbnail,
    JOBS_EXCHANGE,
    "video.thumbnail.*"
  )

  await channel.bindQueue(
    QUEUES.audit,
    JOBS_EXCHANGE,
    "video.#"
  )

  // Dead letter Exchange는 direct이므로 정확하게 일치해야함
  await channel.bindQueue(
    QUEUES.dead,
    DEAD_EXCHANGE,
    DEAD_ROUTING_KEY
  )
}

