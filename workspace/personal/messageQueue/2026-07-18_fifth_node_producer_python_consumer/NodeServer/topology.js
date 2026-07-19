import amqp from "amqplib"

const connection = await amqp.connect(
  "amqp://app:apppass@localhost:5672"
)

const channel = await connection.createConfirmChannel()

const BINDING = {
  "hruwan.orders.jobs": {
    payment: "hurwan.orders.payment.q",
    inventory: "hurwan.orders.inventory.q",
    delivery: "hurwan.orders.delivery.q"
  },
  "hurwan.orders.dlx": {
    dlq: "hurwan.orders.dlq"
  }
}

for(const exchange_name of Object.keys(BINDING)) {
  await channel.assertExchange(
    exchange_name,
    "topic",
    {
      durable: true
    }
  )
  console.log(`[exchange created] ${exchange_name}`)
}

for(const exchange_name of Object.keys(BINDING)) {
  for(const queue_name of Object.values(BINDING[exchange_name])) {
    await channel.assertQueue(
      queue_name,
      {
        durable: true
      }
    )

    const queue_arr = String(queue_name).split(".")
    if(!queue_arr[queue_arr.length-1] === "dlq") {
      queue_arr[queue_arr.length-1] = "*"
    }

    await channel.bindQueue(
      queue_name,
      exchange_name,
      queue_arr.join(".")
    )
    console.log(`${exchange_name}: ${queue_name} / ${queue_arr.join(".")}`)
  }
}

// await channel.assertExchange(
//   "hurwan.orders.jobs",
//   "topic",
//   {
//     durable: true
//   }
// )

// await channel.assertExchange(
//   "hurwan.orders.dlx",
//   "direct",
//   {
//     durable: true
//   }
// )

// await channel.assertQueue(
//   BINDING["hurwan.orders.jobs"].payment,
//   {
//     durable: true
//   }
// )

// await channel.assertQueue(
//   BINDING["hurwan.orders.jobs"].inventory,
//   {
//     durable: true
//   }
// )

// await channel.assertQueue(
//   BINDING["hurwan.orders.jobs"].delivery,
//   {
//     durable: true
//   }
// )

// await channel.assertQueue(
//   BINDING["hurwan.orders.dlx"].dlq,
//   {
//     durable: true
//   }
// )

// await channel.bindQueue(
//   "hurwan.orders.jobs"
// )