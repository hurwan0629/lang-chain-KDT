function main() {
  // console.log("테스트asdfasdf")

  // const readline = require("readline")

  // 노드에서 제공하는 전역 객체
  // console.log(process.version)
  // console.log(process.env)
  // console.log(process.argv)

  // 노드 JS가 가지고 있는 읽기용 스트림 객체(fd 0). 프로세스당 기본으로 하나 제공받음
  // console.log(process.stdin)

  // let rl = readline.createInterface({
  //   input: process.stdin,
  //   output: process.stdout
  // });

  // rl.on("입력: ", (input) => {
  //   console.log(`사용자의 입력: ${input}`)
  //   rl.close()
  // })
  // process.stdout.write("hello user")
  // process.stdout.write("hello user")

  process.stdin.setRawMode(true);
  // process.stdin.setRawMode(false)

  // console.log(process.stdin.isTTY)
  process.stdin.resume()
  process.stdin.setEncoding("utf8")

  process.stdin.on("data", (key) => {
    // console.log(`echo: ${key}`)
    
    if(key === "\u001b[A") {
      process.stdout.write("up\n")
    }
    if(key === "\u001b[B") {
      process.stdout.write("down\n")
    }
    if(key === "\u001b[C") {
      process.stdout.write("right\n")
    }
    if(key === "\u001b[D") {
      process.stdout.write("left\n")
    }
    if(key === "\u0003") {
      process.exit()
    }
  })
}

module.exports = main