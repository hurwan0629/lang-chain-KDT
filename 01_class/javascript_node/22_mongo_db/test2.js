require("dotenv").config()
const { MongoClient } = require("mongodb");

const uri = process.env.MONGO_URI;
const dbName = process.env.DB_NAME;

const client = new MongoClient(uri);
let db;
let customers;
let orders;


async function initDB() {
  await client.connect(dbName)
  db = client.db(dbName)
  console.log("[MongoDB] Database Connected")

  customers = db.collection("customers")
  orders = db.collection("orders")
}

async function main() {
  await initDB()
  await deleteDatas()
  await insertSampleDatas()
  console.log("[MongoDB] Data init completed")
  await testFunc()
}

module.exports = main


async function testFunc() {
  // console.log(await customers.find({ age : { $gte: 30 }}).sort({ _id: 1 }).toArray())
  // console.log(JSON.stringify(await orders.find({ status: { $in: ["PAID", "REFUNDED"]}}).limit(2).toArray(), null, 2))
  // console.log(await orders.find({ "items.category": "BOOK"}).toArray())

  // console.log(await orders.aggregate([
  //   {
  //     $group: {
  //       _id: ["$status"],
  //       orderCount: { $sum: 1 },
  //       totalSales: { $sum: "$totalAmount" }
  //     }
  //   }
  // ]).toArray())

  // const result = (await orders.aggregate([
  //   {
  //     $unwind: "$items"
  //   }
  // ]).toArray())
  // console.log(result.length)

  // console.log((await orders.aggregate([
  //   {
  //     $group: {
  //       _id: null,
  //       count: { $sum: { $size: "$items" }}
  //     }
  //   }
  // ]).toArray())[0]?.count)

  console.log(JSON.stringify((await orders.aggregate([
    {
      $lookup: {
        from: "customers",
        localField: "customerId",
        foreignField: "_id",
        as: "customer"
      }
    },
    { $unwind: "$customers"}
  ]).toArray()), null, 2))
}





// // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // // 

async function deleteDatas() {
  await customers.deleteMany({})
  await orders.deleteMany({})
}

async function insertSampleDatas() {
  await customers.insertMany([
    {
      _id: "C001",
      name: "김민수",
      city: "서울",
      tier: "VIP",
      age: 29,
      joinedAt: new Date("2024-03-15T00:00:00Z")
    },
    {
      _id: "C002",
      name: "이서연",
      city: "부산",
      tier: "BASIC",
      age: 34,
      joinedAt: new Date("2025-01-10T00:00:00Z")
    },
    {
      _id: "C003",
      name: "박지훈",
      city: "서울",
      tier: "GOLD",
      age: 41,
      joinedAt: new Date("2023-11-02T00:00:00Z")
    },
    {
      _id: "C004",
      name: "최유나",
      city: "대구",
      tier: "BASIC",
      age: 25,
      joinedAt: new Date("2025-06-20T00:00:00Z")
    },
    {
      _id: "C005",
      name: "정하늘",
      city: "인천",
      tier: "VIP",
      age: 37,
      joinedAt: new Date("2022-08-01T00:00:00Z")
    }
  ])

  await orders.insertMany([
    {
      _id: "O1001",
      customerId: "C001",
      status: "PAID",
      totalAmount: 82000,
      orderedAt: new Date("2026-06-01T10:30:00Z"),
      payment: { method: "CARD", approved: true },
      items: [
        { sku: "B001", name: "MongoDB 입문", category: "BOOK", price: 22000, qty: 1 },
        { sku: "K001", name: "키보드", category: "DEVICE", price: 60000, qty: 1 }
      ]
    },
    {
      _id: "O1002",
      customerId: "C002",
      status: "PAID",
      totalAmount: 34000,
      orderedAt: new Date("2026-06-03T14:10:00Z"),
      payment: { method: "KAKAO_PAY", approved: true },
      items: [
        { sku: "B002", name: "JavaScript 핵심", category: "BOOK", price: 34000, qty: 1 }
      ]
    },
    {
      _id: "O1003",
      customerId: "C001",
      status: "CANCELLED",
      totalAmount: 19000,
      orderedAt: new Date("2026-06-05T09:00:00Z"),
      payment: { method: "CARD", approved: false },
      items: [
        { sku: "N001", name: "노트", category: "STATIONERY", price: 5000, qty: 2 },
        { sku: "P001", name: "펜", category: "STATIONERY", price: 3000, qty: 3 }
      ]
    },
    {
      _id: "O1004",
      customerId: "C003",
      status: "PAID",
      totalAmount: 125000,
      orderedAt: new Date("2026-06-07T20:20:00Z"),
      payment: { method: "CARD", approved: true },
      items: [
        { sku: "M001", name: "모니터", category: "DEVICE", price: 125000, qty: 1 }
      ]
    },
    {
      _id: "O1005",
      customerId: "C004",
      status: "REFUNDED",
      totalAmount: 54000,
      orderedAt: new Date("2026-06-09T11:45:00Z"),
      payment: { method: "NAVER_PAY", approved: true },
      items: [
        { sku: "B003", name: "자료구조", category: "BOOK", price: 27000, qty: 2 }
      ]
    },
    {
      _id: "O1006",
      customerId: "C005",
      status: "PAID",
      totalAmount: 178000,
      orderedAt: new Date("2026-06-11T16:00:00Z"),
      payment: { method: "CARD", approved: true },
      items: [
        { sku: "K002", name: "기계식 키보드", category: "DEVICE", price: 98000, qty: 1 },
        { sku: "B001", name: "MongoDB 입문", category: "BOOK", price: 22000, qty: 1 },
        { sku: "P002", name: "마우스패드", category: "DEVICE", price: 29000, qty: 2 }
      ]
    }
  ])
}
