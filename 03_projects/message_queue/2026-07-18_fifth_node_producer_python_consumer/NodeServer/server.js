import express from "express"
import { fileURLToPath } from "url"
import { dirname } from "path"

const app = express()

app.use("/", express.static(dirname(fileURLToPath(import.meta.url)) + "/public"))
app.use(express.json())

app.post("/order", (req, res) => {
  const { userId, totalPrice, orderList } = req?.body

  // 결제 정보에 대해서
  // 1. 결제 확인 [producer에서 작업 등록하기]
  // 2. 재고 차감
  // 3. 배송 요청

})

app.listen(8092, "127.0.0.1", () => {
  console.log("express 서버 구동... 127.0.0.1:8092")
})