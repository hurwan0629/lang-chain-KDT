Promise.all([p1, p2, p3])
    .then(results => {
        console.log(results)
    })
- 모든 Promise가 성공해야 then을 실행
- 하나라도 실패하면 catch를 실행
- 병렬 처리용

Promise.race([p1, p2])
    .then(result => console.log(result))
- 가장 먼저 완료된 Promise 하나의 결과를 사용
- 성공/실패 상관없이 먼저 끝난 것을 기준

