import {createRandomIntCode, createUUID} from "../utils/crypto.js";
import redis from "../config/redis.js";
import { sendEmail } from "../utils/gmail.js";
import logger from "../utils/logger.js";
import {ApiError} from "../utils/ApiError.js";
import config from "../config/env.js";

export async function sendEmailVerifyCode(req, res) {
    const { email } = req.body

    // 1. 사용자임시 uuid 생성 후 이메일 발송하여 uuid에 대한 이메일 주소 4분으로 redis에 저장하기
    const registingUserId = createUUID()
    const randomCode = createRandomIntCode()

    // 2. redis에 {emailVerifyUUID}: {code} 형태로 4분 저장하기
    try {
        await redis.set(registingUserId, randomCode, {
            EX: 240
        })
    } catch(error) {
        logger("/controller/email.controller.js sendEmailVerifyCode redis.registingUserId",
            `error: ${error.message}`)
        throw ApiError(500, "server error", {})
    }

    // 3. gmail 발송하기
    try {
        await  sendEmail({
            to: email,
            subject: "Email Verify",
            html: `<h3>Verify Code: [${randomCode}]</h3>`
        })
    } catch(error) {
        logger("/controller/email.controller.js sendEmailVerifyCode email.sendEmail",
            `error: ${error.message}`)
        throw ApiError(500, "server error", {})
    }

    // 4. 사용자 인증 uuid 발송해주기
    return res.status(200).json({
        success: true,
        message: "verify code sent",
        data: {
            clientCode: registingUserId
        }
    })
}

/**
 * clientCode, emailCode 를 받아서 존재하면 true 반환해주는 함수 -> ttl을 10분으로 늘려주기
 */
export async function checkEmailVerifyCode(req, res) {
    const { clientCode, emailCode } = req.body

    if(!clientCode || !emailCode) {
        logger("/controller/email.controller.js checkEmailVerifyCode",
            `invalid values clientCode: ${!!clientCode}, emailCode: ${!!emailCode}`)
        throw new ApiError(400, "invalid values", {})
    }

    // redis에서 꺼내서 작업하기
    const realEmailCode = await redis.get(clientCode)

    // 값이 만료되거나 존재하지 않으면
    if(!realEmailCode) {
        logger("/controller/email.controller.js checkEmailVerifyCode", `no email code. clientCode: ${clientCode}`)
        throw new ApiError(400, "code expired or not exists", {})
    }

    // 값이 틀리다면 반환
    if(realEmailCode !== config.email.verifiedString && emailCode !== realEmailCode) {
        logger("/controller/email.controller.js checkEmailVerifyCode",
            `wrong emailCode: ${emailCode}`)
        throw new ApiError(400, "invalid values", {})
    }

    // 맞다면 ttl 10분으로 늘려주기
    try {
        await redis.set(clientCode, config.email.verifiedString, {
            EX: 600
        })
    } catch (error) {
        logger("/controller/email.controller.js checkEmailVerifyCode",
            `redis.set verified error: ${error.message}`)
    }

    return res.status(200).json({
        success: true,
        message: "email verified",
        data: {}
    })
}