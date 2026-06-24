/*
    async / await
    - Promise를 기반으로 한 자바스크립트의 비동기 처리 문법으로, 비동기 코드를 동기
    코드처럼 읽기 쉽고 직관적으로 작성할 수 있게 함
    - async가 붙은 함수는 항상 Promise를 반환하며,
*/

// async 함수는 항상 Promise를 반환
// await는 Promise 앞에서만 사용 가능
// async function run() {
//     const result = await somePromise()
//     console.log(result)
// }

// 순차 실행
// async function getData() {
//     const banana = await getBanana()
//     const apple = await getApple()
//     console.log(banana, apple)
// }