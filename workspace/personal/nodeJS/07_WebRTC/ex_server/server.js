import { Server } from "socket.io"
import express from "express"
import { createServer } from "http"
import { fileURLToPath } from "url"
import path from "path"

const app = express()
app.use(express.static(path.join(path.dirname(fileURLToPath(import.meta.url)), "public")))

const httpServer = createServer(app)

const io = new Server(httpServer)

const client = {}
let joinedClient = {}
io.on("connection", (socket) => {
  
  client[socket.id] = socket
  console.log(Object.keys(client).length)
  // 한 클라이언트가 자신이 참가할 의사가 있음을 알림
  socket.on("rtc_offer", (offer) => {
    joinedClient[socket.id] = socket
    // 서버에서 요청 들어온 소켓 이외의 다른 클라이언트들에게 쓸 수 있는 미디어 있는지 물어봄
    socket.broadcast.emit("offered", offer)
  }) 

  // emit("offered") 에 대한 응답이 들어오면 다시 클라이언트에게 응답 보내주기
  socket.on("answer", (answerData) => {
    socket.broadcast.emit("rtc_offer_response", answerData)
  }) 

  // 상대의 주소를 알기 위한 candidate
  socket.on("ice_candidate", (candidate) => {
    socket.broadcast.emit("ice_candidate", candidate)
  })

  // 나가면 모두에게 알려주기
  socket.on("disconnect", () => {
    delete client[socket.id]
    delete joinedClient[socket.id]
  })
})

httpServer.listen("8091", "0.0.0.0", () => {
  console.log("서버 구동 시작...")
})