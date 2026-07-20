
import * as UserRepository from "../repository/users.repository.js"

export async function getUserByUserId(id) {
    return await UserRepository.getUserById(id)
}