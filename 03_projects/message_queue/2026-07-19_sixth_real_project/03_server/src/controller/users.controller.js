import logger from "../utils/logger.js";
import {ApiError} from "../utils/ApiError.js";

import * as UserService from "../service/users.service.js"
import redis from "../config/redis.js";
import config from "../config/env.js";
import { checkUserIdExists } from "../service/users.service.js";

/**
 * 사용자 요청에 따라 id를 받아서 이미 존재하는지 확인해주는 핸들러
 * @returns {Promise<void>}
 */
export async function handleIdDuplicated(req, res) {
    const { id } = req.body

    if(!id) {
        logger("/router/api/email.router.js handleIdDuplicated",
            `error: id invalid}`)
        throw new ApiError(400, "invalid value", {})
    }

    const isDuplicated = await UserService.checkUserIdExists(id)

    // 사용자가 중복되면
    if(isDuplicated) {
        return res.status(200).json({
            success: true,
            message: "id available",
            data: {
                duplicated: true
            }
        })
    }
    // 사용자가 중복되지 않으면
    else {
        return res.status(200).json({
            success: true,
            message: "id unavailable",
            data: {
                duplicated: false
            }
        })
    }
}

/**
 * 사용자 회원가입 처리 핸들러
 * clientCode 를 반드시 확인해야함
 */
export async function handleUserSignup(req, res) {
    try {

        const {clientCode, id, password, name, email, address} = req.body

        // 1. 값 잘 들어왔나 확인
        if(!clientCode || !id || !password || !name || !email || !address) {
            logger("/controller/users.controller.js handleUserSignup",
                `invalid values 
                clientCode: ${!!clientCode} 
                id: ${!!id} 
                password: ${!!password} 
                name: ${!!name} 
                email: ${!!email} 
                address: ${!!address}`)
            throw new ApiError(400, "invalid values", {})
        }

        // 2. clientCode가 redis에 verified로 존재하는지 확인
        const clientEmailState = await redis.get(clientCode)

        if(clientEmailState !== config.email.verifiedString) {
            return res.status(422).json({
                success: false,
                message: "clientCode unabled or expired",
                data: {}
            })
        }

        // 3. id 한번 더 확인
        const isDuplicated = await UserService.checkUserIdExists(id)

        if(isDuplicated) {
            return res.status(400).json({
                success: false,
                message: "id duplicated",
                data: {
                    id
                }
            })
        }

        // 4. password Hash 시켜서 저장해주기
        const user = await UserService.createUser({clientCode, id, password, name, email, address})

        // 성공했다면
        if(!!user) {
            return res.status(201).json({
                success: true,
                message: "user created",
                data: {
                    user
                }
            })
        }
        // 실패했다면
        else {
            return res.status(500).json({
                success: true,
                message: "server error",
                data: {}
            })
        }
    } catch (error) {
        logger("/controller/users.controller.js handleUserSignup",
            `error: ${error.message}`)
        throw new ApiError(500, "server error", {})
    }
}
