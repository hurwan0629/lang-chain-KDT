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

    API 주소(URL) 구성 원칙
    - API주소는 단순한 경로가 아니라 리소스를 표현하는 구조적인 설계 요소
    - RESTful 설계 원칙에 따라 구성하는 것이 가장 일반적

    RESTful(Representational State Transfer)
    url과 http 메서드를 이용해 자원을 직관적이고 일관성 있게 설계하는 웹 api방식

    /api/버전/리소스
    - api : API임을 명시
    - v1 : 버전 관리
    - users : 리소스(자원), 명사로 작성

    HTTP 메서드
    GET: 조회
    POST: 생성
    PUT: 수정
    DELETE: 삭제

*/

const express = require("express")
const app = express()

app.use(express.json())

// 생성
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

// 조회
app.get("/user/:id", (req, res) => {
    res.json({ id: req.params.id, message: "사용자 조회" })
})

app.listen(3000, () => {
    console.log("서버 실행 중...")
})

// 전체 수정
app.put("/user/:id", (req, res) => {
    const { name, age } = req.body
    if(!name || !age){
        return res.status(400).json({ error: "필수값 누락!"})
    }
    res.json({ message: "전체 수정 완료", id: req.params.id, data: { name, age }})
})

// 부분 수정
app.patch("/user/:id", (req, res) => {
    const updates = req.body
    if(Object.keys(updates).length === 0) {
        return res.status(400).json({ error: "수정할 데이터가 없습니다."})
    }
    res.json({ message: "부분 수정 완료", id: req.params.id, updateData: updates })
})

// 삭제
app.delete("/user/:id", (req, res) => {
    res.json({ message: "삭제 완료", id: req.params.id })
})

app.listen(3000, () => {
    console.log("서버 실행 중...")
})