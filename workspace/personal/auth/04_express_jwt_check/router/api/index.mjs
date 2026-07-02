import express from "express"

import ItemRouter from "./items.mjs"
import OrderRouter from "./orders.mjs"
import UserRouter from "./users.mjs"

const router = express.Router()

router.use("/items", ItemRouter)

router.use("/orders", OrderRouter)

router.use("/users", UserRouter)

export default router