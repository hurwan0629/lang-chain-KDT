import { MongoClient } from "mongodb"

import { config } from "../config.mjs"

let db;

// 데이터베이스 클라이언트 호출
export default async function connectDB() {
  await MongoClient.connect(config.db.host).then((client) => {
    db = client.db(config.db.databaseName);
  });
}

export function getUser() {
  return db.collection("users")
}

export function getOrders() {
  return db.collection("orders")
}

export function getItems() {
  return db.collection("items")
}