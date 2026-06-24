// Promise.all()


// 비동기 함수
example = new Promise((resolve, reject) => {
  const success = true;

  if(success) {
    resolve("성공입니다.")
  }
  else{
    reject("실패입니다.")
  }
})

console.log(`example: ${example}`)
async function a() {
  result = await example.then((r) => {
    return r
  }).catch((e) => {
    return e
  })

  console.log(`result: ${result}`)
}

console.log(Promise.resolve(example))
a()