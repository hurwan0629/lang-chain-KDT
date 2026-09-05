// 사용자 정보 조회가 필요한 경우의 라우터

import { Router } from "express";

import * as UserController from "../../controller/users.controller.js"

const router = Router()

// 아이디 중복 확인용
router.get("/idDuplicated", UserController.handleIdDuplicated)

// 최종 회원가입 요청
router.post("/signup", UserController.handleUserSignup)

export default router