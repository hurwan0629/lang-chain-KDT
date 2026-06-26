const fs = require("fs")


console.log(__dirname)


// s = "string".repeat(30)

// console.log(s)

// fs.writeFile(`${__dirname}/my_test.txt`, s, (err) => {
//     if(err) {
//       console.log("쓰기 에러 발생: ", err)
//       console.log("\n\n")
//     }
//     return
//   }).then(() => console.log(`${i+1}번 쓰기 완료\n\n`))


for(let i=0;i<100;i++){
  s = String(i)
  fs.appendFile(`${__dirname}/my_test.txt`, s, (err) => {
    if(err) {
      console.log(`${i+1}번 쓰기 에러 ${err}`)
      console.log("\n")
    }
    console.log(`${i+1}번 쓰기 완료\n`)
  })
  fs.readFile(`${__dirname}/my_test.txt`, (err, data) => {
    if(err) {
      console.log(`${i+1}번 읽기 에러 ${err}`)
      console.log("\n")
      return
    }
    console.log(`${i+1}번 읽기 완료: ${data}\n`)
  })
  // fs.appendFileSync(`${__dirname}/my_test.txt`, s)
  // console.log(`${s}번 쓰기 완료\n`)
  // fs.readFileSync(`${__dirname}/my_test.txt`)
  // console.log(`${s}번 읽기 완료\n`)
}