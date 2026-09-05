import { useState } from "react"

export default function LoginPage() {

  const [userId, setUserId] = useState("")
  const [userPassword, setUserPassword] = useState("")


  function tryLogin() {

  }
  
  return (
    <div className="min-h-full w-full bg-white rounded-xl
      flex flex-col items-center justify-center">
      <div className="h-[70%] w-[40%] border rounded-xl border-black
          flex flex-col items-center justify-start gap-4 p-6">
        <h4>로그인 박스</h4>
        <input placeholder="아이디를 입력하세요"
          className="border border-black px-2"
          onChange={e => setUserId(e.target.value)}
        />  
        <input placeholder="비밀번호를 입력하세요"
          type="password"
          onChange={e => setUserPassword(e.target.value)}
          className="border border-black px-2"
        />
        <button 
          onClick={tryLogin}>
            로그인하기
        </button>
      </div>
    </div>
  )
}