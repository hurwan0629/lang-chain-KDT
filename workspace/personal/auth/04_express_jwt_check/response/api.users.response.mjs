// api.users.response.mjs

// 기본 응답 형태
function makeApiResponse(res, status, success, message, datas, errorInfo) {
  return res.status(status).json({
    success,
    message,
    datas: datas,
    errorInfo: errorInfo
  })
}

// // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // 2xx // // // // // // // // // // // // // // 

// // // // // // 200 // // // // // // 
// 단순 작업 완료 안내
export function getTaskSuccessResponse(res, { message="작업에 성공하였습니다.", datas={} } = {}) {
  return makeApiResponse(res, 200, true, message, datas, undefined)
}





// // // // // // // // // // // // // // // // // // // // // // // // // // 
// // // // // // // // // // 4xx // // // // // // // // // // // // // // 

// // // // // // 400 // // // // // // 
// 데이터 검증되지 않음 응답
export function getInvalidDataResponse(res, { message="데이터가 올바르지 않습니다.", datas=[] } = {}) {
  return makeApiResponse(res, 400, false, message, undefined, { errorData: datas })
}

// 틀린 값
export function getWrongInputResponse(res, { message="값이 틀렸습니다.", datas=[] } = {}) {
  return makeApiResponse(res, 400, false, message, undefined, { errorData: datas })
}

// // // // // // 401 // // // // // // 
// 인가되지 않은 사용자
export function getInvalidUserResponse(res, message="해당 기능을 사용하려면 로그인을 해주세요.") {
  return makeApiResponse(res, 401, false, message, undefined, undefined)
}

// // // // // // 403 // // // // // // 
// 허가되지 않은 권한
export function getForbiddenAccessResponse(res, {message="해당 기능을 사용하기 위한 권한이 부족합니다.", data={ userRole: undefined, requiredRole: undefined }} = {}) {
  return makeApiResponse(res, 403, false, message, undefined, data)
}
