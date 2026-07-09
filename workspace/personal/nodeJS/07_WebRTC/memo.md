# Socket.io, mediasoup, Device, 미디어 스트림 (트랙), transport 등에 대해서 쭉 정리해보기

일단 이번에 약 2일동안 소화를 못하고 있는 내용이 웹 소켓이다. 스트림, 소켓, 포트 등의 이야기는 이미 알고 있었지만 트랙 등의 개념도 처음이고, 웹소켓이 소켓통신과 다른걸 몰랐었어서 또 새로웠다. 거기에 여러 프레임워크나 라이브러리 등의 사용법, 이벤트 기반의 서버 프로그래밍 등에 대해서 익숙하지 않아서 현재 [RTCPeerConnection](./ex_server/), [mediasoup](./ex_server_2/)에 대해서 작업을 해보긴 했는데 아직 2,3회독으로는 부족한 감이 있고 한번에 코드를 치면서 이해하다보니까 또 머리가 복잡해져서 정리를 한번 하고 가려고 한다.

---

SFU 방식에서 router은 보통 mediasoup의 createWorker을 통한 하위 프로세스 생성 후 `createRouter({ 코덱 설정 })`을 통해 이루어지게 된다. 여기에서 클라이언트에서 소켓 연결 이후 하게 되는 작업이 `new Device()`를 통한 객체 생성이다. 여기에서 `Device`는 mediasoup 서버와 직접 통신하는 객체는 아니며 브라우저쪽에서 mediasoup의 `RTP`/`코덱`/`Transport`의 처리를 도와주는 `mediasoup-client`패키지의 객체입니다.

> `mediasoup-client`는 TypeScript로 작성되어 JavaScript + CommonJS형태로 변환되어있다고 나와있습니다. 여기에서 CDN의 경우에는 `src`를 통해 받아오는 방법이 존재하며 `ES Module` 방식으로 `import`를 통해 가져오는 방식이 있습니다. 이는 파일마다 독립된 스코프를 가지며 전역 `window`에 자동 등록되지 않습니다. 또한 브라우저는 전통적으로 `commonJS`를 사용하지 않기 때문에 이를 `ems.sh`와 같은 ESM CDN이 `commonJS`같은 구조를 브라우저가 `type="module"`방식으로 읽을 수 있게 `ESM` 모듈 방식으로 바꿔주는 방식입니다.

### [클라이언트] 서버에 소켓 연결
클라이언트가 생성됨과 동시에 `Socket.io`의 `io()`를 통해 즉시 소켓이 만들어지게 됩니다.(지연시킬 수 있지만 일단 패스) 이후 `socket.emitWithAck`를 통해 서버 채널에 대한 `rtp 규격`을 요청하게 된다면 이에 대해서 해당 요청 이벤트를 버퍼(이벤트 큐)에 등록한 후 소켓 연결이 확립된과 동시에 서버에 보내게 됩니다.

### [서버] mediasoup, Worker, router 생성 및 rtpCapability응답 준비
서버쪽 잠깐 보고 가면 mediasoup를 통해 worker를 만든 후에, 거기 안에서 worker가 특정 규격의 router(room 또는 채널이라고도 부름)을 만들어서 거기에 대해서 코덱을 설정이 되어있음과 동시에 이미 시작되는 순간에 등록되어 개발자가 작성한 `get-channel-rtp-capabilities` 같은 이벤트에 대해서 등록되게 됩니다. 현재까지의 `mediasoup`의 주요 객체는 router, worker 정도입니다.(transport, producer, consumer 제외)

> 계층적으로 하나의 worker 안에 여러 router이 존재하며 그 router안에 여러 transport, transport 하위의 producer과 consumer이 존재합니다.

### [클라이언트] 서버의 규격에 대해서 스스로 확인하기
위와 같은 `rtpCapabilities`를 받게 된다면 클라이언트는 `mediasoup-client`에 존재하는 `Device`객체를 이용하여 가능한 RTP 규격을 스스로 설정하게 됩니다. 여기에서 사용되는 메서드가 `[Device객체].load({ routerRtpCapabilities })`입니다.

> 여기에서 `Device`객체는 실제로 연결을 담당하는 객체가 아닌 `RTP`, `코덱`, `Transport` 등을 관리해주는 객체입니다. 다른 속성으로는 `canProduce`, `rtpCapabilities`, `sendRtpCapabilities` 등이 존재합니다.

