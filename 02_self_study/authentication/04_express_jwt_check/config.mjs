import dotenv from "dotenv"

dotenv.config()

function required(key, defaultValue=undefined){
  const value = process.env[key] || defaultValue

  // undefined 또는 null 만 처리
  if(value == null) {
    throw new Error(`${key}의 값이 존재하지 않습니다.`)
  }
  return value
}

export const config = {
  jwt: {
    secretKey: required("JWT_SECRET"),
    expiresInSec: parseInt(required("JWT_EXPIRES_SEC"))
  },
  bcrypt: {
    saltRounds: parseInt(required("BCRYPT_ROUNDS"))
  },
  host: {
    port: required("SERVER_PORT", 8091),
    listen_host: required("LISTEN_HOST", "127.0.0.1")
  },
  db: {
    host: required("DATABASE_URL"),
    databaseName: required("DATABASE_NAME")
  }
}