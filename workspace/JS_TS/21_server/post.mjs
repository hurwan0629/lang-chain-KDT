import express from "express"

const app = express()
const router = express.Router()

router.get("/", (req, res) => {
  res.send("포스팅 조회")
})

router.patch("/", (req, res) => {
  res.send("포스팅 생성")
})

router.put("/:id", (req, res) => {
  const { id } = req.params
  res.send("포스팅 수정", id)
})

router.delete("/:id", (req, res) => {
  const { id } = req.params
  res.send("포스팅 삭제:", id)
})

export default router