import { createServer } from "http"
import app from "./app.js"
import config from "./config.js"
import registerSocketHandlers from "./sockets/index.js"
import { Server } from "socket.io"

// // // // // // // // // // // // // // // // // // // // // // // // 
// Express 앱을 Node.js HTTP 서버의 요청 처리 함수로 등록
// app는 호출 가능한 한수이면서 Express 기능을 가진 객체
// app는 개념적으로 function app(req, res)와 같은 형태를 가짐
// 따라서 .get() 등과 같은 메서드와 함께 함수로 쓰일 수 있다.

// createServer()의 경우에는 createServer(requestListener) 또는 createServer(options, requestListener)과 같이 설정할 수 있습니다.
// 여기에서 requestListener은 (req, res) 형태를 가지며
// req: http.IncomingMessage 타입을 가지고
// res: http.ServerResponse 타입을 가집니다.
// 위의 타입은 app(express())이 받는 객체와 동일합니다.
const httpServer = createServer(app)
const io = new Server(httpServer, {
  cors: {
    origin: ["http://localhost:3000", "http://127.0.0.1:3000"],
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
  }
})

registerSocketHandlers(io)

// http 모듈의 서버를 이용하여 포트로부터 데이터를 받아주기.
httpServer.listen(config.host.port, () => {
  console.log("서버 구동중...")
})