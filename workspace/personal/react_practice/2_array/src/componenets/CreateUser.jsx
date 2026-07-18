// import React from "react"

function CreateUser({ userid, name, email, onChange, onCreate }) {
    return (
        <div>
            <input name="userid" placeholder="아이디를 입력하세요" value={userid} onChange={onChange} />
            <input name="name" placeholder="이름을 입력하세요" value={name} onChange={onChange} />
            <input name="email" placeholder="이메일을 입력하세요" value={email} onChange={onChange} />
            <button onClick={onCreate}>등록</button>
        </div>
    )
}

export default CreateUser
