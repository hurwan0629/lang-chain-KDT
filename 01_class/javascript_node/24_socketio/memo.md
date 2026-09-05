# Express, socket.io 모듈에 대해서
**Socket.IO**는 클라이언트와 서버가 양방향으로 이벤트를주고 받게 해주는 라이브러리입니다.

공식 설명으로는 `low-latency, bidirectional, event-based communication`으로 연결/해제 없이 소켓을 연결된 상태 그대로 이벤트 기반의 동작을 하게 해주기 때문에 지연 없이 빠른 통신이 가능하게 해주는 전형적인 웹소켓의 구현 고수준 패키지입니다.

> **주의할 점**으로는 `Socket.IO`는 순수 웹소켓 프로토콜을 그대로 사용하는 것이 아닌 해당 프로토콜에서 한번 더 감싸서 고유한 기능과 전송 규칙을 추가한 자체 프로토콜 (메타데이터를 통한)이기 때문에 일반 웹소켓 클라이언트는 `Socket.IO`를 사용하는 서버에 바로 연결될 수 없습니다.

일반적으로 `socket.io`에서는 `Server`을 `export` 해줍니다. 이를 사용하기 위해선 일반적으로 다음과 같은 절차를 거치게 됩니다.

```js
import express from "express";
import { createServer } from "http";
import { Server } from "socket.io";

// 1. express 어플리케이션 생성
const app = express();
// 2. 기본 http 모듈을 이용한 httpServer을 생성
const httpServer = createServer(app);
/// 3. httpServer을 이용한 Socket.IO 서버 생성
const io = new Server(httpServer);

httpServer.listen(3000);
```

위에서 `io`는 `new Server()`에 대한 `Server` 객체입니다.

이를 통해서 **브라우저(클라이언트)**로부터의 요청을 `HTTP`와 `Websocket`연결 로 나누어 처리하게 됩니다.

## socket.io의 기본 형태
`socket.io` 패키지는 기본적으로 이벤트 기반의 서버입니다. 예를 들어 다음과 같이 이벤트를 설정하여 서버가 클라이언트의 요청을, 클라이언트가 서버의 요청을 들을 수 있게 됩니다.

```js
// Server
// `io`는 Server 객체
const userList = {}

io.on("connection", (socket) => { // socket는 클라이언트와 연결된 서버의 소켓 객체
  console.log("새로운 연결이 생성되었습니다.")
  socket.on("regist-socket", (data) => { // data는 선택적으로 클라이언트에서 보내는 데이터 (규약을 통해 설정)
    // `socket.id`는 소켓의 고유한 번호를 반환함 (이를 통해 맵으로 설정 가능)
    userList[socket.id] = data 
    console.log("새로 연결된 소켓이 등록되었습니다.")
  })

  socket.on("disconnect", () => {
    userList[socket.id] = undefined
    console.log("한 소켓의 연결이 해제되었습니다.")
  })
})
```

위는 하나의 코드 예시일 뿐으로 제공되는 여러 메서드를 이용하여 더 다채로운 구현이 가능합니다.

여기에서 주목할 객체는 `socket`인자로 `socket`는 클라이언트 하나와 연결된 통신 객체를 말합니다.

해당 객체는 `emit`, `on`, `once` 같은 Node.js의 `EventEmitter`라는 이벤트 기반 프로그래밍의 메서드를 상속합니다.

또한 `socket.broadcast.emit("event", "message")`를 통해 해당 소켓을 제외한 다른 소켓에 메시지를 뿌릴 수도 있습니다.

`io.to().emit()`와 `io.in().emit()`과 같은 경우에는 특정 방 또는 네임스페이스, 채널이라고 불리는 특정 그룹 또는 하나의 소켓을 지정하여 그 소켓으로만 데이터를 보낼 수 있게 해줍니다.

`.except()`를 통해서 특정 지점을 제외할 수도 있습니다.

## 클라이언트의 소켓
클라이언트의 경우에는 서버에서 `/socket.io/socket.io.js`와 같은 스크립트를 보내주어 여기에 존재하는 `io()` 함수를 이용하여 서버와 연결할 소켓 객체를 생성하게 됩니다.

해당 함수를 실행하게 된다면 클라이언트는 `Socket.IO` 서버에 연결을 시작하여 통신을 할 수 있게 해주게 됩니다.

> 위의 경우에는 클라이언트와 서버가 같은 경우이기 때문에 서버 주소가 다른 경우에는 `https://cdn.socket.io/4.8.3/socket.io.min.js`와 같은 CDN 스크립트를 사용하거나 `socket.io-client`라는 클라이언트 라이브러리 사용과 함께 자신의 주소를 `io(자신의 주소)`를 작성해주어야합니다. 또한 백서버에서는 `cors origin`을 다음과 같이 작성해주어야합니다.

```js
const io = new Server(httpServer, {
  cors: {
    origin: "http://localhost:5173",
    credentials: true
  }
});
```

## socket.handshake
`socket`객체에는 `socket.handshake`라는 속성이 존재합니다. 예를 들면 다음과 같은 형태로 존재하게 됩니다.
```js
{
  headers: {
    // 최초 요청의 HTTP headers
  },
  query: {
    // 최초 연결 URL의 query string
  },
  auth: {
    // 클라이언트가 auth 옵션으로 보낸 값
  },
  time: "...",
  issued: 1234567890,
  url: "/socket.io/?EIO=4&transport=polling&t=...",
  address: "::1",
  xdomain: false,
  secure: false
}
```

등과 같은 정보들을 내부에 가지고 있게 됩니다. 이는 클라이언트가 처음 Socket.IO 세션을 마늗ㄹ 때 들어온 초기 연결 정보를 말합니다.

