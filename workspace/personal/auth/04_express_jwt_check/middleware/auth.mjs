import * as ApiResponse from "../response/api.users.response.mjs"

// Cookie에서 사용자의 accessToken을 확인하여 존재하지 않으면 401 또는 403을 반환해주는 미들웨어
export const isAuth = (req, res, next, role) => {
  // 0. 쿠키에서 accessToken 뽑아주기
  const accessToken = res?.cookies?.accessToken

  // 1. 없으면 반환해주기 401
  if(!accessToken) {
    return ApiResponse.getInvalidUserResponse(res)
  }

  // 2. accessToken 파싱해서 id와 role 뽑아주기

  // 3. id가 유효한지(ObjectId가 되는지)와 role이 적절한지 확인 맞는지 guest < user < admin 
  //     401                                  403
  getInvalidUserResponse
  getForbiddenAccessResponse

  // 3. id와 role가 모두 제대로 존재하면 req.user에 .id와 .role로 넣어주기

  next()
}