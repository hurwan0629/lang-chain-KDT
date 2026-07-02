import express from "express"
import * as UserController from "../../controller/users.controller.mjs"

// /api/users/...

const router = express.Router()

// 로그인
router.post("/login", (req, res) => {
  UserController.login(req, res)
})

// 회원가입
router.post("/signup", (req, res) => {
  UserController.signup(req, res)
})

// 로그아웃
router.post("/logout", () => {
  console.log("로그아웃")
})

// 회원 탈퇴
router.delete("/", () => {
  console.log("회원 탈퇴")
})

// 로그인 체크
router.get("/me", () => {
  console.log("로그인 체크")
})



export default router