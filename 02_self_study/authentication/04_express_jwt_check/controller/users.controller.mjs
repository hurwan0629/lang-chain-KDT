// users.controller.mjs
import * as UserRepository from "../repository/users.repository.mjs"
import * as ApiResponse from "../response/api.users.response.mjs"

import { config } from "../config.mjs"

import bcrypt from "bcrypt"
import jwt from "jsonwebtoken"

// 로그인
export async function login(req, res) {
  // 사용자에게 id, password 받아서 cookie token 발급해주기
console.log(req.body)
  const { userId, userPassword } = Object.fromEntries(
    Object.entries(req?.body ?? {}).map(([key, value]) => {
      if(typeof value === "String") {
        return [key, value.trim()]
      }
      return [key, value]
    })
  )
  console.log("userId",userId)
  console.log("userPassword",userPassword)

  // 0. 데이터 유효성 검사하기
  if(!userId || !userPassword) {
    return ApiResponse.getInvalidDataResponse(res, {datas: ["userId", "userPassword"]})
  }

  // 1. id 존재하는지 확인하기
  const user =  await UserRepository.getUserByUserId(userId)
  if(!user) {
    return ApiResponse.getWrongInputResponse(res, { datas: ["userId", "userPassword"] })
  }

  // 2. password hashing 확인하기
  if(!(await bcrypt.compare(userPassword, user?.userPassword))) {
    return ApiResponse.getWrongInputResponse(res, { datas: ["userId", "userPassword"] })
  }

  // 3. jwt 토큰 발급해주기
  const token = jwt.sign({ id: user.id, role: user?.role || "user" }, config.jwt.secretKey, { expiresIn: config.jwt.expiresInSec })

  res.cookie("accessToken", token, {
    httpOnly: true,
    sameSite: "lax",
    path: "/",
    maxAge: 6*60*60*1000 // 6시간
  })

  // 사용자 데이터와 함께 보내주기
  return ApiResponse.getTaskSuccessResponse(res, { datas: { _id: user?._id, userId: user?.userId, userName: user?.userName, userRole: user?.userRole, userEmail: user?.userEmail }})
}

// 회원가입
export async function signup(req, res) {
  // 0. 모든 데이터가 잘 존재하는지 확인
  const { userId, userPassword, userName, userEmail } = Object.fromEntries(
    Object.entries(req?.body ?? {}).map(([key, value]) => {
      if(typeof value === "String") {
        return [key, value.trim()]
      }
      return [key, value]
    })
  )
  
  // 1. 유효성 검사 한번 해주기
  if(!userId || !userPassword || !userName || !userEmail) {
    return ApiResponse.getInvalidDataResponse(res, { datas: ["userId", "userPassword", "userName", "userEmail"] })
  } 

  // userId 중복 확인해주기
  if(await UserRepository.getUserByUserId(userId)) {
    return ApiResponse.getInvalidDataResponse(res, { message: "이미 존재하는 사용자의 아이디입니다.", datas: ["userId"] })
  }
  // userEmail 중복 확인해주기
  if(await UserRepository.getUserByUserEmail(userEmail)) {
    return ApiResponse.getInvalidDataResponse(res, { message: "이미 존재하는 사용자의 이메일입니다.", datas: ["userEmail"] })
  }

  // 2. 비밀번호 해싱해주기
  const hashed = bcrypt.hashSync(userPassword, config.bcrypt.saltRounds)

  // 2. 사용자 추가해주기
  const createdId = await UserRepository.createUser({ userId, userPassword: hashed, userName, userEmail })

  return ApiResponse.getTaskSuccessResponse(res, { message: "회원가입에 성공하였습니다.", datas: { id: createdId } })
}

// 로그아웃
export async function logout(req, res) {
  
}

// 회원 탈퇴
export async function signout(req, res) {
  
}

// 로그인 체크
export async function me(req, res) {
  
}