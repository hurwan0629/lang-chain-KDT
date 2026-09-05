import { useState } from "react"

export default function RegisterPage() {

  const [userId, setUserId] = useState("")
  const [userPassword, setUserPassword] = useState("")
  const [userPasswordCheck, setUserPasswordCheck] = useState("")
  const [userName, setUserName] = useState("")
  const [userPhone, setUserPhone] = useState("")

  
  function tryRegister() {
    
  }

  function checkIdDuplicated() {

  }

  return (
    <div className="flex-1 flex flex-col w-full justify-center items-center bg-white">
      <div className="h-[70%] w-[30%] rounded-xl border border-black
          flex flex-col items-center justify-start p-6 gap-4">
        <h4>회원가입 박스</h4>

        <div className="flex gap-1">
          <input placeholder="아이디를 입력하세요"
            className="w-40 border border-black px-2"
            onChange={e => setUserId(e.target.value)}
          />  

          <button onClick={checkIdDuplicated}
            className="rounded border border-black px-1  active:bg-gray-200">
            확인
          </button>

        </div>
        <input placeholder="비밀번호를 입력하세요"
          type="password"
          onChange={e => setUserPassword(e.target.value)}
          className="border border-black px-2"
        />
        <input placeholder="비밀번호를 다시 입력하세요"
          type="password"
          onChange={e => setUserPasswordCheck(e.target.value)}
          className="border border-black px-2"
        />
        <input placeholder="이름을 입력하세요"
          className="border border-black px-2"
          maxLength={5}
          onChange={e => setUserName(e.target.value)}
        />  
        <input placeholder="전화번호를 입력하세요"
          className="border border-black px-2"
          maxLength={11}
          onChange={e => setUserPhone(e.target.value)}
        />  



        <button 
          onClick={tryRegister}>
            로그인하기
        </button>
      </div>
    </div>
  )
}