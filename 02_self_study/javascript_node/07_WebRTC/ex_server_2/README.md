# SFU역할을 하는 서버의 webRTC

프론트의 경우에는 아래의 요소가 존재하게 할 것임
- 채널
- 접속자
- 접속자 화면 보기 (일단 처음에는 쭉 그리드나 플랙스로 나열해놓고 나중에 크기 줄이거나 버튼으로 렌더링 선택하게 하기)


백의 경우에는 아래 요소 포함시키기
- 사용자의 접속 채널
- 사용자들이 보내주는 미디어트랙

---

연결 방식
1. mediasoup Worker 생성
2. 사용자가 room에 입장 (Router 생성 또는 참가)
3. 클라이언트가 RTP Capabilities 요청 
4. 클라이언트의 mediasoup-client 생성
5. 클라이언트가 send transport 를 통해 서버와 WebTrcTransport 생성 후 ice 정보 받음
6. 