const express = require("express")


const app = express()


app.get("/", (req, res) => {
  res.send("Hello Node.js")
})

app.get("/bye", (req, res) => {
  res.header()
  res.json([
    { id: 1, name: "kim" },
    { id: 2, name: "lee" },
  ])
})

app.listen(8090, "127.0.0.1", () => {
  console.log("서버 실행중://127.0.0.1:8090")
})