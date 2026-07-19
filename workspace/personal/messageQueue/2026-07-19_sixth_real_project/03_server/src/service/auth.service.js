import * as UserRepository from "../repository/users.repository.js"

export async function checkUserIdAndPasswordAvailable(id, password) {
  // repo에서 데이터 꺼내와서 bcrypt 확인하기
  try {
    const user = await UserRepository.getUserById(id)

    if(!user) {
      return false
    }

    
  } catch (error) {
  
  }
}