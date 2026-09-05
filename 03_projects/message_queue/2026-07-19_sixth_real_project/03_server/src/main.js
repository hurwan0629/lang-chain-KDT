// 최초 및 최종적으로 실행될 스크립트

// app 생성 및 등록하기
// app.listen 실행하기

import app from "./app/app.js";
import config from "./config/env.js";
import logger from "./utils/logger.js";
import {closeRedis, connectRedis} from "./config/redis.js";
import pool, {closePgPool} from "./config/db.js";

await connectRedis()

async function closeResources() {
  await closeRedis()
  await closePgPool()
}



process.on("SIGINT", async () => {
  await closeResources()
  process.exit(0)
})

process.on("SIGTERM", async () => {
  await closeResources()
  process.exit(0)
})


app.listen(config.host.port, config.host.address, () => {
  logger("main.js", 
    `server active... [${config.host.address}:${config.host.port}]`
  )
})