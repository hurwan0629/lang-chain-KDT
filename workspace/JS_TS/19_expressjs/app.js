/*
    Express
    - node.js 환경에서 가장 널리 사용되는 웹 애플리케이션 프레임워크, 서버를 쉽고 빠르게 구축할 수
    있도록 다양한 기능을 제공
    - 기본적인 HTTP 모듈보다 훨씬 간단하게 라우팅 처리, 요청/응답 객체 관리, 미들웨어 설정, 정적
    파일 제공, 템플릿 엔진 연결 등을 할 수 있어 개발 생산성을 크게 높여줌

    라우팅
      클라이언트가 어떤 URL과 HTTP 메서드(GET, POST)로 요청을 보냈을 때 그 요청을 어떤 코드가
      처리할지 연결해주는 규칙

    미들웨어
    - 요청(request)과 응답(response) 사이에서 중간에 실행되는 함수로, 클라이언트의 요청을 직접
    처리하기보다는 가공/검사/추가 작업을 담당하는 역할을 함
    - 요청 로그를 남기거나, JSON 데이터를 파싱하거나, 로그인 여부를 검사하거나, 에러를 처리하는
    기능들이 모두 미들웨어


*/

const express = require("express")
const path = require("path")

port = 8090
const app = express()
app.use("/resource", express.static('public'))
app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "view"))



// 미들웨어
// app.use((req, res, next) => {
//   console.log("hello")
// })

app.get("/", (req, res) => {
  // res.send("Hello Express")
  res.setHeader("Content-Type", "text/html")
  res.render("index", {
    name: "허완"
  })
})

app.listen(port, () => {
  console.log("서버 실행 시작")
})