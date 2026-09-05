import express from "express"

const router = express.Router()

router.get("/", (req, res) => {
  res.status(200).send("GET /users: 회원 정보 보기")
})


router.post("/", (req, res) => {
  res.status(201).send("POST /users: 회원가입")
})


router.put("/:id", (req, res) => {
  const { id } = req.params
  res.status(200).send(`PUT /users/${id} 정보 수정`)
})

router.delete("/:id", (req, res) => {
  const { id } = req.params
  res.status(200).send(`DELETE /users/${id} 회원탈퇴`)
})

export default router