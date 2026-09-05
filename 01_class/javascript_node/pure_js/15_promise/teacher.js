function getApple() {
    return new Promise((resolve) => {
        setTimeout(() => {
          // console.log(1)
          resolve('🍎')
        }, 3000)
    })
}

function getBanana() {
    return new Promise((resolve) => {
        setTimeout(() => {
          // console.log(1)
          resolve('🍌')
        }, 1000)
    })
}

function getOrange() {
    return Promise.reject(new Error("오렌지 없음"))
}

// Promise 체이닝
// getBanana().then((banana) => getApple().then((apple) => [banana, apple])).then(console.log)

// Promise.all([
//   getApple(),
//   getBanana()
//   ,getOrange()
// ]).then(
//   console.log
// ).catch( e => {
//   console.log("에러")
// })

// 가장 빨리 수행된 것이 실행
Promise.race([getBanana(), getApple()])
    .then((fruit) => console.log('race', fruit))

// 여러 프로미스를 병렬로 처리하되 하나의 프로미스가 실패해도 무조건 실행
Promise.allSettled([getBanana(), getApple(), getOrange()])
    .then((fruits) => console.log('allSettled', fruits))