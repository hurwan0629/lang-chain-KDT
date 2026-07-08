import http from "http"
import app from "./app.js"
import { Server } from "socket.io"
import registerSocketHandler from "./socket.js"

// 워커 하나 만들고 시작해주기
// 소켓 이벤트 등록하기 전에 사용할 워커가 준비되어있어야한다
import { createMediasoupWorker } from "./mediasoup.js"
await createMediasoupWorker()

const httpServer = http.createServer(app)
const io = new Server(httpServer)

registerSocketHandler(io)

httpServer.listen("8091", () => {
  console.log("server started: http://localhost:8091")
})