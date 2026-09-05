// function test({a, b}) {
//   console.log(a)
//   console.log(b)
// }
// test({
//   a: "a",
//   b: "bella"
// })

const { selectAllUsers, addUser, getUserDataByCode } = require("../repository/users")
const { selectAllDatas, addLog } = require("../repository/regist_log")

// selectAllUsers()
// console.log(selectAllDatas())
// console.log(selectAllUsers())
// addUser({ 
//   userName:  "kim gong", 
//   userId: "gongong", 
//   password: "sadf123"
// })

// console.log(selectAllUsers())

console.log(getUserDataByCode(3))