import Router from "express"

import UserRouter from "./userRouter.ts"
import RoomRouter from "./roomRouter.ts"
import TestRouter from "./testRouter.ts"


const router = Router()

router.use("/users", UserRouter)

router.use("/rooms", RoomRouter)

router.use("/test", TestRouter)

export default router