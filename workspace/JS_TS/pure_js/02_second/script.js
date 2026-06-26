// # 변수 종류
// var
// let
// const

let age = 20;
let name = "김사과";

console.log(age);
console.log(name);

// let name = "김땡땡";// error

console.log(name); 

var score = void
console.log(`점수: ${score}`);

var score = 100;

console.log(`재점수: ${score}`)

/*
var와 let/const의 가장 큰 차이는 변수의 유효 범위(scope)와 예측 가능성에 있습니다. var는 함수 단위 스코프를 가지며 선언 전에 사용해도 동작하는 호이스팅 특성 때문에 의도치 않은 오류를 만들기 쉽고, 중복 선언도 허용됩니다. 반면 let과 const는 블록 단위 스코프를 가져 {} 안에서만 유효하며 중복 선언이 불가능해 코드의 안정성이 높습니다. 또한 const는 한 번 할당한 값을 변경할 수 없어 의도를 명확히 표현할 수 있어, 현대 자바스크립트에서는 var 대신 let과 const 사용이 권장됩니다.
*/