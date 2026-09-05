import { sendEmail, connectEmail } from "./utils/gmail.js";
import {createRandomIntCode, createUUID} from "./utils/crypto.js";
import redis, {closeRedis, connectRedis} from "./config/redis.js";

const email = "cchamppang0629@gmail.com"

// 1. 사용자임시 uuid 생성 후 이메일 발송하여 uuid에 대한 이메일 주소 4분으로 redis에 저장하기
const registeringUserId = createUUID()
const randomCode = createRandomIntCode()

console.log("registeringUserId:", registeringUserId)
console.log("randomCode:", randomCode)


// 2. redis에 {emailVerifyUUID}: {code} 형태로 4분 저장하기
await connectRedis()

await redis.set(registeringUserId, randomCode, {
    EX: 240
})
await closeRedis()

// 3. email 발송하기
await connectEmail()
const emailResult = await sendEmail({
    to: "hurwan2005@gmail.com",
    subject: "verify Code",
    text: randomCode,
    html: `<h1>Hello Gmail! <br/>randomCode: ${randomCode}</h1>`
})

console.log("emailResult:", emailResult)