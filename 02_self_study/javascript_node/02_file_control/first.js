
const fs = require("fs")
const path = require("path")

function make_file_path(...file_loc) {
  // console.log(...file_loc)
  return path.join(__dirname, "datas", ...file_loc)
}
// make_file_path("dir", "example.txt")
const target = make_file_path("example.txt")

const writeCallback = (err) => {
  if(!err) {
    console.log("쓰기 완료")
    return
  }
  console.log("에러 발생:", err)
}

fs.writeFileSync(target, "conasdftent")
fs.writeFile(target, "writing data", writeCallback)

fs.appendFile(target, "appended 데이터", writeCallback)

