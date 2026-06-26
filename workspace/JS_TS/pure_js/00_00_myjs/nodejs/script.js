// let, const, 스코프, 호이스팅
// 원시값/참조값, 얕은 복사/깊은 복사
// 함수, 콜백, 클로저
// this, 화살표 함수
// 객체, 배열 메서드
// 구조분해 할당, spread/rest
// Promise, async/await
// 모듈 import/export
// 프로토타입과 class
// 타입 변환, ==/===, truthy/falsy

// 심볼
function func1() {
  const id1 = Symbol("id");
  const id2 = Symbol("id");
  const id3 = Symbol(1);

  console.log(id1 == id2)
  console.log(id1 === id2)

  console.log(id1)
  console.log(id2)
  console.log(id3)

  const myType = {
    name: "hurwan",
    [id1]: 1234
  }

  console.log(myType)
}

// js는 동적 타입 언어]

// let, const는 블록타입을 가지는데
// var은 함수 스코프라서 다르게 동작?

// TDZ란? Temporal Dead Zone -> 메모리에 접근하지만 접근할 수 없는 사각지대

// 클로저

// this - 어디에서 호출되었는가에 따라 달라지는거.
function func2() {
  const example = {
    name: "Kim",
    sayHi() {
      console.log(this.name);
    }
  }
  const f = example.sayHi
  f();

  const newO = {
    name: "new object",
    f
  }

  newO.f()

  const obj = {
    name: "hello",
    normal() {
      console.log(this.name);
    },
    arrowFunc: () => {
      const name = "arrow";
      console.log(this.name)
    }
  }

  obj.normal()
  obj.arrowFunc()
}

objOuter = {
  name: "outer",
  func() {
    console.log("objOuter.func()")
    func2()
  },
  func2: func2
}

// func2();
// objOuter.func()
// objOuter.func2()

function func3() {
  const user = {
    name: "kim",
  };

  console.log(user.toString())

  class User {
    constructor(name) {
      this.name = name;
    }

    sayHi() {
      console.log(this.name);
    }
  }

  u = new User("class")

  u.sayHi()
}

function func4() {
  // 1. 동기코드 실행
  console.log(1);

  // 4. macrotask
  setTimeout(() => {
    console.log(2);
  }, 0);

  // 3. microtask
  Promise.resolve().then(() => {
    console.log(3);
  })

  // 2. 동기코드 실행
  console.log(4)
}

// func4()

// const fs = require("fs");
// console.log(fs)

// 
// const와 let
// 블록 스코프를 가짐
// 블록 안에서 선언되었으면 안에서만 쓰일 수 있음

// const = 변수에 다른 값을 대입할 수 없다. 참조 객체 내부를 바꾸는건 가능

// var 은 함수 스코프

// 스코프
// 스코프의 종류에는
// 전역 스코프
// 함수스코프
// 블록 스코프

// 가 존재함.
function func5() {
  // var은 가장 가까운 함수에 붙는다.
  console.log(x)
  // console.log(y) // err
  
  function func_ex() {
    var y = 10;
  }
  
  if(true) {
    var x = 10;
  }
}

// 비동기
async function func6() {
  async function hello() {
    await Promise.resolve().then(() => {
      console.log("hello");
    })
    return "hello returned";
  }

  const result = hello();

  // result.resolve();
  console.log(result)

  async function timered() {
    const hello = setTimeout(() => {
      console.log("hello");
    }, 10)

    console.log(hello)
  }

  timered()
}

// Promise
function func7() {
  const promise = new Promise((resolve, reject) => {
    const success = true;

    if (success) {
      resolve("성공 결과");
    }
    else {
      reject("실패 이유");
    }
  })

  promise.then((result) => {
    console.log(result);
  }).catch((e) => {
    console.log(e)
  });
}
// func7()

// 여러 비동기 함수 동시에 돌리기
async function func8() {
  function delay(ms) {
    return new Promise((resolve) => {
      setTimeout(resolve, ms);
    })
  }

  async function countingFunc(name, term) {
    let c = 5;
    while(c >= 1) {
      console.log(`${name}: ${c}`);
      c--;

      await delay(term);
    }

    return `${name} end`;
  }


  console.log(" --- 각개 시작 및 처리 --- ");
  let r1 = countingFunc("first", 800);
  let r2 = countingFunc("second", 1000);
  let r3 = countingFunc("third", 500);

  // console.log(await r1);

  setTimeout(async () => {
    console.log("---------")
    console.log(await r1);
    console.log(await r2);
    console.log(await r3);
    // console.log(r3.then((result) => console.log(result)));
    // console.log(r1.then((result) => console.log(result)));
    // console.log(r2.then((result) => console.log(result)));

    console.log(" --- 병렬 시작 및 처리 --- ");

    const [a, b, c] = await Promise.all([
      countingFunc("first", 800),
      countingFunc("second", 1000),
      countingFunc("third", 500)
    ])

    console.log(a)
    console.log(b)
    console.log(c)
  }, 9000);
}

// func8()

async function func9() {
  async function ex() {
    return "hello"
  }
  result = ex()
  console.log(result)
  console.log(await result)
  return
}

// func9()

function func10() {
  async function f() {

    const pro = new Promise((resolve, reject) => {
      let success = true;

      if(success) {
        resolve(() => {
          console.log("hello"); 
          return "result";
        })
      }
      else {
        reject(() => {
          console.log("go away"); 
          return "bye";
        })
      }
    })
  
    const result = await pro
    console.log("---------")
    console.log(result())

    return "a";
  }

  const fv = f();
  console.log(`f(): ${fv}`)

  setTimeout(async () => {
    console.log(`await f(): ${await fv}`)
  }, 0)
}

// func10();

function func11() {

  function waitfunc() {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve("1초 경과");
      }, 1000 ); // 1초 뒤 반환
    })
  }

  async function canWait() {
    const result = waitfunc();

    console.log(`await 전: ${result}`);
    console.log(`await 후: ${await result}`);

  }
  canWait()
}

func11()