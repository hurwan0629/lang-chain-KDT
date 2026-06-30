// const { MongoClient } = require("mongodb");

// const uri = "";

// async function main() {
//   const client = new MongoClient(uri);

//   try {
//     await client.connect();
//     console.log("연결 성공");
//   } catch (err) {
//     console.error("연결 실패:", err);
//   } finally {
//     await client.close();
//   }
// }

// main();
const dns = require("node:dns");

// MongoDB 연결 전에 먼저 설정
dns.setServers([
  "8.8.8.8",
  "1.1.1.1",
  "127.0.0.1"
]);

console.log(dns.getServers());

const { MongoClient } = require("mongodb");

const uri = "";

async function main() {
  const client = new MongoClient(uri);

  await client.connect();
  console.log("MongoDB connected");

  await client.close();
}

main().catch(console.error);

// const dns = require("node:dns");
// // dns.resolveSrv()
// console.log(dns.getServers())
// // dns.resolveTxt()