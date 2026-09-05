/*
  원시타입
  원시 타입은 하나의 값만 저장하며, 값 자체가 변수에 직접 저장됩니다.

  Number
  String
  Boolean
  undefined
  null

  // n을 뒤에 붙이면 된다.
  BigInt: let bignum - 99999999999999n

*/

console.log(Number.MAX_SAFE_INTEGER)

let bigNum = 999999999999999999999999999999999n

console.log(`bigNum: ${bigNum}, type: ${typeof bigNum}`)