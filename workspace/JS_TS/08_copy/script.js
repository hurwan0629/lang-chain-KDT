// 얕은복사
function func1() {
  let a = {
  x: 1,
  y: "hello",
  inner: {
    greet: "hello",
    language: {
      one: "one",
      two: "two"
    }
  }
}

  let b = { ...a }
  
  b.x = 3
  b.inner.greet = "welcome"
  b.inner.language.one = "1"
  
  console.log(a.x)
  console.log(a.inner.greet)
  console.log(a.inner.language.one)
}

// 깊은복사
function func2() {
   let a = {
    x: 1,
    y: "hello",
    inner: {
      greet: "hello",
      language: {
        one: "one",
        two: "two"
      }
    }
  }

  let c = structuredClone(a)

  c.x = 3
  c.inner.greet = "welcome"
  c.inner.language.one = "1"
  
  console.log(a)
  console.log(c)
}

// func2()

function func3() {
  let a = {
    x: 1,
    y: "hello",
    inner: {
      greet: "hello",
      language: {
        one: "one",
        two: "two"
      }
    }
  }

  let k = {...a, x: 1001}

  console.log(k)
}

// func3()
function func4() {
  function some(k = { styles: { color }}) {
    console.log(k.styles)
    console.log(k.styles.color)
  }

  const obj = {
    styles: {
      color: "black"
    }
  }
  some(obj);
}
func4()