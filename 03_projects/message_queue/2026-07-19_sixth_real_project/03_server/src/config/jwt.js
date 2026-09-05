import config from "./env.js";

export const accessCookieOptions = {
    path: config.jwt.accessCookiePath,
    sameSite: config.jwt.sameSite,
    httpOnly: config.jwt.httpOnly,
    secure: config.jwt.secure,
    maxAge: config.jwt.accessCookieMaxAge,
}

export const refreshCookieOptions = {
    path: config.jwt.refreshCookiePath,
    sameSite: config.jwt.sameSite,
    httpOnly: config.jwt.httpOnly,
    secure: config.jwt.secure,
    maxAge: config.jwt.refreshCookieMaxAge,
}