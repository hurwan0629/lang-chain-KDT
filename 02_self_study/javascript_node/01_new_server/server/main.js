main = function() {
  const express = require("express");
  const path = require("path")

  const app = express();

  // 설정 끄기
  // x-powered-by는 헤더에 X-Powered-By: Express를 적을 수 있어서 서버 기술 노출을 줄이기 위해 비활성화할 수 있습니다.
  app.disable("x-powered-by")

  // 미들웨어 등록
  // app.use를 통해 미들웨어를 등록하는데 
  
  // express.json()은 요청 body가 JSON일 때 자동으로 JS 객체로 
  // 파싱해주는 미들웨어입니다.
  // 헤더의 `Content-Type`가 `application/json` 일때만 해석합니다.
  app.use(express.json())

  // express.urlencoded()는 인코딩된 데이터를 읽어주는 설정입니다.
  // `id=abc&pw=1234` 와 같은 데이터를 
  // { id: "abc", pw: "1234" } (일반객체)형태로 바꿔줍니다.
  // extended는 `user[name]=kim&user[age]=20` 같은 복잡한 구조도 처리해줍니다.
  app.use(express.urlencoded({ extended: true }));

  // 미들웨어는 인터셉터보다 필터에 가까운 위치이며 req를 처리하기 전 또는 res를 처리한 후 작업할 내용을 의미합니다.
  // 인자는 기본적으로 [콜백(요청, 응답, 진행콜백)]을 받으며 1번 인자를 "경로"로 설정함으로 써 특정 경로에만 다른 라우터를 적용 가능합니다.
  app.use((req, res, next) => {
    console.log("1번 use")
    console.log(req.method);
    console.log(req.url)
    next()
  })

  app.use("/hello", (req, res, next) => {
    console.log("2번 use")
    if(req.path === "/") {
      console.log(req.path)
      console.log("/hello 요청은 응답하지 않습니다.")
      return
    }
    next()
  })

  app.use("/hello/*left", (req, res, next) => {
    console.log("3번 use")
    console.log("/hello/* 요청은 응답해줍니다.")
    console.log(`하위 경로: ${req.params.left}`)
    console.log(`param값: ${req.query.param}`)
    next()
  })

  // 첫번째 인자로 지정되어있는 경로로 시작하는 요청이 오면 뒤의 express.static(경로)
  // 에 존재하는 나머지 경로의 위치를 그대로 파일로 반환해줍니다. 
  // 해당 폴더에 파일이 존재하지 않으면 index.html을 "서버"가 반환해줍니다.
  app.use("/resources", express.static(path.join(__dirname, "/resources")))

  // app.set
  // express 내부에 앱 전체에서 공유하는 설정 저장소의 요소를 설정하는 문법
  // {
  //    "view engine": "ejs"
  // }
  // 느낌으로 저장
  app.set("view engine", "ejs");
  app.set("views", path.join(__dirname, "views"))

  // app.get
  // app.get는 2가지 의미가 있습니다.
  // 1번: 설정값 조회
  // 2번: GET 요청 처리
  app.get("/", (req, res) => {
    console.log("루트 요청")
    const viewEngine = app.get("views")
    res.send(`${viewEngine}`);
  })

  app.get("/ejs", (req, res) => {
    console.log(`\n --- /ejs 요청 들어옴 --- \n`)
    console.log(`ejs/ 이후 경로: ${req.params.files}`)
    console.log(!!req.params.file)
    if(!req.params.file) {
      res.render("index", {
        "name": "이름",
        "age": "20",
      })
    }
  })

  // app.route
  // 같은 경로의 다른 메서드를 관리할 때 쓰입니다.
  app.route("/users/:id")
  .get((req, res) => {
    res.send("사용자 조회")
  })
  .post((req, res) => {
    res.send("사용자 수정")
  })
  .delete((req, res) => {
    res.send("사용자 삭제")
  })

  // Node HTTP에는 2가지 주요 스트림 구조가 있습니다.
  // IncomingMessage: 
  function aboutFunc(req, res) {
    console.log(`\n --- /about --- \b`)
    // express가 구현에 이용한 저수준 파일은 Node.http입니다.
    // .req의타입은 Readable Stream으로 클라이언트가 보낸 데이터를 서버가 읽는 통로를 받은 것입니다.  
    // .req객체 내에 그 자체로 요청 데이터를 가지고 있지 않습니다.
    // body 한 chunk를 받을 때마다 호출되는 콜백입니다.
    req.on("data", (data) => {
      console.log(`데이터 받음: ${data}`)
    })
    // 데이터를 모두 불러온 뒤 항상 불려지는 콜백 등록입니다.
    req.on("end", () => {
      console.log(`데이터 모두 받음`)
      req.body = "hello"
    })
    // url, method, header은 미리 받아놓을 수 있습니다.
    console.log(req.method)
    console.log(req.url)
    console.log(req.headers.host)

    // req.body는 스트림을 모두 읽은 뒤 읽은 스트림 데이터를 모두 모아 저장해놓는 객체입니다.
    console.log("데이터: ",req.body)

    res.json({
      "message": "잘 받았습니다.",
      "data": "줄 데이터가 없네용"
    })
    res.set
  }

  app.route("/about")
    .get(aboutFunc)
    .post(aboutFunc)



  app.listen(8090, "127.0.0.1", () => {
    console.log("서버 실행 시작");
  })
}

module.exports = main
