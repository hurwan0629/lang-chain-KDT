import { addPeerToRoom, getOrCreateRoom, findProducer } from "./rooms.js"
import { createWebRtcTransport } from "./mediasoup.js"


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

    // 사용자가 자신과 소통할 WebRtcTransport 객체 하나 미리 만들어달라고 하는 이벤트
    socket.on("create-webrtc-transport", async ({ direction }, callback) => {
      try {
        const roomName = socket.data.roomName
        // roomName: { roomName, router: worker.createRouter(codec) , peers: Map() }
        const room = await getOrCreateRoom(roomName)
        // room(라우터)에 존재하는 클라이언트들중에서 id를 통해 O(1) 접근으로 가져오기 socket.id -> (socket, userName, transports, producers, consumers)
        const peer = room.peers.get(socket.id)

        // 해당 방에대한 router을 뽑아우기 (worker.createRouter())
        // router.createWebRtcTransport
        const transport = await createWebRtcTransport(room.router)

        // peer의 연결 객체에 transport.id와 방향 (지금은 클라이언트가 서버에 보내는 "send" 또는 서버가 주는 "recv")
        peer.transports.set(transport.id, {
          transport,
          direction
        })

        callback({
          ok: true,
          params: {
            id: transport.id,
            iceParameters: transport.iceParameters,
            iceCandidates: transport.iceCandidates,
            dtlsParameters: transport.dtlsParameters
            // stcp도 있는데 이건 지금은 필요 없고 data Channels 추가할 때 사용한다고 함
          }
        })
      } catch (error) {
        console.log(error)

        callback({
          ok: false,
          error: error.message
        })
      }
    })

    // 클라이언트에서 서버가 보내준 transportId와 클라이언트의 dtls 암호화 방식을 보내줌
    socket.on("connect-transport", async ({ transportId, dtlsParameters }, callback) => {
      try {
        const roomName = socket.data.roomName
        const room = await getOrCreateRoom(roomName)
        const peer = room.peers.get(socket.id)

        // transport.id -> WebRtcTransport객체, direction
        const transportData = peer.transports.get(transportId)

        // WebRtcTransport객체에서 transport 뽑아서 connect 해줌
        await transportData.transport.connect({
          dtlsParameters
        })

        console.log("transport connected:", transportId)

        callback({
          ok: true
        })
      } catch (error) {
        console.error(error)

        callback({
          ok: false,
          error: error.message
        })
      }
    })

    // 사용자로부터 제공받을 준비를 해라 라는 의미로 Producer 만들라는 의미이다.
    socket.on("produce", async ({ transportId, kind, rtpParameters }, callback) => {
      try {
        const roomName = socket.data.roomName
        const room = await getOrCreateRoom(roomName)
        const peer = room.peers.get(socket.id)

        const transportData = peer.transports.get(transportId)

        const producer = await transportData.transport.produce({
          kind,
          rtpParameters
        })

        peer.producers.set(producer.id, producer)

        console.log("[./socket.js socket.on(\"produce\")] producer created:", producer.id, kind)

        socket.to(roomName).emit("new-producer", {
          producerId: producer.id,
          socketId: socket.id,
          kind
        })

        callback({
          ok: true,
          producerId: producer.id
        })
      } catch (error) {
        console.error(error)

        callback({
          ok: false,
          error: error.message
        })
      }
    })

    // 클라이언트가 자신이 속한 방에 대한 생산자 정보를 모두 불러오기 위해 서버에 발생시키는 이벤트
    socket.on("get-producers", async (_, callback) => {
      try {
        // 소켓이 존재하는 방 이름 뽑아오기
        const roomName = socket.data.roomName
        const room = await getOrCreateRoom(roomName)

        // 넣어줄 생산자 목록 뽑아주기
        const producers = []

        for (const [peerSocketId, peer] of room.peers.entries()) {
          if (peerSocketId === socket.id) {
            continue
          }

          for (const producer of peer.producers.values()) {
            producers.push({
              producerId: producer.id,
              socketId: peerSocketId, // 생산자의 소켓 ID 뽑아주기
              kind: producer.kind
            })
          }
        }

        callback({
          ok: true,
          producers
        })
      } catch (error) {
        console.error(error)

        callback({
          ok: false,
          error: error.message
        })
      }
    })

    // 기대 소비자의 get-producers를 통한 생산자들의 Id를 받은 이후, 해당 소켓 클라이언트의 consume이벤트를 통해 transportId를 가진 사용자의 transport에 consume를 만들어줌
    // 이때 producerId는 get-producers를 통해 서버가 준 producerId를 말함.
    socket.on("consume", async ({ transportId, producerId, rtpCapabilities }, callback) => {
      try {
        const roomName = socket.data.roomName
        const room = await getOrCreateRoom(roomName)
        const peer = room.peers.get(socket.id)

        const transportData = peer.transports.get(transportId)
        const producer = findProducer(room, producerId)

        if (!producer) {
          throw new Error("producer not found")
        }

        if (!room.router.canConsume({ producerId, rtpCapabilities })) {
          throw new Error("cannot consume")
        }

        // console.log(peer)
        // console.log("transportData:", transportData)
        // console.log("transpoertId:",transportId)

        const consumer = await transportData.transport.consume({
          producerId,
          rtpCapabilities,
          paused: true
        })

        peer.consumers.set(consumer.id, consumer)

        callback({
          ok: true,
          params: {
            id: consumer.id,
            producerId,
            kind: consumer.kind,
            rtpParameters: consumer.rtpParameters
          }
        })
      } catch (error) {
        console.error(error)

        callback({
          ok: false,
          error: error.message
        })
      }
    })

    socket.on("resume-consumer", async ({ consumerId }, callback) => {
      try {
        const roomName = socket.data.roomName
        const room = await getOrCreateRoom(roomName)
        const peer = room.peers.get(socket.id)

        const consumer = peer.consumers.get(consumerId)

        if(!consumer) {
          throw new Error("consumer not found")
        }

        await consumer.resume()

        callback({
          ok: true
        })
      } catch (error) {
        console.log(error)

        callback({
          ok: false,
          error: error.message
        })
      }
    })

    socket.on("disconnect", async () => {
      // 서버에서 room.peers[socket.id] 지워주기
      const room = await getOrCreateRoom(socket.data.roomName)
      const peer = room.peers.get(socket.id)
      for (const consumer of peer.consumers.values()) {
        consumer.close()
      }

      for (const producer of peer.producers.values()) {
        producer.close()
      }

      for (const { transport } of peer.transports.values()) {
        transport.close()
      }

      room.peers.delete(socket.id)
      console.log("socket disconnected:", socket.id)
    })
// // // // io.on("connection", (socket) => {}) 끝   
  })
}