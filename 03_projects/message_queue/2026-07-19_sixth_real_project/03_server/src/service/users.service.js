
import * as UserRepository from "../repository/users.repository.js"
import {createBcryptPassword} from "../utils/crypto.js";
import logger from "../utils/logger.js";

export async function getUserByUserId(id) {
    return await UserRepository.getUserById(id)
}

/**
 * users.id 중복 여부에 따라 존재 하면 true, 아니면 false 반환
 */
export async function checkUserIdExists(id) {
    return await UserRepository.checkUserIdExists(id)
}

export async function createUser({id, password, name, email, address}) {
    try {
        // 사용자 password Hash 시키기
        const passwordHash = await createBcryptPassword(password)

        const insertedUser = await UserRepository.createUser({id, passwordHash, name, email, address})

        logger("utils/users.service.js createUser",
            `insertedUser: ${JSON.stringify(insertedUser)}`)

        return insertedUser

    } catch (error) {
        logger("utils/users.service.js createUser",
            `error: ${error.message}`)
        return null
    }
}