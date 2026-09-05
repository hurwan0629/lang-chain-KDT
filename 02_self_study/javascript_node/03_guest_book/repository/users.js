const path = require("path")
const fs = require("fs")

const datasDir = path.join(__dirname, "..", "datas")
const userDataFile = path.join(datasDir, "users.json")

function prevWork() {

  // /datas 폴더 확인
  if(!fs.existsSync(datasDir)) {
    fs.mkdirSync(datasDir, { recursive: true })
  }

  // datas/ 가 있다는 가정 하에 .json 파일 찾기. 없으면 생성
  if(!fs.existsSync(userDataFile)) {
    fs.writeFileSync(userDataFile, "[]")
  }

  return JSON.parse(fs.readFileSync(userDataFile))
}

// 사용자 조회하기
function selectAllUsers() {
  const users = prevWork()

  return users
}

// 사용자 추가하기
function addUser({userName, userId, password}) {
  let users = prevWork()

  console.log({userName, userId, password})

  const userCode = (Math.max(...users.map(user => {
    // console.log(user?.userCode)
    // console.log(user?.userCode || 0)
    return user?.userCode || 0
  })) || 0) +1

  users.push({
    userCode,
    userName,
    userId,
    password
  })

  fs.writeFileSync(userDataFile, JSON.stringify(users), "utf-8")

  return userCode
}

// 사용자 code로 이름 받기
function getUserDataByCode(userCode) {
  const users = prevWork()

  const filteredUsers = users.filter(user => String(user.userCode) === String(userCode))

  const userData = filteredUsers.length === 0 ? null : filteredUsers[0]

  return userData
}

// 사용자 userId 이름 받기
function getUserDataByUserId(userId) {
  const users = prevWork()

  const filteredUsers = users.filter(user => String(user.userId) === String(userId))

  const userData = filteredUsers.length === 0 ? null : filteredUsers[0]

  return userData
}

module.exports = {
  selectAllUsers,
  addUser,
  getUserDataByCode,
  getUserDataByUserId
}