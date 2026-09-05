require("dotenv").config();

// mongodb의 exports중 하나인 MongoClient를 받았습니다.
const { MongoClient } = require("mongodb")

// process에서 루트 폴더의 .env를 통해 접속할 주소(저같은 경우엔 Atlas)와 그 서버의 데이터베이스를 설정해주었습니다.
const uri = process.env.MONGO_URI;
const dbName = process.env.DB_NAME;


// Atlas 서버와 동기로 통신해야하기 때문에 async 함수로 생성해주었습니다.
async function main() {
  // 몽고DB 클라이언트를 uri를 통해 연결해주었습니다.
  // 몽고의 경우에는 user, password, server 을 모두 한 uri에 넣은 인자를 주기 때문에 단일 인자를 갖습니다.
  const client = new MongoClient(uri);

  try {
    // 서버 접속
    // await를 통해 서버가 연결 될때까지 대기해줍니다.
    await client.connect()
    console.log("0. 데이터베이스 연결 완료")
    
    // 2. DB / collection 선택
    // 클라이언트의 .db를 통해 데이터베이스를 생성하거나 선택(이미 있다면)할 수 있습니다.
    const db = client.db(dbName);
    // collection메서드를 통해 데이터베이스 안의 문서/컬렉션(RDB로 치면 테이블)을 선택할 수 있습니다.
    const computer_status = db.collection("computer_status");

    // 컬렉션 초기화하기
    // 빈 조건을 주어 모든 값을 삭제해줍니다.
    await computer_status.deleteMany({});
    console.log("1. 기존 연습 데이터 삭제 완료")

    // 몇가지 데이터 넣어보기. (이걸 gpt에서는 여러 문서를 추가한다고 합니다.)
    const insertResult = await computer_status.insertMany([
      {
        computer_id: 1,
        computer_name: "master server",
        cpu: 24,
        ram: 64,
        roles: ["control", "proxy"]
      },
      {
        computer_id: 2,
        computer_name: "slave server",
        cpu: 16,
        ram: 32,
        roles: ["database", "cache"]
      },
      {
        computer_id: 3,
        computer_name: "logic server",
        cpu: 8,
        ram: 16,
        roles: ["WAS"]
      }
    ])

    console.log("데이터 삽입 개수:", insertResult);

    // 데이터 읽어보기
    // find({}) 을 통해 모든 데이터 읽어오기
    const allComputers = await computer_status.find({}).toArray();
    console.log("\n전체 조회");
    console.log(allComputers)
    console.log(typeof(allComputers))

    const manyCPUServers = await computer_status.find({cpu: { $gt: 10 }}).toArray()
    console.log(manyCPUServers)

    // 정렬 및 특정 열만 선택
    const manyCPUServersProj = await computer_status
                    .find({cpu: { $gt: 10 }})
                    .sort({ ram: 1 }) // ram 오름차순
                    .project({computer_id: 1, computer_name: 1, _id: 0 }) // _id는 기본값이 0입니다.
                    .toArray()
    console.log(manyCPUServersProj)

    // 여러 조회 결과중에서 하나만 뽑아보기
    const oneResult = await computer_status.findOne({})
    console.log("console.log(oneResult)")
    console.log(oneResult)

    // 2개 이상의 값들을 수정해주기
    const updateManyResult = await computer_status.updateMany({
       computer_name: { $ne: "slave server" } },
      { // cpu 10개씩 더해주기
        $inc: { cpu: 10 }
      })
    console.log("updateManyResult:", updateManyResult)

    // 현재 상태 보기
    const checkAll = await computer_status.find({}).toArray()
    console.log(checkAll)

    // 몇개의 데이터가 들어있는지 확인해주기
    const computerCount = await computer_status.countDocuments({})
    // 컴퓨터가 3개 있다고 출력됨
    console.log(computerCount + "\n")

    // 인덱싱 걸어주기
    const indexingResult = await computer_status.createIndex({ computer_id: 1 })
    console.log("indexingResult:", indexingResult)
    
    // 복합 인덱싱 걸어주기. (1이 오름차순, -1이 내림차순)
    const indexingResult2 = await computer_status.createIndex({ cpu: 1, ram: -1 })
    console.log("\createIndexResult:", indexingResult2)

    // 집계 메서드 사용해보기 (aggregate)
    const status = await computer_status
                .aggregate([ // 배열을 통해 단계별로 작업을 진행해줄 수 있음
                  {  // cpu가 10개보다 많은지에 따라 그룹으로 나누어주기
                    $group: {
                      _id: "$computer_name",
                      bookCount: { $sum: 1 },
                      avgCpu: { $avg: "$cpu" }
                    }
                  },
                  {
                    $sort: { avgCpu: 1 }
                  }
                ]).toArray()
    console.log("집계 결과:", status)


  } catch (err) {
    console.error("에러가 발생했습니다.", err)
    console.log("에러입니다.")
  } finally {
    // 무슨일이 있어도 클라이언트를 닫아줍니다. (접속을 끊어줍니다.)
    await client.close()
    console.log("\nMongoDB connection closed")
  }
}


