import express from "express"
import registerApplicationMiddleware from "./middleware.ts"
import router from "../router/index.ts"

const app = express()

registerApplicationMiddleware(app)

app.use("/api", router)

export default app