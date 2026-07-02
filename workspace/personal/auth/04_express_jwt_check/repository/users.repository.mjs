import { getUser } from "../db/database.mjs"

// 사용자 추가하기
export async function createUser({ userId, userPassword, userName, userEmail }) {
  return getUser().insertOne({ userId, userPassword, userName, userEmail }).then(result => result.insertedId.toString())
}

// 아이디로 사용자 찾기
export async function getUserByUserId(userId) {
  return getUser().find({ userId }).next().then(mapOptionalUser)
}

// 이메일로 사용자 찾기
export async function getUserByUserEmail(userEmail) {
  return getUser().find({ userEmail }).next().then(mapOptionalUser)
}

// user 단일 Object를 받아서 존재하면 id속성을 추가해서 반환해주기
function mapOptionalUser(user) {
  return user ? { ...user, id: user._id.toString() } : user
}