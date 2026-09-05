/*
  1. 경로설정
  http 모듈에서 경로 설정(라우팅)을 사용자의 요청 주소를 나타내는 
  req.url과 요청 방식인 req.method를 확인하여 조건문으로 분기 처리하는 방식으로 이루어짐

  2. GET과 POST
    GET: 서버로부터 데이터를 조회할 때 사용하는 요청 방식으로, 주로 게시글 목록 보기, 검색 결과 조회, 상세 페이지 열기처럼
    데이터를 가져오는데 사용됨. GET요청은 필요한 값을 URL 뒤에 ?KEY=VALUE 형태의 쿼리 문자열로 함께 전달하며, 브라우저 주소창에 그대로 표시한다.

    POST: 서버에 데이터를 전송해서 새로운 데이터를 생성하거나 기존 데이터를 변경할 때 사용하는 요청 방식으로, 회원 가입, 로그인, 글 작성, 파일 업로드 등에 사용됨. 
    POST요청은 데이터를 URL이 아니라 요청 본문(body)에 담아 보내기 때문에 주소창에 내용이 보이지 않으며, GET보다 보안성이 조금 더 높고 전송할 수 있는 데이터의 양에도 제한이 거의 없음

    if(req.url === "/login" && req.method === "POST") {
      res.end("로그인 처리")
    }
    
  3. 쿼리 문자열
  - 쿼리 문자열(Query String)은 URL 뒤에 ?기호를 기준으로 붙는 추가 데이터 전달 방식으로, 서버에 필요한 값을 함께 보내기 위해 사용됨
  - key=value 형태로 작성하며 여러 개의 값은 & 기호로 연결함 (예: ?name=김사과&age=20)
  - 주로 GET 요청에서 사용되며 검색 조건, 페이지 번호, 필터 값 등을 전달할 때 많이 활용

  nodemon
  - node.js 개발 시 자주 사용하는 유틸리티로, 소스 코드가 변경될 때마다 자동으로 서버를 재시작해주는 도구
  - `npm install -g nodemon` `-g`: 모든 프로젝트에서 사용 가능
  - `npm install --save-dev nodemon` (해당 프로젝트에서만 사용)
*/
const http = require("http")
const { parse } = require("path")
const url = require("url")

const server = http.createServer((req, res) => {
  console.log("요청 도착:", req.method, req.url)
  // 모든 도메인의 요청을 허용하려면 '*'를 사용합니다.
  res.setHeader('Access-Control-Allow-Origin', '*'); 
  
  // 허용할 HTTP 메서드 설정 (필요에 따라 지정)
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'); 
  
  // 허용할 헤더 설정
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  // const url = req.url
  // const parseUrl = url.parse(req.url, true)

  // console.log(req.headers.host)

  const parseUrl = new URL(req.url, `http://${req.headers.host}`)
  // console.log(`\n`)
  // console.log(parseUrl)
  // console.log(`\n`)
  // console.log(parseUrl.pathname)
  // console.log(parseUrl.searchParams.get("hello"))
  // console.log(`\nend`)

  // preflight 요청은 여기서 바로 종료
  if (req.method === "OPTIONS") {
    console.log("preflight 처리")
    res.writeHead(204)
    return res.end()
  }
  

  if(parseUrl.pathname === "/") {
    console.log("parseUrl.pathname === /")
    res.writeHead(200, {"Content-Type":"text/plain; charset=utf-8"})
    req.on("data", (data) => {
      console.log(data)
      console.log(data.toString())
      res.end(data.toString())
    })
    // res.end("<h2>안안ㅇ안녕 Node.js</h2>")
  }
  else if(parseUrl.pathname === "/about") {
    res.writeHead(200, {"Content-Type":"text/html; charset=utf-8"})
    res.end("<h2>저는 서버입니다..</h2>")
  }
  else if(parseUrl.pathname === "/404") {
    res.writeHead(200, {"Content-Type":"text/html; charset=utf-8"})
    res.end("<h2>페이지를 찾을 수 없습니다..</h2>")
  }
  else if(parseUrl.pathname === "/api/user") {
    const user = {
      userId: "apple",
      name: "김사과",
      age: 20
    }
    res.writeHead(200, {"Content-Type": "application/json"})
    res.end(JSON.stringify(user))
  }
})
server.listen(8091, "127.0.0.1", () => {
  console.log("서버 실행 시작")
})