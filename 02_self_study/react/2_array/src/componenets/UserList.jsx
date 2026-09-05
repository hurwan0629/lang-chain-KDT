// import React from "react"
import { useEffect } from "react"

function User( { user, onRemove, onToggle}) {

    useEffect(() => {                       // 실행순서 3
        console.log("user 설정: ", user)

        return() => {
            console.log("user 바뀌기 전: ", user)   // 실행순서 2
        }
    }, [user])

    console.log("User 컴포넌트 실행!")      // 실행순서 1

    return (
        <div>
            <b style={{ cursor: "pointer", color: user.select ? "deeppink" : "green" }} onClick={() => onToggle(user.id)}>{user.userid}</b>
            <span>({user.name} / {user.email})</span>
            <button onClick={() => onRemove(user.id)}>삭제</button>
        </div>
    )
}

function UserList({ users, onRemove, onToggle }) {
    return (
        <div>
            {users.map((user) => (
                <User user={user} key={user.id} onRemove={onRemove} onToggle={onToggle} />
            ))}
        </div>
    )
}

export default UserList
