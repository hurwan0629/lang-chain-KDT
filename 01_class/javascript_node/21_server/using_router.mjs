import express from "express"
import userRouter from "./routes/user.mjs"
import postRouter from "./routes/post.mjs"

const app = express()
app.use(express.json())

app.use("/user", userRouter)
app.use("/post", postRouter)

app.listen(8081, () => {
  console.log("서버 실행 중...")
})