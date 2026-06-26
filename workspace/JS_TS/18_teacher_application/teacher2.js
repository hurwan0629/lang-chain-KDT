/*
    파일 입출력
    fs(File System) 모듈을 사용해서 파일을 읽고 쓰는 작업을 수행
*/
const fs = require("fs")
console.log();

const datas = fs.readFileSync(`${__dirname}/example.txt`, "utf8")
console.log(datas)

// 비동기 방식으로 파일 읽기
fs.readFile(`${__dirname}/example.txt`, "utf8", (err, data) => {
    if(err) {
        console.log("파일 읽기 실패: ", err)
        return
    }
    console.log(data)
    return
})

/////////////////////////////////////
// 동기 방식으로 파일 쓰기
fs.writeFileSync(`${__dirname}/output1.txt`, "이 내용이 파일에 저장됩니다. 동기방식!")
console.log("파일 저장완료")

fs.writeFile(`${__dirname}/output2.txt`, "비동기 방식으로 저장합니다.", (err) => {
  if(err) {
    console.log("저장 실패", err)
    return
  }
  console.log("파일 저장 완료 (비동기)")
})


// 비동기 방식으로 파일 삭제하기
fs.unlink("output2.txt", (err) => {
    if (err) throw err
    console.log("파일 삭제 완료!!!")
})