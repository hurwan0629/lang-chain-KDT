import { Router } from "express";
import logger from "../../utils/logger.js";
import * as AuthController from "../../controller/auth.controller.js"
import { checkAccessToken } from "../../auth/auth.middleware.js"

const router = Router()

router.post("/login", AuthController.handleLogin)

router.post("/refresh", AuthController.refreshToken)

router.get("/me", checkAccessToken , AuthController.provideMe)

router.post("/logout", AuthController.handleLogout)

export default router