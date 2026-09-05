import { useState, useRef } from "react"
import CreateUser from "./componenets/CreateUser"
import UserList from "./componenets/UserList"

function App() {
  const [inputs, setInputs] = useState({ userid: "", name: "", email: "" })
  const { userid, name, email } = inputs
  const [users, setUsers] = useState([
    {
      id: 1,
      userid: "apple",
      name: "김사과",
      email: "apple@apple.com",
      select: true
    },
    {
      id: 2,
      userid: "banana",
      name: "반하나",
      email: "banana@banana.com",
      select: false
    },
    {
      id: 3,
      userid: "orange",
      name: "오렌지",
      email: "orange@orange.com",
      select: false
    },
    {
      id: 4,
      userid: "melon",
      name: "이메론",
      email: "melon@melon.com",
      select: false
    }
  ])

  const onChange = (e) => {
    const { name, value } = e.target
    setInputs({
      ...inputs,
      [name]: value
    })
  }

  const nextId = useRef(5)    // users 리스트에서 id를 4까지 사용 중이니까 기본값을 5로

  const onCreate = () => {
    const user = {
      id: nextId.current,
      userid,
      name,
      email
    }

    setUsers([...users, user])

    setInputs({
      userid: "",
      name: "",
      email: ""
    })

    nextId.current += 1
  }

  const onRemove = (id) => {
    setUsers(users.filter((user) => user.id !== id))
  }

  const onToggle = (id) => {
    setUsers(
      users.map((user) => user.id === id ? { ...user, select: !user.select } : user)
    )
  }

  return (
    <>
      <CreateUser userid={userid} name={name} email={email} onChange={onChange} onCreate={onCreate}></CreateUser>
      <UserList users={users} onRemove={onRemove} onToggle={onToggle} />
    </>
  )
}

export default App
