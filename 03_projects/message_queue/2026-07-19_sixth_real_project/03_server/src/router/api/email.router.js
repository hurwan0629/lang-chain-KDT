import { Router } from "express";
import * as EmailController from "../../controller/email.controller.js"

const router = Router()

// /api/email/*

router.post("/send", EmailController.sendEmailVerifyCode)

router.post("/check", EmailController.checkEmailVerifyCode)

export default router