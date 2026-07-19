// 사용하는 데이터베이스 드라이버 설정하기 및 connection (아마 Pool 로 기억하고 있음)

import { Pool } from "pg"
import config from "./env.js"
import logger from "../utils/logger.js"

const pool = new Pool({
  host: config.db.host,
  port: config.db.port,
  database: config.db.database,
  user: config.db.user,
  password: config.db.password,
  max: 10
})

export default pool