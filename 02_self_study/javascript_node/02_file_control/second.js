const fs = require("fs")
const path = require("path")

const datasPath = path.join(__dirname, "datas")
const writeFilePath = path.join(datasPath, "hello.txt")

if(!fs.existsSync(datasPath)) {
  fs.mkdirSync(datasPath, { recursive: true })
}

fs.unlinkSync(writeFilePath)
if(!fs.existsSync(writeFilePath)) {
  fs.writeFileSync(writeFilePath, "")
}

function make_file_path(...file_loc) { 
  return path.join(datasPath, ...file_loc)
}

const readFileCallback = (err, data) => {
  if(!!err) {
    console.log(err)
    return
  }
  console.log(data)
}

// make_file_path("hello.txt")
let data = fs.readFileSync(writeFilePath, "utf8")
console.log("data:", data)

fs.writeFileSync(writeFilePath, "hello file system!\n안녕! 파일시스템!", "ascii")

data = fs.readFileSync(writeFilePath, "utf8")
console.log("data:", data)

const status = fs.statSync(datasPath)
// const status = fs.statSync(writeFilePath)
console.log("stat:", status)

fs.copyFileSync(writeFilePath, make_file_path("new_file.txt"))