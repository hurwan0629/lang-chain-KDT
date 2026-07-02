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

// // // // // // 400 // // // // // // 
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