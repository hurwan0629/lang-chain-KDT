# 2026-07-16 22:04:51 - React/Node 기반 Router/Node 연습
현재 React의 hook/Router과 가능하면 react-style까지 한번 보려하고 있는데 React만 쓰면 연습이 잘 안되기도 하고 슬슬 풀스택 및 전반적인 프로젝트 개발에 반복 연습을 시작할 적절한 타이밍이 되었다 판단하여 프로젝트를 파며 연습을 합니다.

## 사용하는 패키지 
업데이트: `2026-07-16 22:18:53`
### 서버
- Express
- cookie-parser
- jwt
- nodemon (Dev)
- cors

### 클라이언트(React)
- React
- react-router-dom

### 데이터베이스
- users
  - pk
  - id
  - password_hash
  - name
  - phone
  - created_at
- rooms
  - pk
  - id
  - title
  - host: [foriegn key: users.pk]
  - deleted: bool
  - created_at
- replies
  - pk
  - writer: [foriegn key: users.pk]
  - room: [foriegn key: room.pk]
  - content
  - created_at

## 만들 기능
### 회원
- 회원가입
- 로그인
- 마이페이지
- 로그아웃
### 방 생성
- 방 만들기
- 방 조회(검색)하기
- 방 입장하기
- 방 나가기
- 방 수정하기 (호스트)
- 방 삭제하기
- 방에 글 작성하기