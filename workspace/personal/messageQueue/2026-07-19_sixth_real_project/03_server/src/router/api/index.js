// api의 경우 모든 라우팅을 받기 위한 index.js 라우터

import { Router } from "express";
import UserRouter from "./users.router.js"
import AdminRouter from "./admin.router.js"
import ItemRouter from "./items.router.js"
import OrderRouter from "./orders.router.js"
import PaymentRouter from "./payments.router.js"
import AuthRouter from "./auth.router.js"
import EmailRouter from "./email.router.js"

const apiRouter = Router()


apiRouter.use("/users", UserRouter)
apiRouter.use("/auth", AuthRouter)
apiRouter.use("/email", EmailRouter)
apiRouter.use("/admin", AdminRouter)
apiRouter.use("/items", ItemRouter)
apiRouter.use("/orders", OrderRouter)
apiRouter.use("/payments", PaymentRouter)

export default apiRouter