async function clearAllDatas(computer_status) {
  const clearResult = await computer_status.deleteMany({})
  console.log("[Database] data cleared:", clearResult)
}

async function doMySelfFunc(collection) {
  const seoulPaidCust = await collection.find({ "customer.city": "서울", status: "PAID" }, {
    projection: {
      "orderNo": 1,
      "customer.name": 1,
      "customer.tier": 1,
      "totalAmount": 1,
      "orderedAt": 1,
    }
  }).sort({ totalAmount: -1}).toArray()
  console.log(seoulPaidCust)

  const overTotalPayment = await collection.find({
    "totalAmount": { $gte: 50000 },
    "status": { $ne: "CANCELLED" }
  }, {
    projection: {
      "orderNo": 1,
      "customer.name": 1,
      "customer.city": 1,
      "status": 1,
      "totalAmount": 1,
      "payment.method": 1,
    }
  }).sort({ orderedAt: -1 }).toArray()
  console.log(overTotalPayment)

  const shipItems = await collection.updateMany(
    { status: "READY" },
    { 
      $set: { status: "SHIPPED"},// shippedAt: new Date() }
      $currentDate: { shippedAt: true}
    }
  )
  console.log(shipItems)
  
  const citySales = await collection.aggregate([
    {
      $group: {
        _id: "$customer.city",
        orderCount: { $sum: 1},
        totalSales: { $sum: "$totalAmount" },
        avgOrderAmount: { $avg: "$totalAmount" },
        maxOrderAmount: { $max: "$totalAmount" },
      }
    }
  ]).toArray();
  console.log(citySales)

  const catSales = await collection.aggregate([
    { $match: { status: { $ne: "CANCELLED" }}},
    { $unwind: "$items" },
    { $group: {
      _id: "$items.category",
      catSalesCount: { $sum: "$items.qty"},
      catSalesAmount: { $sum: { $multiply: ["$items.price", "$items.qty"]}},
      catSalesTime: { $sum: 1}
    }}
  ]).toArray()
  console.log(catSales)
}


async function expFunc() {
  const client = new MongoClient(uri)
  await client.connect()
  console.log("[DataBase] client 연결 완료")
  try {
    const db = client.db(dbName)
    const collection = db.collection("shop")
    await clearAllDatas(collection)
    await putDataFunc(collection)
    await doMySelfFunc(collection)
  }
  catch (err) {
    console.error(err)
    console.log("에러 발생")
  }
  finally {
    await client.close()
    console.log("\nMongoDB connection closed")
  }
  // main()
}

module.exports = expFunc


