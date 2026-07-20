// auth.controller.js

import { ApiError } from "../utils/ApiError"
import * as AuthService from "../service/auth.service.js"
import * as UserService from "../service/users.service.js"
import * as JwtService from "../service/jwt.service.js"
import config from "../config/env.js";
import logger from "../utils/logger.js";
import {accessCookieOptions, refreshCookieOptions} from "../config/jwt.js";

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
      // 성공하면 accessToken/refreshToken 만들어주기
      const user = await UserService.getUserByUserId(id)

      res.cookie(
          "accessToken",
          JwtService.createAccessToken({ pk: user.pk, role: user.role }),
          accessCookieOptions
      )

      res.cookie(
          "refreshToken",
          JwtService.createRefreshtoken({ pk: user.pk, role: user.role }),
          refreshCookieOptions
      )

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
        accessCookieOptions
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

/**
 * accessToken으로부터 users.pk 를 꺼내어 사용자쪽으로 json 형태로 응댑해주는 컨트롤러
 * @param req
 * @param res
 */
export async function provideMe(req, res) {
  try{
    // 1. 이미 checkAccessToken에서 req.user.id, req.user.role을 넣어줬음
    const { id, role } = req.user

    if(!id || !role) {
      throw new ApiError(401, "no access token", {})
    }


    const user = await UserService.getUserByUserId(id)

    if(!user) {
      throw new ApiError(401, "invalid user", {})
    }

    const {
      pk,
      name,
      address,
      createdAt,
    } = user

    return res.send(200).json({
      success: true,
      message: "user exists",
      data: {
        pk,
        id,
        name,
        address,
        createdAt,
      }
    })

  } catch (error) {
    logger("/controller/auth.controller.js provideMe", `error: ${error.message}`)
    throw error
  }
}

/**
 * 그냥 토큰 2개 덮어씌워줘 버리기
 * @param req
 * @param res
 */
export function handleLogout(req, res) {
  res.cookie(
      "accessToken",
      "",
      accessCookieOptions
  )
  res.cookie(
      "refreshToken",
      "",
      refreshCookieOptions
  )
}