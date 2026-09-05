import React from "react"

function User() {

}

function UserList() {
  const users = [
    {
      id: 1,
      userId: "apple",
      name: "김사과",
      email: "apple@apple.com"
    },
    {
      id: 2,
      userId: "apple",
      name: "김바나",
      email: "banana@banana.com"
    },
    {
      id: 3,
      userId: "kiwi",
      name: "김키위",
      email: "kiwi@kiwi.com"
    }
  ]

  return (
    <div>
      {/* <div><b>{users[0].userId}</b><span>{users[0].name}</span></div> */}
        {
          users.map((user, idx) =>{
              return (<div key={idx}><b>{user.userId}</b><span>{user.name}</span></div>)
            }
          )
        }
    </div>
  )
}

export default UserList