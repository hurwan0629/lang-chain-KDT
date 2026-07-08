import express from "express"
import { Server } from "socket.io"
import { createServer } from "http"
import path from "path"
import { fileURLToPath } from "url"

const PORT = 8091
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

const app = express()
app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "/public/chat_index.html"))
})

const server = createServer(app)
const io =  new Server(server)

app.use(express.static(path.join(__dirname, "public")))

const users = {}
io.on("connection", (socket) => {
  console.log("사용자가 연결되었음")

  // join: 원래 존재하지 않는 이벤트
  socket.on("join", ({ nickname, channel }) => {
    socket.nickname = nickname
    socket.channel = channel
    users[socket.id] = { nickname, channel }

    socket.join(channel)

    console.log(`[${channel} 채널] {${nickname}}님의 접속 | 소켓ID: ${socket.id}`)

    // 서버에서 클라이언트로 사용자에게 메시지 보내주기
    const msg = { user: "system", text: `${nickname}님이 입장했습니다.` }
    // 클라이언트에 "message" 이벤트 열어주기
    io.to(channel).emit("message", msg)
    // io.emit("message", msg)
    console.log("[서버]: 클라이언트에 message 이벤트 호출:", msg)

    updateUserList()
  })

  socket.on("chat", ({ text, to }) => {
    // user = {} 에서 사용자 꺼내기
    const sender = users[socket.id]
    if(!sender) return

    const payload = { user: sender.nickname, text }

    console.log("to:", to)

    if(to) {
      const receiverSocket = Object.entries(users).find(([id, u]) => (u.nickname === to))?.[0]

      if(receiverSocket) {
        console.log(receiverSocket)
        payload.user = `${payload.user} -> ${to}`
        io.to(receiverSocket).emit("whisper", payload)
        // socket.emit("whisper", payload)
        console.log(`[서버]: {${sender.nickname}}님의 "whisper"이벤트 요청: {${users[receiverSocket.id]?.nickname}}에게 [${text}] | payload: [${payload}]`)
      }
      else {
        io.to(sender.channel).emit("message", payload)
        console.log(`[서버] [${sender.channel} 채널]: {${sender.nickname}}님의 "chat"이벤트 요청: ${text} | payload: [${payload}]`)
        // io.emit("message", payload)
      }
    }
    else {
      // io.to(sender.channel).emit("message", payload)
      console.log(`[서버] [${sender.channel} 채널]: {${sender.nickname}}님의 "chat"이벤트 요청: ${text} | payload: [${payload}]`)
      io.emit("message", payload)
    }

  })

  socket.on("changeChannel", ({ newChannel }) => {
    const oldChannel = socket.channel
    const nickname = socket.nickname
    socket.leave(oldChannel)
    io.to(oldChannel).emit("message", {
      user: "system",
      text: `${nickname}님이 ${newChannel} 채널로 이동했습니다.`
    })

    socket.channel = newChannel
    users[socket.id].channel = newChannel
    socket.join(newChannel)
    const joinMsg = { user: "system", text: `${nickname}님이 입장했습니다.`}
    io.to(newChannel).emit("message", {
      user: "system",
      text: `${nickname}님이 입장했습니다.`
    })
    updateUserList()
    
  })

  socket.on("disconnect", () => {
    // console.log("사용자가 연결을 끊었습니다.")
    const msg = { 
      user: "system",
      text: `${users[socket.id]?.nickname}님이 접속을 끊었습니다.`
    }
    io.to(users[socket.id].channel).emit("message", msg)
    
    users[socket.id] = undefined

    
    updateUserList()
  })

  function updateUserList() {
    
    const userList = Object.values(users)
    // console.log(`현재 접속자 명단: ${JSON.stringify(userList)}`)

    io.emit("userList", userList)
  }
})

server.listen(PORT, "0.0.0.0", () => {
  console.log("서버 실행 중...")
})

