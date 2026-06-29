const express = require("express")
const path = require("path")
const morgan = require("morgan")
const app = express()

app.use(express.json())
// app.use(express.urlencoded({ extended: true }))

app.use(morgan("dev", { immediate: true}))
app.use(morgan("dev"))


app.get("/", (req, res) => {
  console.log(" url: ", req.url)
  console.log(" method: ", req.method)
  console.log(" host: ", req.host)
  console.log(" hostname: ", req.hostname)

  res.sendFile(path.join(__dirname, "resources", "views", "index.html"))
})

app.post("/urlencoded", (req, res) => {
  console.log("req.headers:", req.headers)
  console.log("content-type:",req.headers["content-type"])
  let body = ""
  req.on("data", (data) => {
    body += data.toString("utf8")
    console.log("  data:", data.toString())
  })

  req.on("end", () => {
    console.log("  [end] body:", body)
    body = decodeURIComponent(body)
    console.log("  [decode] body:", body)
  })

  res.status(200).json({
    message: "hello!"
  })
})

app.listen(8090, () => {
  console.log("서버 실행")
})