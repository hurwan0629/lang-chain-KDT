const express = require("express")
const path = require("path")
const morgan = require("morgan")
const fs = require("fs")
const cookieParser = require("cookie-parser")

const currTime = require("./utils/time")

const { name } = require("ejs")

const app = express()

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "views"))
app.use("/resources", express.static(path.join(__dirname, "resources")))


app.use(express.json())
app.use(express.urlencoded())
app.use(cookieParser())

morgan.token("kdt-time", (req, res) => {
  return currTime()
})

app.use(morgan("[:kdt-time] :method :url :status :response-time ms - :res[content-length]"))

app.get("/favicon.ico", (req, res) => {
  res.sendFile(path.join(__dirname, "resources", "dog.png"))
})

app.get("/", (req, res) => {
  // /datas 폴더 확인
  if(!fs.existsSync(path.join(__dirname, "datas"))) {
    fs.mkdirSync(path.join(__dirname, "datas"), { recursive: true })
  }

  // /datas/registLog.csv 파일 만들기
  if(!fs.existsSync(path.join(__dirname, "datas", "registLog.csv"))) {
    fs.writeFileSync(path.join(__dirname, "datas", "registLog.csv"), "")
  }
  datas = fs.readFileSync(path.join(__dirname, "datas", "registLog.csv"), "utf-8")


  let rows = []

  if(datas.trim()) {
    rows = datas.trim().split(/\r?\n/).map((line) => {
      const data = line.split(",")
      return {
        logTime: data[0],
        name: data[1],
        content: data[2]
      }
    })
    console.log(rows)
  }

  res.render("index", {
    rows
  })
})

app.get("/regist", (req, res) => {
  const cookieUserCode = req.cookies?.userCode
  console.log(typeof(cookieUserCode))
  // 로그인 가능성이 있으면
  if(cookieUserCode) {
    if(!fs.existsSync(path.join(__dirname, "datas", "users.json"))) {
      fs.writeFileSync(path.join(__dirname, "datas", "users.json"), "[]")
    }
    // 중복하는 code가 존재하면 "/"로 리다이렉트 해주기
    if(JSON.parse(fs.readFileSync(path.join(__dirname, "datas", "users.json"), "utf-8")).some(({ userCode }) => String(userCode) === cookieUserCode)) {
      console.log("GET /regits 리다이렉트")
      res.redirect("/")
      return
    }
  }
  res.render("regist")
})

app.get("/login", (req, res) => {
  console.log("로그인 페이지 요청")
  const cookieUserCode = req.cookies?.userCode
  console.log(req.cookies)
  // userCode가 없으면 확실히 로그인 안한 상태
  if(!cookieUserCode) {
    // unauthorized
    res.render("login")
    return
  }

  // 사용자 이름 뽑기af
  if(!fs.existsSync(path.join(__dirname, "datas", "users.json"))) {
    fs.writeFileSync(path.join(__dirname, "datas", "users.json"), "[]")
  }
  
  // 사용자 userCode 목록에 있는지 확인
  let userData = JSON.parse(fs.readFileSync(path.join(__dirname, "datas", "users.json"), "utf-8")).find(({ userCode }) => String(userCode) === cookieUserCode)
  
  // 이미 로그인 되어있으면 해당 페이지 주지 않기
  console.log("userData:", userData)
  if(userData) {
    console.log("이미 로그인 되어있는 회원")
    return res.redirect("/")
  }
  res.render("login")
})

app.post("/login", (req, res) => {
  const { id, password } = req.body
  console.log(id, password)

  // id/password 없으면 실해
  if(!id || !password) {
    res.status(401).json({
      "message": "아이디와 비밀번호를 입력해주세요"
    })
    return
  }

  // 사용자 id있으면 userData에 넣어주기
  if(!fs.existsSync(path.join(__dirname, "datas", "users.json"))) {
    fs.writeFileSync(path.join(__dirname, "datas", "users.json"), "[]")
  }
  let userData = JSON.parse(fs.readFileSync(path.join(__dirname, "datas", "users.json"), "utf-8")).find(({ userId }) => String(userId) === id)
  console.log(userData)
  
  // id가 존재하지 않으면
  if(!userData) {
    res.status(401).json({
      "message": "아이디 또는 비밀번호가 틀렸습니다."
    })
    return
  }

  // id가 존재하면 password와 대조하기
  if(userData.password !== password) {
    res.status(401)
    return
  }

  res.cookie("userCode", userData.userCode, {
    httpOnly: true,
    sameSite: "lax",
    maxAge: 30 * 1000 // 30초
  })
  res.status(200).json({
    "message": "로그인 성공"
  })
})

app.post("/regist", (req, res) => {
  // 로그인 되어있는지 확인
  const cookieUserCode = req.cookies?.userCode
  if(!cookieUserCode) {
    // unauthorized
    res.status(401).json({
      message: "글을 작성하려면 로그인 하세요"
    })
    return
  }

  // 사용자 이름 뽑기af
  if(!fs.existsSync(path.join(__dirname, "datas", "users.json"))) {
    fs.writeFileSync(path.join(__dirname, "datas", "users.json"), "[]")
  }
  let userData = JSON.parse(fs.readFileSync(path.join(__dirname, "datas", "users.json"), "utf-8")).find(({ userCode }) => String(userCode) === cookieUserCode)
  const name = userData.userName

  // const name = req.body.name
  const content = req.body.content
  const now = currTime()
  const contentToWrite = [now, name, content].join(",") + "\n"
  console.log(contentToWrite)
  fs.appendFileSync(path.join(__dirname, "datas", "registLog.csv"), contentToWrite, "utf-8")
  res.status(200).json({
    message: "변경 성공"
  })
})

app.put("/user", (req, res) => {
  console.log(req.cookies)
  console.log(req.body)
  const { id, name, password } = req.body
  
  // 아이디 중첩은 409
  if(!fs.existsSync(path.join(__dirname, "datas", "users.json"))) {
    fs.writeFileSync(path.join(__dirname, "datas", "users.json"), "[]")
  }
  let userData = JSON.parse(fs.readFileSync(path.join(__dirname, "datas", "users.json"), "utf-8"))
  
  if(userData.some(({ userId }) => userId === id)) {
    res.status(409).json({
      "message": "중복된 아이디"
    })
    return
  }

  // 추가해주기
  const userCode = userData.length === 0 
                  ? 1
                  : Math.max(...userData.map((user) => user.userCode))+1
  userData.push({
    userCode,
    userId: id,
    userName: name,
    password
  })

  fs.writeFileSync(
    path.join(__dirname, "datas", "users.json"),
    JSON.stringify(userData, null, 2),
    "utf-8"
  )
  

  // 성공하면 ok
  return res.status(201).json({
    "message": "회원가입 성공",
    userCode
  })
  // 실패하면 400
})

app.listen(8090, () => {
  console.log("서버 시작")
})