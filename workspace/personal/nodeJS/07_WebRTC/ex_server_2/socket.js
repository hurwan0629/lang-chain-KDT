import { addPeerToRoom, getOrCreateRoom } from "./rooms.js"


export default function registerSocketHandler(io) {
  // io 소켓 서버에 핸들러 등록해주기
  io.on("connection", (socket) => {
    console.log("socket connected:", socket.id)

    // 사용자가 방에 들어오겠다고 하면 방 이름과 사용자 이름을 통해 방(라우터) 만들어주기
    socket.on("join-room", async ({ roomName, userName }, callback) => {
      try {
        // 들어가려는 방 만들어주기 (있으면 그냥 반환)
        // 생성에는 워커에 요청해서 라우터 만들어줘 하는 과정이 필요하기 때문에 비동기 + await 사용
        const room = await getOrCreateRoom(roomName)

        // 위에서 받아온 방에 해당 클라이언트에 대한 소켓과 사용자 이름 넣어주어 Transport 등록해주기
        addPeerToRoom(room, socket, userName)

        // 소켓 자체를 통해서도 채널 확인과 이름 확인 가능하게 정보 저장해주기
        socket.data.roomName = roomName
        socket.data.userName = userName

        // 위에 등록이 잘 진행 되었다면 잘 되엇다고 뭔가 다시 보내주기. (클라이언트에게 callback용 데이터 전달해주기 - 서버에서 실행되는 callback 아님)
        callback({
          ok: true,
          socketId: socket.id
        })

        console.log("room status:", room)
      } catch (error) {
        console.error(error)
        // 실패했으니까 응답으로 보내주기.
        // callback는 response에 가까운 것으로 추정
        callback({
          ok: false,
          error: error.message
        })
      }
    })

    // 브라우저가 mediasoup-client Device를 만들 때 필요한 정보를 주는 방식
    socket.on("get-router-rtp-capabilities", async (_, callback) => {
      try {
        // 우선 해당 소켓이 들어가있는 roomName가 존재하는지 확인
        // (이미 들어갔다면 socket.data.roomName = roomName를 해주기 때문에)
        const roomName = socket.data.roomName
        // 라우터만 생성해주는 함수
        const room = await getOrCreateRoom(roomName)

        callback({
          ok: true,
          rtpCapabilities: room.router.rtpCapabilities
        })
      } catch (error) {
        console.error(error)

        callback({
          ok: false,
          error: error.message
        })
      }
    })

    socket.on("disconnect", () => {
      console.log("socket disconnected:", socket.id)
    })
// // // // io.on("connection", (socket) => {}) 끝   
  })
}