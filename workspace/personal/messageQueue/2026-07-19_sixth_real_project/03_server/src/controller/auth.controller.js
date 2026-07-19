// auth.controller.js

import { ApiError } from "../utils/ApiError"
import * as AuthService from "../service/auth.service.js"
import * as JwtService from "../service/jwt.service.js"
import config from "../config/env.js";

// /api/auth/login
export async function handleLogin(req, res) {
  try {
    const { id, password } = req.body

    if(!id || !password) {
      throw new ApiError(400, "required value missing", {
        fields: ["id", "password"]
      })
    }

    const result = await AuthService.checkUserIdAndPasswordAvailable(id, password)

    if(result) {
      return res.status(200).json({
        success: true,
        message: "login success",
        data: {}
      })
    }
    else {
      return res.status(200).json({
        success: false,
        message: "login fail",
        data: {}
      })
    }
  } catch (error) {
    throw new ApiError(500, "server error", {})
  }
}

/**
 * refreshToken이 정상적으로 발견되면 accessToken을 만들어주는 컨트롤러
 * @param req
 * @param res
 */
export async function refreshToken(req, res) {
  // 1. refreshToken이 존재하는지 확인하기
  const { refreshToken } = req.cookies

  if (!refreshToken) {
    throw new ApiError(401, "no refresh token", {})
  }

  // 2. refreshToken에서 사용자 정보 확인하기
  try {
    const { pk, role } = JwtService.verityRefreshToken(refreshToken)

    // 3. 원래는 db에서 정보 뽑아서 access 만들어도 되지만 문제 없기때문에 그대로 반환
    res.cookie(
        "accessToken",
        JwtService.createAccessToken({ pk, role }),
        {
          path: config.jwt.accessCookiePath,
          sameSite: config.jwt.sameSite,
          maxAge: config.jwt.accessCookieMaxAge,
          secure: config.jwt.secure
        }
    )
  } catch (error) {
    throw new ApiError(401, "invalid token", {})
  }

  return res.status(200).json({
    success: true,
    message: "accessToken issued",
    data: {}
  })
}
export function provideMe(req, res) {
  
}
export function handleLogout(req, res) {
  
}