async function putDataFunc(collection) {
  const orders = [
    {
      orderNo: "ORD-1001",
      customer: { name: "김민준", city: "서울", tier: "GOLD" },
      status: "PAID",
      orderedAt: new Date("2026-06-01"),
      items: [
        { name: "무선 마우스", category: "전자기기", price: 25000, qty: 1 },
        { name: "키보드 커버", category: "액세서리", price: 8000, qty: 2 },
      ],
      payment: { method: "CARD", paid: true },
      deliveryFee: 3000,
      couponUsed: false,
      totalAmount: 44000,
    },
    {
      orderNo: "ORD-1002",
      customer: { name: "이서연", city: "부산", tier: "SILVER" },
      status: "PAID",
      orderedAt: new Date("2026-06-02"),
      items: [
        { name: "텀블러", category: "생활용품", price: 18000, qty: 2 },
        { name: "노트", category: "문구", price: 3000, qty: 3 },
      ],
      payment: { method: "KAKAO_PAY", paid: true },
      deliveryFee: 0,
      couponUsed: true,
      totalAmount: 45000,
    },
    {
      orderNo: "ORD-1003",
      customer: { name: "박지훈", city: "서울", tier: "BRONZE" },
      status: "CANCELLED",
      orderedAt: new Date("2026-06-03"),
      items: [
        { name: "USB-C 케이블", category: "전자기기", price: 12000, qty: 2 },
      ],
      payment: { method: "CARD", paid: false },
      deliveryFee: 3000,
      couponUsed: false,
      totalAmount: 27000,
    },
    {
      orderNo: "ORD-1004",
      customer: { name: "최유나", city: "대구", tier: "GOLD" },
      status: "PAID",
      orderedAt: new Date("2026-06-04"),
      items: [
        { name: "백팩", category: "패션", price: 59000, qty: 1 },
        { name: "파우치", category: "패션", price: 15000, qty: 1 },
      ],
      payment: { method: "CARD", paid: true },
      deliveryFee: 0,
      couponUsed: true,
      totalAmount: 74000,
    },
    {
      orderNo: "ORD-1005",
      customer: { name: "정도윤", city: "인천", tier: "SILVER" },
      status: "READY",
      orderedAt: new Date("2026-06-05"),
      items: [
        { name: "볼펜 세트", category: "문구", price: 7000, qty: 3 },
        { name: "파일 홀더", category: "문구", price: 4000, qty: 5 },
      ],
      payment: { method: "BANK_TRANSFER", paid: true },
      deliveryFee: 3000,
      couponUsed: false,
      totalAmount: 44000,
    },
    {
      orderNo: "ORD-1006",
      customer: { name: "한지아", city: "서울", tier: "VIP" },
      status: "PAID",
      orderedAt: new Date("2026-06-06"),
      items: [
        { name: "기계식 키보드", category: "전자기기", price: 89000, qty: 1 },
        { name: "무선 마우스", category: "전자기기", price: 25000, qty: 1 },
      ],
      payment: { method: "CARD", paid: true },
      deliveryFee: 0,
      couponUsed: false,
      totalAmount: 114000,
    },
    {
      orderNo: "ORD-1007",
      customer: { name: "오하준", city: "광주", tier: "BRONZE" },
      status: "PAID",
      orderedAt: new Date("2026-06-07"),
      items: [
        { name: "샴푸", category: "생활용품", price: 13000, qty: 2 },
        { name: "수건", category: "생활용품", price: 9000, qty: 4 },
      ],
      payment: { method: "KAKAO_PAY", paid: true },
      deliveryFee: 3000,
      couponUsed: true,
      totalAmount: 65000,
    },
    {
      orderNo: "ORD-1008",
      customer: { name: "서지우", city: "부산", tier: "GOLD" },
      status: "SHIPPED",
      orderedAt: new Date("2026-06-08"),
      items: [
        { name: "후드티", category: "패션", price: 39000, qty: 2 },
      ],
      payment: { method: "CARD", paid: true },
      deliveryFee: 0,
      couponUsed: false,
      totalAmount: 78000,
    },
    {
      orderNo: "ORD-1009",
      customer: { name: "강민서", city: "서울", tier: "SILVER" },
      status: "PAID",
      orderedAt: new Date("2026-06-09"),
      items: [
        { name: "스티커팩", category: "문구", price: 5000, qty: 4 },
        { name: "노트", category: "문구", price: 3000, qty: 5 },
      ],
      payment: { method: "NAVER_PAY", paid: true },
      deliveryFee: 3000,
      couponUsed: false,
      totalAmount: 38000,
    },
    {
      orderNo: "ORD-1010",
      customer: { name: "윤태오", city: "대전", tier: "VIP" },
      status: "PAID",
      orderedAt: new Date("2026-06-10"),
      items: [
        { name: "모니터 받침대", category: "전자기기", price: 32000, qty: 1 },
        { name: "USB-C 케이블", category: "전자기기", price: 12000, qty: 3 },
      ],
      payment: { method: "CARD", paid: true },
      deliveryFee: 0,
      couponUsed: true,
      totalAmount: 68000,
    },
    {
      orderNo: "ORD-1011",
      customer: { name: "장예린", city: "서울", tier: "GOLD" },
      status: "READY",
      orderedAt: new Date("2026-06-11"),
      items: [
        { name: "에코백", category: "패션", price: 22000, qty: 2 },
        { name: "파우치", category: "패션", price: 15000, qty: 2 },
      ],
      payment: { method: "BANK_TRANSFER", paid: true },
      deliveryFee: 3000,
      couponUsed: false,
      totalAmount: 77000,
    },
    {
      orderNo: "ORD-1012",
      customer: { name: "임현우", city: "인천", tier: "BRONZE" },
      status: "CANCELLED",
      orderedAt: new Date("2026-06-12"),
      items: [
        { name: "텀블러", category: "생활용품", price: 18000, qty: 1 },
      ],
      payment: { method: "CARD", paid: false },
      deliveryFee: 3000,
      couponUsed: false,
      totalAmount: 21000,
    },
  ];
  await collection.insertMany(orders)
}