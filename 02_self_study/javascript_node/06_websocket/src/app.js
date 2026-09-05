import express from "express"
import { Server } from "socket.io"
import { createServer } from "http"
import config from "./config.js"
import Router from "./routes/index.js"

const app = express()

// 기본 설정만 간단히 해주고 static를 통해 html 줄 수 있게 해주기
app.use(express.json())

// console.log(config.host.resources)
app.use(express.static(config.host.resources))

// 일단 모든 요청을 index 라우터로 보내주기
app.use("/api", Router)

app.all("/", (req, res) => {
  res.send("아직 url이 만들어지지 않았습니다! /resoures 를 통해 html을 요청해주세요!")
})
// 여기서부터 

export default app

