// express 생성 및 등록 + 라우팅 설정 (index.js)

import express from "express"
import registerApplicationMiddleware from "./middleware.js"
import apiRouter from "../router/api/index.js"
import { errorHandler } from "../auth/error.middleware.js"

const app = express()

// 미들웨어 등록
registerApplicationMiddleware(app)

// 라우터 등록
app.use("/api", apiRouter)

// 에러 핸들러 등록
app.use(errorHandler)

export default app