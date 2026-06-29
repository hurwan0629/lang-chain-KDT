const express = require("express")
const path = require("path")
const morgan = require("morgan")
const fs = require("fs")
const cookieParser = require("cookie-parser")

const currTime = require("./utils/time")
const { selectAllUsers, addUser, getUserDataByCode, getUserDataByUserId } = require("./repository/users")
const { selectAllDatas, addLog } = require("./repository/regist_log")

const app = express()

//////////// [ 서버 설정 ] ////////////

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "views"))
app.use("/resources", express.static(path.join(__dirname, "resources")))

//////////// [ 미들 웨어 - 요청 디코딩 ] ////////////

app.use(express.json())
app.use(express.urlencoded())
app.use(cookieParser())

//////////// [ 미들 웨어 - 로깅 ] ////////////

morgan.token("kdt-time", (req, res) => {
  return currTime()
})

app.use(morgan("[:kdt-time] [morgan] :method :url :status :response-time ms - :res[content-length]", { immediate: true }))
app.use(morgan("[:kdt-time] [morgan] :method :url :status :response-time ms - :res[content-length]"))

//////////// [ 미들 웨어 - 회원 상태 확인 (로그인 쿠키) ] ////////////

app.use("/", (req, res, next) => {
  // 쿠키 있는지 확인
  const cookieUserCode = req.cookies?.userCode

  req.user = null

  if(!!cookieUserCode) {
    const user = getUserDataByCode(cookieUserCode)
    if(!!user) {
      req.user = user
    }
  }
  next()
})

app.get("/favicon.ico", (req, res) => {
  res.sendFile(path.join(__dirname, "resources", "dog.png"))
})

app.get("/", (req, res) => {
  const rows = selectAllDatas().reverse()

  console.log("rows:", rows)


  res.render("index", {
    rows,
    loggedIn: !!req.user,
    userName: req.user?.userName
  })
})

app.get("/regist", (req, res) => {

  // 로그인 가능성이 있으면
  if(!!req.user) {
    res.redirect("/")
    return
  }
  res.render("regist")
})

app.get("/login", (req, res) => {
  // 로그인 되어있다면
  if(!!req.user) {
    return res.redirect("/")
  }
  res.render("login")
})

app.get("/logout", (req, res) => {
  if(!!req.user) {
    res.cookie("userCode", {
      httpOnly: true,
      sameSite: "lax",
      maxAge: 0
    }).redirect("/")
    return
  }
  res.redirect("/")

})

app.post("/login", (req, res) => {
  const { id, password } = req.body
  console.log("id:",id)
  console.log("password:", password)

  // id/password 없으면 실해
  if(!id || !password) {
    res.status(401).json({
      "message": "아이디와 비밀번호를 입력해주세요"
    })
    return
  }

  const userData = getUserDataByUserId(id)
  console.log("userData:", userData)
  
  // id가 존재하지 않으면
  if(!userData) {
    res.status(401).json({
      "message": "아이디 또는 비밀번호가 틀렸습니다."
    })
    return
  }

  // id가 존재하면 password와 대조하기
  if(userData?.password !== password) {
    res.status(401).json({
      "message": "아이디 또는 비밀번호가 틀렸습니다."
    })
    return
  }

  res.cookie("userCode", userData.userCode, {
    httpOnly: true,
    sameSite: "lax",
    maxAge: 1 * 60 * 1000 // 1분
  })
  res.status(200).json({
    "message": "로그인 성공"
  })
})

app.post("/regist", (req, res) => {
  const { content } = req.body

  // 로그인 되어있는지 확인
  if(!req.user) {
    // unauthorized
    res.status(401).json({
      message: "글을 작성하려면 로그인 하세요"
    })
    return
  }

  const name = req.user.userName
  if(addLog({ 
    logTime: currTime(), 
    name: name, 
    content: content })) {
    res.status(200).json({
      message: "변경 성공"
    })
    return
  }
  res.status(400).json({
    message: "작성 실패"
  })

})

// 사용자 회원가입
app.put("/user", (req, res) => {
  const { id, name, password } = req.body
  
  // 아이디 중첩은 409
  if(getUserDataByUserId(id)) {
    res.status(409).json({
      "message": "중복된 아이디"
    })
    return
  }

  const userCode = addUser({
    userName: name,
    userId: id,
    password: password
  })

  // 추가해주기
  if (!!userCode) {
    // 성공하면 ok
    return res.status(201).json({
      "message": "회원가입 성공",
      userCode
    })
  }

  // 실패하면 400
  return res.status(400).json({
    message: "회원 생성에 실패하였습니다."
  })
})

app.listen(8090, () => {
  console.log("서버 시작")
})