> `rtpCapabilities`의 경우에는 `JSON`형태로 이루어져 있기 때문에 구조가 다른 경우 오류가 나기 쉽지만 이 또한 `mediasoup`에서 정한 `RtpCapabilities` 타입이기 때문에 서버에서 주는 그대로 사용이 가능합니다. (모두 `medieasoup.RtpCapabilities`타입이여서) 전체적인 구조는 `codecs배열`, `headersExtensions`로 이루어져 있으며 `codecs`에는 `kind`, `mimeType`, `시간간격`, `기타 파라미터 또는 채널 등`이 존재하며 `headersExtensions`에는 RTP 패킷에 붙는 추가 정보로 대상, 식별자, 암호화, 사용 방향 등에 대한 추가 확장자를 설정하게 됩니다.

### [클라이언트] 서버에 연결 준비 요청하기
클라이언트가 서버와 연결되기 위해선 몇가지 조건이 존재합니다.
- 클라이언트의 발송/수신용 연결
- 서버의 해당 클라이언트에 대한 발송/수신용 연결
- 해당 연결이 들어갈 `router`
- 해당 연결을 문제 없이 하기 위한 연결 정보

여기에서 연결의 시작은 보통 클라이언트의 이벤트 생산을 통해 시작되며 해당 요청을 통해 서버는 `createWebRtcTransport(router)`을 통해 통신 창구를 하나 만들어주게 되며 이의 반환 값으로 연결 객체인 `WebRtcTransport객체`를 반환하게 되는데 이곳에는 향후 클라이언트와 핸드셰이크를 위해 필요한 `id`, `iceParameters`, `iceCandidates`, `dtlsParameters`와 같은 `ice` 정보와 암호화 정보가 존재하여 이를 클라이언트에게 제공함으로써 클라이언트가 이것을 최종 연결에 사용이 가능하게 됩니다.

용어에 대해 설명을 간단히 하면
- ICE: 상호 연결 확립의 약자로 외부와 자신이 통신할 수 있는 경로(IP, 포트, 프로토콜, 경로)를 아는 절차(프로토콜 또는 프레임워크정도).
- `iceCandidates`: 연결할 후보 주소 목록
- `iceParameters`: ICE 연결 과정에서 서로를 인증하고 매칭하기 위한 정보. (사용자 이름, 비밀번호, 더 가볍게 연결 검사를 하는 ICE lite방식 여부)
- `dtlsParameters`: 말했듯 인증서가 맞는지 확인하기 위한 알고리즘과 키의 목록들
- `WebRtcTransport객체`: ICE와 DTLS 절차로 협상된 경로. 향후 클라이언트의 `transport` 객체와 미리 확립한 ICE/DTLS를 통해 연결하게 됩니다. 이렇게 연결에 필요한 데이터들을 미리 교환해두며 실제 `produce/consume` 순간에 연결 검사를 진행하여 최종 경로를 확정하게 됩니다.

### [클라이언트] 자신이 보낼 transport를 생성함
위에서 서버가 연결할 경로에 대한 준비를 마쳤다면 이제 클라이언트는 위에에서 받은 `WebRtcTransport객체`에 대한 id, 파라미터 등을 받게 됩니다. 이를 기반으로 `Device.createSendTransport({ id, iceCandidates, iceParameters, dtlsParameteres })`를 생성하게 됩니다. 해당 값의 반환값은 `Transport`객체를 구현한 `mediasoup-client.SendTransport`입니다. 해당 객체를 만들려면 그에 대응하는 서버의 `WebRtcTransport`가 존재해야합니다. `Transport` 객체는 내부적으로 `RTCPeerConnection`을 다룹니다.

`SendTransport`객체의 속성은 대략 다음과 같습니다.
- `.id`
- `.closed`
- `.connectionState`
- `.on("이벤트", ...)`
- `.produce({ 트랙 })`

여기에서 주목할 점은 `createSendtransport()` 순간에 연결되는 것이 아닌 먼저 `connect`와 `produce`에 대한 이벤트를 구독한 후 최초로 `SendTransport.produce()`를 하는순간에 연결이 시작됩니다. (이미 되어있으면 패스) 이렇게 되면 `mediasoup-client`에서 `SendTransport`의 `"connect"`이벤트와 함께 내부적으로 만든 `dtls` 데이터를 인자로 넣어주게 됩니다. 

이때 `SendTransport`의 `connect` 이벤트 발생 시 서버로 자신의 `SendTransport.id`와 `dtlsParameters`를 보냄으로써 자신이 어떤 경로로 어떤 암호를 통해 연결할 것인지를 알려주게 됩니다. 여기서 포인트는 `SendTransport.id`와 서버의 `WebRtcTransport.id`가 동일하여 둘이 한 쌍으로 같은 연결을 바라보는 서로 다른 객체라고 해석할 수 있습니다.

이렇게 연결된 `WebRtcTransport`를 기반으로 해당 암호화/경로 등을 사용하는 `Producer`을 만들어 사용하며 `Consumer`의 경우에도 동일한 원리로 동작합니다.

