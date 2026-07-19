// export defualt const config = {} 를 통해 dotenv 받아와서 export 해주기

import dotenv from "dotenv"

dotenv.config()

function required(key, defaultKey=undefined) {
  const value = process.env[key] ?? defaultKey

  if(!value) {
    throw new Error(`env key not exists: ${key}`)
  }
  return value
}

const config = {
  host: {
    port: parseInt(required("HOST_PORT", 8080)),
    address: required("HOST_ADDRESS", "127.0.0.1")
  },
  
  client: {
    protocol: required("CLIENT_PROTOCOL", "https"),
    port: parseInt(required("CLIENT_PORT", 5173)),
    address:required("CLIENT_ADDRESS", "localhost")
  },

  jwt: {
    secure: false,
    httpOnly: true,
    sameSite: "lax",

    accessSecret: required("JWT_ACCESS_SECRET", "64-byte-secret-key-64-byte-secret-key"),
    accessExpiredIn: required("JWT_ACCESS_EXPIRES_IN", "1h"),
    accessCookieMaxAge: parseInt(required("JWT_ACCESS_COOKIE_MAX_AGE", "3600000")),
    accessCookiePath: required("ACCESS_COOKIE_PATH", "/"),

    refreshSecret: required("JWT_ACCESS_SECRET", "64-byte-secret-key-64-byte-secret-key"),
    refreshExpiredIn: required("JWT_ACCESS_EXPIRES_IN", "1h"),
    refreshCookieMaxAge: parseInt(required("JWT_ACCESS_COOKIE_MAX_AGE", "3600000")),
    refreshCookiePath: required("REFRESH_COOKIE_PATH", "/auth/refresh"),
  },

  db: {
    host: required("DB_ADDRESS", "127.0.0.1"),
    port: parseInt(required("DB_PORT", 5432)),
    database: required("DB_NAME", "test_db"),
    user: required("DB_USER", "root"),
    password: required("DB_PASSWORD", "1234")
  }
}

export default config