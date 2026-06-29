const express = require("express")
const fs = require("fs")
const path = require("path")

const app = express()
const PORT = 3000

app.set("view engine", "ejs")
app.set("views", path.join(__dirname, "view"))

app.use(express.urlencoded({ extended: true }))
const filePath = path.join(__dirname, "data", "posts.txt")

// 게시물 저장
app.post("/posts", (req, res) => {
    const { title, content } = req.body
    const saveText = `
    ===================
    제목: ${title}
    내용: ${content}
    작성일: ${new Date().toLocaleString()}
    ===================
    `

    fs.appendFile(filePath, saveText, "utf8", (err) => {
        if(err) {
            console.error(err)
            return res.send("파일 저장 중 오류가 발생함!")
        }
        res.send("파일 저장 성공!")
    })
})

// 게시물 리스트
app.get("/posts", (req, res) => {
    fs.readFile(filePath, "utf8", (err, data) => {
        if(err) {
            console.error(err)
            return res.render("posts", {posts: "아직 저장된 게시물이 없습니다."})
        }
        res.render("posts", {posts: data})
    })
})

app.listen(PORT, () => {
    console.log("서버 실행 중...")
})