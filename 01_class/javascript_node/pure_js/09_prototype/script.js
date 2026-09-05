/*
프로토타입
- 자바스크립트에서 객체가 공통된 속성과 메서드를 공유하도록 해주는 매커니즘
- 모든 객체는 내부에 prototype라는 숨겨진 연결을 가지며 자신에게 없는 속성이나 메서드를 요청받으면 이 연결을 따라 프로토타입 객체에서 찾아옴
- 여러 객체가 동일한 메서드를 각각 따로 가지지 않고, 하나의 원본을 공유할 수 있어 메모리를 절약하고 구조적인 코드 작성이 가능


*/
function func1() {

  function Person(name) {
    this.name = name
  }
  
  const p1 = new Person("김사과")
  const p2 = new Person("반하나")
}

function func2() {
  const user = {
    name: "kim"
  };

  console.log(user.toString());
}

function func3() {
  console.log(Object.prototype)
  console.log(Number.prototype)

  class Animal {
    
  };

  const a = new Animal;
  const b = new Animal;

  const obj = {
    name: "hong",
    age: 20
  }

  const obj2 = {...obj}

  const obj3 = {
    name: "hong",
    age: 20
  }

  console.log(a.prototype === b.prototype)

  console.log(obj.prototype)
}

func3() 