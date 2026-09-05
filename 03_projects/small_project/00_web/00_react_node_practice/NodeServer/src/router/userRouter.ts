import Router from "express"

// /api/users/
const router = Router()

// 전체 사용자 정보 제공
router.get("/", (req, res) => {
  console.log("[/api/users] get")
  res.json({ message: "hello" })
})

export default router