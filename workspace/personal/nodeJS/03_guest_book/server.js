const express = require("express")
const path = require("path")
const morgan = require("morgan")
const fs = require("fs")
const currTime = require("./utils/time")

const { name } = require("ejs")

const app = express()

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "views"))
app.use("/resources", express.static(path.join(__dirname, "resources")))


app.use(express.json())
app.use(express.urlencoded())

morgan.token("kdt-time", (req, res) => {
  return currTime()
})

app.use(morgan("[:kdt-time] :method :url :status :response-time ms - :res[content-length]"))

app.get("/favicon.ico", (req, res) => {
  res.sendFile(path.join(__dirname, "resources", "dog.png"))
})

app.get("/", (req, res) => {

  if(!fs.existsSync(path.join(__dirname, "datas"))) {
    console.log("1")
    fs.mkdirSync(path.join(__dirname, "datas"), { recursive: true })
  }
  if(!fs.existsSync(path.join(__dirname, "datas", "registLog.csv"))) {
    console.log("2")
    fs.writeFileSync(path.join(__dirname, "datas", "registLog.csv"), "")
  }
  datas = fs.readFileSync(path.join(__dirname, "datas", "registLog.csv"), "utf-8")


  let rows = []

  if(datas.trim()) {
    rows = datas.trim().split(/\r?\n/).map((line) => {
      const data = line.split(",")
      return {
        logTime: data[0],
        name:data[1],
        content: data[2]
      }
    })
    console.log(rows)
  }

  res.render("index", {
    rows
  })
})

app.post("/regist", (req, res) => {


  const name = req.body.name
  const content = req.body.content
  const now = currTime()
  const contentToWrite = [now, name, content].join(",") + "\n"
  console.log(contentToWrite)
  fs.appendFileSync(path.join(__dirname, "datas", "registLog.csv"), contentToWrite, "utf-8")
  res.status(200).json({
    message: "변경 성공"
  })
})

app.listen(8090, () => {
  console.log("서버 시작")
})