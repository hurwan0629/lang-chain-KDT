window.onload = function() {
  const ssn1 = document.getElementById("ssn1")
  ssn1.addEventListener("keyup", () => {
    if(ssn1.value.length >= 6) {
      document.getElementById("ssn2").focus()
    }
  })
}

function sendit() {
    const userid = document.getElementById("userid")
    const userpw = document.getElementById("userpw")
    const userpw_re = document.getElementById("userpw_re")
    const name = document.getElementById("name")
    const hp = document.getElementById("hp")
    const email = document.getElementById("email")


    const expIdText = /^[A-Za-z0-9]{4,20}$/
    /*
        (?=.*): 어디엔가 원하는 패턴이 하나라도 있어야 함
        (?=.*[A-Za-z]): 영문자가 최소 1개 이상 있어야 함
        (?=.*\d): 숫자가 최소 1개 이상 있어야 함
        (?=,*[!@#$%^&*()]): 제시된 특수 문자가 최소 1개 이상 있어야 함
        
    */
    const expPwTest = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[!@#$%^&*()])[A-Za-z\d!@#$%^&*()]{8,20}$/
    const expNameTest = /^[가-힣]+$/
    const expHpTest = /^\d{3}-\d{3,4}-\d{4}$/
    const expEmailTest = /^[A-Za-z0-9\-\.]+@[A-Za-z0-9\-]+\.[A-Za-z]+$/
    // const expEmailTest = /^[^\s@]+@[^\s@]+\.[^\s@]$/
    
    if(userid.value === ""){
        alert("아이디를 입력하세요")
        userid.focus()
        return false
    }

    if(!expIdText.test(userid.value)){
        alert("아이디는 4자 이상 20자 이하의 영문자 또는 숫자로 입력하세요")
        userid.focus()
        return false
    }

    if(!expPwTest.test(userpw.value)){
        alert("비밀번호는 8자 이상 20자 이하의 영문자, 숫자, 특수문자를 한 자 이상 꼭 포함해야 합니다")
        userpw.focus()
        return false
    }

    if(userpw.value != userpw_re.value){
        alert("비밀번호와 비밀번호 확인이 일치하지 않습니다")
        userpw_re.focus()
        return false
    }

    if(!expNameTest.test(name.value)){
        alert("이름은 한글로 입력하세요")
        name.focus()
        return false
    }

    if(!expHpTest.test(hp.value)){
        alert("휴대폰번호 형식이 일치하지 않습니다\n하이픈을 꼭 입력하세요")
        hp.focus()
        return false
    }

    if(!expEmailTest.test(email.value)){
        alert("이메일 형식이 일치하지 않습니다")
        email.focus()
        return false
    }
}

function checkSsn(){
    const ssn1 = document.getElementById("ssn1")
    const ssn2 = document.getElementById("ssn2")

    const expSsn1Test = /^[0-9]{6}/
    const expSsn2Test = /^[0-9]{7}/

    if(!expSsn1Test.test(ssn1.value)) {
      alert("주민번호 앞자리 형식이 일치하지 않습니다 (6자리 숫자)")
      ssn1.focus()
      return
    }

    if(!expSsn1Test.test(ssn2.value)) {
      alert("주민번호 뒷자리 형식이 일치하지 않습니다 (6자리 숫자)")
      ssn2.focus()
      return
    }

    try {
      // 001011
      // 3068518
      // console.log(ssn1.value+ssn2.value)
      const numList = (ssn1.value+ssn2.value).split('').map(s => Number(s))
      const divList = [2, 3, 4, 5, 6, 7, 8, 9, 2, 3, 4, 5]

      // console.log(numList)
      // console.log(divList)

      let sum = 0;
      for(let i=0;i<12;i++) {
        sum += numList[i] * divList[i]
      }

      // console.log(`sum: ${sum}`)

      sum = sum % 11

      // console.log(`sum: ${sum}`)

      if(sum >= 10) {
        sum %= 10
        // console.log(`sum: ${sum}`)
      }

      // console.log((11-sum))
      // console.log(numList[11])
      if((11-sum) === numList[12]) {
        alert('주민번호 인증 성공!')
      }
      else {
        alert('주민번호 인증 실패!')
      }
    } catch(e) {
      alert('주민번호 인증 실패!')
      console.log(e)
    }

} 