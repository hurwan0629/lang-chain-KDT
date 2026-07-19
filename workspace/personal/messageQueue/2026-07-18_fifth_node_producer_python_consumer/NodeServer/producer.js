// 존재하는 queue 3개에 대해서 가져와서 쓰기

import amqp from "amqplib"
import crypto from "node:crypto"

const connection = await amqp.connect(
  "amqp://app:apppass@localhost:5672"
)

const producer = await connection.createConfirmChannel()

export async function producerPaymentMessage(orderList) {
  producer.publish(
    "hurwan.orders.jobs",
    "hurwan.orders.payment.default",
    Buffer.from(
      JSON.stringify({
        id: crypto.randomUUID(),
        userId,
        totalPrice,
        orderList, // [{item_id, item_price, item_amount}, ...]
        createdAt: new Date().toISOString()
      })
    ),
    {
      persistent: true,
      contentType: "application/json",
      headers: {
        retryCount: 0
      }
    }
  )
}