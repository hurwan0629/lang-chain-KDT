// 방, 참여자, transport, producer, consumer 상태 저장

// createRouter: 워커가 존재할 때 라우터를 생성해주는 함수
import { createRouter } from "./mediasoup.js"

// 채널의 형태
// 내부에는 roomName: room객체 가 존재하며
// room에는 이름, 라우터 (채널로 보내주는), 연결되어있는 RTC Transport를 관리하는듯 (peer로써)
const rooms = new Map()

// 방을 추가함 == 관리하는 라우터를 하나 만들어준다는 의미
export async function getOrCreateRoom(roomName) {
  let room = rooms.get(roomName)

  // 이미 만들어둔 방이 존재하지 않으면 추가해주기.
  // 방은 하나로 설정하는 형태인듯 함
  if(!room) {
    // 라우터 생성에는 시간이 좀 걸리는 듯 함
    const router = await createRouter()

    room = {
      name: roomName,
      router,
      peers: new Map()
    }
    rooms.set(roomName, room)
  
    console.log("room created:", roomName)
  }

  return room
}

// WebRTC 연결 시 사용자정보를 만들어 특정 방에 넣어주는 함수
export function addPeerToRoom(room, socket, userName) {
  room.peers.set(socket.id, {
    socket,
    userName,
    transports: new Map(), // 이후의 WebRTC연결
    producers: new Map(), // 클라이언트가 주는 정보들 받을곳
    consumers: new Map()  // 클라이언트에게 줄 통로
  })

  console.log("peer joined", socket.id, userName)
}

export function getRoom(roomName) {
  return rooms.get(roomName)
}