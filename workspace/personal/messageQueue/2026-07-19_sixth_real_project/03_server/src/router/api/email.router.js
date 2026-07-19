import { Router } from "express";
import logger from "../../utils/logger.js";

const router = Router()

router.get("/admin", (req, res) => {
  logger("admin.router.js GET /admin", "hello")
})

export default router