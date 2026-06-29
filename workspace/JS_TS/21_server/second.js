/*
    Express에서 JSON 데이터를 처리하는 흐름

    클라이언트(요청) -> Express 서버 -> JSON 파싱 -> req.body로 접근 -> 로직 처리 -> JSON 응답

    1. 미들웨어 등록
        app.use(express.json())


    {
        "name": "김사과",
        "age": 20
    }

    2. post로 json 데이터 받기
        app.post("/user", (req, res) => {
            const { name, age } = req.body
        })

    3. json 응답 보내는 방법
        res.json({ success: true })

        { "success": true }
        > 자동으로 Content-Type: application/json 설정
        > 자바스크립트 객체를 보내면 자동으로 JSON 변환

    4. 유효성 검사
        app.post("/user", (req, res) => {
            const { name, age } = req.body
            if(!name || !age) {
                return res.status(400).json({
                    error: "name 또는 age는 필수"
                })
            }
        })
*/

const express = require("express")
const app = express()

app.use(express.json())

app.post("/user", (req, res) => {
    const { name, age } = req.body
    if(!name || !age){
        return res.status(400).json({ error: "필수값 누락!"})
    }
    res.status(201).json({
        message: "등록 완료",
        data: {name, age}
    })
})

app.listen(3000, () => {
    console.log("서버 실행 중...")
})