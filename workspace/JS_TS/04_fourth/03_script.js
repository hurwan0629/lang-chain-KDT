// 전역 스코프
var a = 1
let b = 2
const c = 3

function func1() {
  console.log(a, b, c)
}

func1()

console.log(window.a)
console.log(window.b)
console.log(window.c)


function func2() {
  if (true) {
    var x = 10
    let y = 20
  }
  console.log(x)
  // console.log(y)
}

func2()

const x = "전역"
function func3() {
  const x = "outer"
  function inner() {
    console.log(x)
  }
  inner()
}

func3()