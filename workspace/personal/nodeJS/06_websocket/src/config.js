import dotenv from "dotenv"
import { fileURLToPath } from "url"
import path from "path"

dotenv.config()

const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)
const __viewpath = path.join(__dirname, "resources")

function required(key, defaultValue=undefined) {
  // process.env[key]가 존재하지 않으면 defaultValue로 만들어주기
  const value = process.env[key] ?? defaultValue
  if(!value) {
    throw new Error(`${key}가 존재하지 않습니다!`)
  }
  return value
}

const config = {
  host: {
    port: parseInt(required("PORT")),
    resources: __viewpath
  }
}

export default config