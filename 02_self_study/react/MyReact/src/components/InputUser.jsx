import React from "react"
import { useState } from "react"

export default function InputUser() {
  const [inputs, setInputs] = useState({
    userId: "",
    userPassword: ""
  })

  const { userId, userPassword } = inputs

  return (
    <div>
      <input name="userPassword" placeholder="아이디를 입력하세요" 
      value={userId} 
      onChange={e => setInputs({ userId: e.target.value, userPassword: userPassword })}/> <br />
      <input type="password" name="userPassword" placeholder="비밀번호를 입력하세요" 
      onChange={e => setInputs({ userId: userId, userPassword: e.target.value })}
      value={userPassword} />

      <button onClick={e => setInputs({ userId: "", userPassword: "" })}>초기화</button>
      <div><b>값: {userId}({userPassword})</b></div>
    </div>
  )
}