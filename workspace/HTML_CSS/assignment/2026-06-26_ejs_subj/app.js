const express = require("express")
const path = require("path")
const app = express()
const port = 8090

// 미들웨어
app.use("/resources", express.static("resources"))

//EJS
app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "view"))

app.use(express.urlencoded({ extended: true}))

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "resources", "index.html"))
})


app.get("/hello", (req, res) => {
  res.render("hello", {
    name: "허완"
  })
})

app.get("/teacher", (req, res) => {
  res.sendFile(path.join(__dirname, "resources", "teacher.html"))
})

app.post("/submit", (req, res) => {
  console.log("/submit")
  res.header("Content-Type", "applicaion/json")
  res.header("Access-Control-Allow-Origin", "*")
  res.header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
  res.send({
    message: "/submit 잘 송신받았습니다."
  })
})


app.post("/get-info", (req, res) => {
  const { name, age } = req.body
  console.log("name: ", name)
  console.log("age: ", age)
  res.send("post로 호출!")
})

app.listen(port, () => {
  console.log("서버 실행")
})