// ./app.js의 미들웨어 설정용

import cors from "cors"
import morgan from "morgan"
import express from "express"
import cookieParser from "cookie-parser"
import { currTime } from "../utils/date.js"
import { corsOptions } from "../config/cors.js"

export default function registerApplicationMiddleware(app) {

  app.use(cors(corsOptions))

  app.use(express.json())
  app.use(express.urlencoded())
  app.use(cookieParser())


  // morgan 나갈때 로깅
  morgan.token("currTime", (req, res) => {
    return currTime()
  })
  app.use(morgan(`[:currTime] [morgan] method\::method url\::url status\::status response-time\::response-time remote-addr\::remote-addr `))
}