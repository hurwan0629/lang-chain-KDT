// 함수 표현식
const add = function(a, b) {
  return a + b;
}

const result2 = add2(3, 5)
console.log(result2)


// 화살표함수
const add3 = (a, b) => a + b
console.log(add3(3, 5))

function add2(a, b) {
  return a + b;
}

// 즉시 실행 함수(사용하기 전 문장을 ;으로 끝내야 함)
(function() {console.log("즉시실행됨")})()