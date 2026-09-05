import jwt from "jsonwebtoken"
import config from "../config/env.js"


export function createAccessToken({ pk, role }) {
  return jwt.sign({ 
    pk, role 
  }, 
  config.jwt.accessSecret, 
  { expiresIn: config.jwt.accessExpiredIn })
}

export function createRefreshtoken({ pk, role }) {
  return jwt.sign({
    pk, role
  },
  config.jwt.refreshSecret,
  { expiresIn: config.jwt.refreshExpiredIn })
}

export function createAuthTokens({ pk, role }) {
  return {
    accessToken: createAccessToken({ pk, role }),
    refreshToken: createRefreshtoken({ pk, role })
  }
}

export function verifyAccessToken(accessToken) {
  return jwt.verify(accessToken, config.jwt.accessSecret)
}

export function verityRefreshToken(refreshToken) {
  return jwt.verify(refreshToken, config.jwt.refreshSecret)
}