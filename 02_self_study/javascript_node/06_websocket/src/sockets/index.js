// 기본적으로 소켓IO 서버에 대한 설정을 해주는 루트 파일
// 외부에서 registerSocketHandlers(io) 를 통해 소켓 객체를 이쪽으로 보내주면
// 이쪽에서 소켓서버에 대한 설정을 해주는 방식

// 접속된 소켓들의 정보를 저장해보기
export const socketList = {}

function registerSocketHandlers(io) {
  // 클라이언트의 연결이 들어왔을 때에 대한 콜백
  io.on("connection", (socket) => {
    // console.log("[서버] 소켓 연결 - socket:", socket)
    console.log("socket.id:", socket.id)

    // 소켓 리스트의 발언 목록들 준비해주기
    socketList[socket.id] = { datas: [] }

    // 직접 만들어보는 이벤트
    socket.on("client-says", (data) => {
      console.log("클라이언트의 메시지:", data)
      socketList[socket.id].datas.push(String(data?.message))
    })

    // 핸드셰이크 정보 확인해보기
    socket.on("my-handshake", () => {
      console.log("my-handshake 소켓 요청 들어옴")
      socket.emit("your-handshake", JSON.stringify(socket.handshake))
      console.log(JSON.stringify(socket.handshake, null, 2), "\n응답해줌")
    })

    socket.on("disconnect", (reason) => {
      console.log("socket의 연결이 끊어집니다.")
      console.log("연결 끊김 사유:", reason)
      console.log("해당 소켓 클라이언트의 발언 목록:", socketList[socket.id].datas)
    })
  })
}

export default registerSocketHandlers
