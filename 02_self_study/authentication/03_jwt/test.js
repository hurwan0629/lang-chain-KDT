import jwt from "jsonwebtoken"
import bcrypt from "bcrypt"

const secretKey = "dasf1234abAS#$"

const myPassword = "Qwer!@34"
const saltRounds = 10

async function hashPassword(password) {
  const hashed = await bcrypt.hash(password, saltRounds)
  console.log("해시된 비밀번호:", hashed)
  return hashed
}

const hashPw = await hashPassword(myPassword)
// const inputPassword = "Qwer!@#$"
const inputPassword = "Qwer!@34"
const isMatch = await bcrypt.compare(inputPassword, hashPw)
console.log("비밀번호 일치 여부:", isMatch)


function main() {

  const token = jwt.sign(
    { sup: "abc123" , role: "guest"},
    secretKey,
    { expiresIn: "1h" }
  )
  
  console.log(token)
  
  try {
    const decoded = jwt.verify(token, secretKey)
    console.log("토큰 검증 성공:", decoded)
  } catch(err) {
    console.log("에러 발생")
  }
}
