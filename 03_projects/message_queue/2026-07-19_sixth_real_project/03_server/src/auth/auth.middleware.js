// jwt - access/refresh 설정해주는 계층

import logger from "../utils/logger.js"



export function checkAccessToken(req, res, next) {
  // req에서 cookie 뽑아서 
  const { accessToken } = req.cookies
  try {
    const { pk, role } = verifyAccessToken(accessToken)


    if(!pk || !role) {
      throw Error(`invalid access token pk: ${pk}, role: ${role}`)
    }

    req.user.pk = pk
    req.user.role = role

    
  } catch (error) {
    logger("auth.middleware.js checkAccessToken", `error: ${error}`)
    return res.status(400).json({
      success: false,
      message: "need auth",
      data: {}
    })
  }

  next()
}