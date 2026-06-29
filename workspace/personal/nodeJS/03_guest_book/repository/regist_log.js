const path = require("path")
const fs = require("fs")

const datasDir = path.join(__dirname, "..", "datas")
const registLogFile = path.join(datasDir, "registLog.csv")

function prevWork() {

  // /datas 폴더 확인
  if(!fs.existsSync(datasDir)) {
    fs.mkdirSync(datasDir, { recursive: true })
  }

  // datas/ 가 있다는 가정 하에 .csv 파일 찾기. 없으면 생성
  if(!fs.existsSync(registLogFile)) {
    fs.writeFileSync(registLogFile, "")
  }
}

// 파일 전체 조회하기
function selectAllDatas() {
  prevWork()

  // 파일 읽기
  const rows = fs.readFileSync(registLogFile, "utf-8")
          .trim()
          .split("\n")
          .map(row => {
            const data = row.split(",")
            return {
              logTime: data[0],
              name: data[1],
              content: data[2],
            }
          })

  return rows
}




// 방명록 추가하기
function addLog({ logTime, name, content }) {
  prevWork()

  const contentToWrite = `${logTime},${name},${content}\n`

  fs.appendFileSync(registLogFile, contentToWrite, "utf-8")

  return true
}


module.exports = {
  selectAllDatas,
  addLog
}