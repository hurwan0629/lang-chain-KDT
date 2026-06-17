function func1() {
  function Person(name, age) {
    this.name = name;
    this.age = age
    this.greet = function() {
      console.log("안녕하세요, 저는 " + this.name + "입니다")
    }
  }
  
  const person1 = new Person("허완", 22)
  person1.greet()

}  

function func2() {
  class Person {
    constructor(name, age) {
      this.name = name
      this.age = age
    }

    greet(){
      console.log(`hello, im ${this.name}, age is ${this.age}`)
    }
  }
}