### [서버] WebRtcTransport에 대한 producer 생성
클라이언트의 `SendTransport`와 `WebRtcTransport`가 연결되었다면 클라이언트의 제공한다는 요청을 통해 서버의 `WebRtcTransport`가 `Producer객체`를 메서드를 통해 생성할 수 있습니다. `WebRtcTransport.produce({ kind, rtpParameters, paused?: false, appData?: [식별자 또는 객체] })`

또한 해당 반환값 `Producer`객체의 `id`를 반드시 클라이언트에게 응답으로 주어야하며, 클라이언트는 `on("produce", ..., callback)` 의 `callback{ id: producerId }`를 실행해주어 서버의 `Producer`로 연결하는 과정을 가져야합니다.

### [클라이언트] 자신의 미디어 트랙들을 서버에 전송
일반적으로 브라우저에는 `navigator.mediaDevices`라는 미디어 관련 메서드를 가지고 있는 속성이 존재하며 그중 `.getUserMedia()`를 통해 내부에 `MediaStreamTrack`를 가지고 있는 `MediaStream`객체를 받을 수 있습니다.

여기에서 클라이언트는 해당 트랙을 `produce`하기 위해선 `SendTransport.on("produce")`가 등록되어있어야하며, `SendTransport.produce({ track })`가 이루어 질 시 `track`가 `{ kind, rtpParameters }`로 반환되어 `"produce"` 이벤트를 발생시킵니다. 이는 곧 서버에 `sendTransport.id`와 함께 전송하게 되며, 서버는 해당 `WebRtcTransport.id`를 통해 `transport.produce({ kind, rtpParameters })`를 통해 `Transport`하위의 `Producer` 객체를 만들어주게 됩니다. 또한 클라이언트에게 다시 `Producer.id`를 주어 클라이언트의 `callback({ id })`로 최종적으로 `Device`에 등록해주게 됩니다.

이렇게 등록된 `Producer`은 향후 `router.canConsume( producer, rtpCapabilities )`를 통해 확인 후 `WebRtcTransport.consume({ producerId, rtpCapabilities, paused })`을 통해 `Consumer`이 생성될 수 있습니다.

최종적으로 `MediaStreamTrack`를 `recvTransport.consume({ id, producerId, kind, rtpParameters })`를 통해 받아온 `new MediaTrack(consumer.track)`로 만들어 영상/음향에 등록해줄 수 있습니다.

## [TIP] 알아야하는 객체들의 구조
해당 구성도에서 **브라우저**는 `socket.io`, `mediasoup-client Device`, `send/recvTransport`, `Producer/Consumer wrapper`, `MediaStream/MediaStreamTrack`로 이루어져 있으며 브라우저의 내부 `WebRTC` 엔진에는 `RTCPeerConnection`, `ICE`, `DTLS`, `SRTP`, `RTP/RTCP 패킷 처리 기능`, `UDP/TCP 네트워크 소켓 기능` 등이 존재합니다.

**Node.js** 서버 프로세스의 경우에는 `Socket.io`, `mediasoup Worker`, `Router`, `Transport`, `Producer`, `Consumer`과 관리를 위한 `Map`객체 등이 존재합니다. 

**mediasoup-worker** 프로세스의 경우에는 실제 미디어 처리를 위한 `ICE 처리`, `DTLS 처리`, `RTP/RTCP 송수신`, `Router 내부 RTP 라우팅`, `Producer/Consumer의 실제 패킷 처리`, `UDP/TCP 포트 listen` 기능을 담당하게 됩니다.

여기에서 `Node.js`의 경우에는 데이터 미디어 데이터의 송수신은 담당하지 않으며 `mediasoup-worker`이 담당하게 됩니다.

**WebRtcTransport**의 경우에는 소켓 등과 같은 특정 스트림을 읽는 객체보다는 클라이언트 브라우저(WebRtc브라우저)부터 `mediasoup`의 라우터까지 연결해주는 객체입니다. 여기에서는 ICE 상태, DTLS 상태, 선택된 ICE tuple, RTP/RTCP 송수신 경로, 위에 붙어있는 Producer/Consumer 객체를 관리하는 객체입니다. 또한 사용하는 포트의 경우에는 일반적으로 하나의 포트에 하나의 Transport가 할당되며, 경우에 따라 하나의 포트를 통해 여러 생산/구독자를 처리할 수 있습니다. 

**Producer/Consumer**의 경우에는 해당 객체들이 포함되어있는 `WebRtcTransport`의 경로를 공유하게 됩니다. 또한 식별의 경우에는 내부적으로 통신에 쓰이는 안내서 역할인 `rtpParameters`에 존재하는 포멧 및 식별자 등을 활용하여 어떤 객체에 데이터 흐름을 붙여줄지 판단하게 됩니다.



