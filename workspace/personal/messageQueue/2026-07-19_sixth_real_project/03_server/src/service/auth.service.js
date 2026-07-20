import * as UserRepository from "../repository/users.repository.js"
import {compareBcryptPassword} from "../utils/crypto.js";
import logger from "../utils/logger.js";

export async function checkUserIdAndPasswordAvailable(id, password) {
  // repo에서 데이터 꺼내와서 bcrypt 확인하기
  try {
    const user = await UserRepository.getUserById(id)

    if(!user) {
      return false
    }

    // 사용자 정보에서 passwordHash 꺼내기
    const { id, passwordHash } = user

    // 비교 후 즉시 반환하기
    return await compareBcryptPassword(password, passwordHash)
    
  } catch (error) {
    logger("/service/auth.service.js checkUserIdAndPasswordAvailable",
        `error: ${error.message}`)
    throw error
  }
}