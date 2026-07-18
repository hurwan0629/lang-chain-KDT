import express from "express"
import type {Express} from "express"
import cors from "cors"
import cookieParaser from "cookie-parser"

export default function registerApplicationMiddleware(app: Express): void {
  app.use(cors({
      origin: ["https://localhost:5173", "https://127.0.0.1:5173"]
  }))

  app.use(express.urlencoded())
  app.use(express.json())
  app.use(cookieParaser())
  
  console.log("[registerApplicationMiddleware] 미들웨어 등록 완료")
}