const express = require("express")
const fs = require("fs")
const path = require("path")

const app = express()
const PORT = 8091

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "view"))

app.use(express.urlencoded({ extended: true }))

// 게시물 저장
app.post("/posts", (req, res) => {
    const { title, content } = req.body
    const saveText = `
====================
제목: ${title}
내용: ${content}
작업일: ${new Date().toLocaleDateString()}
====================
`

    const filepath = path.join(__dirname, "data", "posts.txt")
    fs.appendFile(filepath, saveText, "utf8", (err) => {
      if(err) {
        console.log(err)
        return res.send("파일 저장 중 오류가 발생함!")
      }
      res.send("파일 저장 성공!")
    })
})

app.get("/posts", (req, res) => {
  const filepath = path.join(__dirname, "data", "posts.txt")
  const posts = fs.readFileSync(filepath, "utf-8")
  res.render("posts", {
    posts
  })
})

app.listen(PORT, () => {
  console.log("서버가 실행되었습니다.")
})