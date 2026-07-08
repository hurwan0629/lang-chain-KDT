// 브라우저와 주고받는 signaling 이벤트 처리
// 워커의 생성을 담당하며 
// 라우터를 생성해준다.

import mediasoup from "mediasoup"

let worker

const mediaCodecs = [
  {
    kind: "audio",
    mimeType: "audio/opus", //인코딩/디코딩을 모두 합친 용어인 Codec를 의미하는 단어로 mime 타입을 알려주는 것
    clockRate: 48000, // 1초를 48000등분하여 계산한다는 의미 (계산하는 시간의 단위를 맞추는 형태. 48프레임이면 1000단위로 계산하는 형태)
    channels: 2
    // 1: mono 오디오
    // 2: stereo 오디오
    // 채널은 타입 선택
  },
  {
    kind: "video",
    mimeType: "video/VP8",
    clockRate: 90000,
    parameters: {
      "x-google-start-bitrate": 1000 // 시작 비트레이트 힌트를 1000kbps정도로 준다는 뜻
      // 비트레이트가 높을수록 화질이 좋고 네트워크 부담이 됨
      // 일단 적절히 시작하고 이후에 계속 조절해나가는 방식
    }
  }
]

export async function createMediasoupWorker() {
  // 해당 파일의 전역 변수인 worker에 Worker 객체 만들어서 넣어주기.
  // 해당 워커는 4만대 포트 번호에 RTC 연결을 관리할 수 있음
  worker = await mediasoup.createWorker({
    rtcMinPort: 40000,
    rtcMaxPort: 49999
  })

  console.log("mediasoup 워커 생성. worker.pid:", worker.pid)

  worker.on("died", () => {
    console.error("mediasoup worker died")
    process.exit(1)
  })
}

// 라우팅을 할 방을 만들어주는 함수
export async function createRouter() {
  if(!worker) {
    throw new Error("mediasoup worker is not created")
  }

  const router = await worker.createRouter({
    mediaCodecs
  })

  console.log("[/mediasoup.js createRouter] mediasoup router created:", router.id)
  
  return router
}