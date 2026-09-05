/*
    1. 경로 설정
    http 모듈에서 경로 설정(라우팅)은 사용자의 요청 주소를 나타내는 req.url과 요청 방식인 req.method를 확인하여 조건문으로 분기 처리하는 방식으로 이루어짐

    127.0.0.1:3000/
    127.0.0.1:3000/about

    2. GET과 POST
        GET: 서버로부터 데이터를 조회할 때 사용하는 요청 방식으로, 주로 게시글 목록 보기, 검색 결과 조회, 상세 페이지 열기처럼 데이터를 가져오는 데 사용됨. GET 요청은 필요한 값을 URL 뒤에 ?key=value 형태의 쿼리 문자열로 함께 전달하며, 브라우저 주소창에 그대로 표시
        POST: 서버에 데이터를 전송하여 새로운 데이터를 생성하거나 기존 데이터를 변경할 때 사용하는 요청 방식으로, 회원 가입, 로그인, 글 작성, 파일 업로드 등에 사용됨. POST 요청은 데이터를 URL이 아니라 요청 본문(body)에 담아 보내기 때문에 주소창에 내용이 보이지 않으며, GET보다 보안성이 조금 더 높고 전송할 수 있는 데이터의 양에도 제한이 거의 없음

        127.0.0.1:3000/login
        if(req.url === "/login" && req.method === "post") {
            res.end("로그인 처리")
        }

    3. 쿼리 문자열
        - 쿼리 문자열(Query String)은 URL 뒤에 ?기호를 기준으로 붙는 추가 데이터 전달 방식으로, 서버에 필요한 값을 함께 보내기 위해 사용됨
        - key=value 형태로 작성하며 여러 개의 값은 & 기호로 연결함 (예: ?name=김사과&age=20)
        - 주로 GET 요청에서 사용되며 검색 조건, 페이지 번호, 필터 값 등을 전달할 때 많이 활용

    코드러너 실행: 컨트롤 + 알트 + n

    nodemon
    node.js 개발 시 자주 사용하는 유틸리티로, 소스 코드가 변경될 때마다 자동으로 서버를 재시작해주는 도구
        npm install -g nodemon (모든 프로젝트에서 사용 가능, 권장 X)
        npm install --save-dev nodemon (해당 프로젝트에서만 사용)


    JSON
    - 자바스크립트 객체 표기법을 기반으로 한 데이터 교환 형식
    - 일반적으로 서버와 클라이언트 간에 데이터를 주고 받을 때 사용
    - 구조는 키-값 쌍으로 이루어진 객체 형태나 배열 형태를 사용

        const user = { name: "김사과", age: 20 }
        const jsonStr = JSON.stringify(user)    // 객체를 문자열로 변환

        const jsonStr = "{ name: "김사과", age: 20 }"
        const userObj = JSON.parse(jsonStr)     // 문자열을 객체로 변환
*/
const http = require("http")
const url = require("url")


const server = http.createServer((req, res) => {
    // url.parse(req.url, true) // : true는 query string을 객체로 자동 변환

    console.log(req.url)
    console.log(req.headers.host)
    const myUrl = new URL(req.url, `http://${req.headers.host}`)
    console.log(myUrl.pathname)
    console.log(myUrl.searchParams.get("userid"))
    console.log(myUrl.searchParams.get("name"))
    console.log(myUrl.searchParams.get("age"))

    if(req.url === "/"){
        res.writeHead(200, {"Content-Type": "text/html"})
        res.end("<h2>Hello Node.js</h2>")
    }else if(req.url === "/about"){
        res.writeHead(200, {"Content-Type": "text/html"})
        res.end("<h2>about page</h2>")
    }
    else if(req.url === "/api/user") {
    const user = {
      userId: "apple",
      name: "김사과",
      age: 20
    }
    res.writeHead(200, {"Content-Type": "application/json"})
    res.end(JSON.stringify(user))
  }
  else{
        res.writeHead(404, {"Content-Type": "text/html"})
        res.end("<h2>error 🤢</h2>")
    }
})

server.listen(3000, () => {
    console.log("서버 실행 중..!!!")
})