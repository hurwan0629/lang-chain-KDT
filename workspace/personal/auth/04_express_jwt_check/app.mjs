import express from "express"
import { config } from "./config.mjs"
import morgan from "morgan"
import cookieParser from "cookie-parser"

import connectDB from "./db/database.mjs"

import { currTime } from "./util/date.mjs"
import ApiRouter from "./router/api/index.mjs"

// express 객체 생성해주기
const app = express()

// 미들웨어 설정하기

// 개발용 로깅
morgan.token("curr-time", (req, res) => {
  return currTime()
})
app.use(morgan("[:curr-time] :method :url :remote-addr", { immediate: true }))

// 기본적인 렌더링
app.use(express.static("public"))
app.set("view engine", "ejs")
app.set("views", "/views")

// 파서
app.use(express.json())
app.use(express.urlencoded())
app.use(cookieParser())

// api 서버 라우팅
app.use("/api", ApiRouter)

app.use((req, res) => {
  res.status(404).end()
})

// 데이터베이스 설정 후 서버 열기
connectDB().then(() => {
  console.log(`데이터베이스 연결 완료: [${config.db.databaseName}]`)
  app.listen(config.host.port, config.host.listen_host, () => {
    console.log(`서버 실행중... ORIGIN: ${config.host.listen_host}`)
  })
}).catch((err) => {
  console.error(err)
  console.log("데이터베이스 연결중 에러 발생")
})
