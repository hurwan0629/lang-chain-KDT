// 비밀번호 생성 및 payments_key, 여러 메시지 id 생성 및 해싱 담당

import bcrypt from "bcrypt"
import crypto from "node:crypto"
import config from "../config/env.js";


/**
 * bcrypt 대조해주기
 */
export async function compareBcryptPassword(password, passwordHash) {
    return await bcrypt.compare(password, passwordHash)
}

/**
 * bcrypt 생성해주기
 */
export async function createBcryptPassword(password) {
    return await bcrypt.hash(password, config.bcrypt.salt)
}

export function createUUID() {
    return crypto.randomUUID()
}

/**
 * 랜덤 n자리 코드 만들어주기
 */
export function createRandomIntCode(length=config.email.codeLength) {
    return String(crypto.randomInt(0, 10**(length-1))).padStart(6, "0")
}