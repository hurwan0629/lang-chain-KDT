import { createClient } from "redis"
import config from "./env.js";
import logger from "../utils/logger.js";


const redis = createClient({
    socket: {
        host: config.redis.host,
        port: config.redis.port,
    },
    password: config.redis.password
})

redis.on("error", (error) => {
    logger("/config/redis.js",
        `error: ${error.message}`)
    console.log(error)
})

export async function connectRedis() {
    if(!redis.isOpen) {
        await redis.connect()
        logger("/config/redis.js connectRedis", "redis connected")
    }
}

export async function closeRedis() {
    if(redis.isOpen) {
        await redis.quit()
        logger("/config/redis.js closeRedis", "redis disconnect")
    }
}

export default redis