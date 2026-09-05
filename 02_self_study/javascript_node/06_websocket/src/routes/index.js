import express from "express"
import { socketList } from "../sockets/index.js"

const router = express.Router()

// 요청이 많지 않으니까 그냥 직접 받아주기

router.get("/socketHist", (req, res) => {
  console.log("/socketHist 요청 들어옴.")
  res.send(JSON.stringify(socketList))
})

export default router