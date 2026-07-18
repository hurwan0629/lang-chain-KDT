import { useState, useReducer } from 'react'

function reducer(state, action) {
  if(action.type === "setName") {
    return {
      ...state,
      name: action.name
    }
  }
  else if(action.type === "init") {
    return {
      name: "undefined"
    }
  }
}

function App() {
  const [nameInput, setNameInput] = useState("")

  const [state, dispatch] = useReducer(reducer, {
    name: "init"
  })

  return (
    <>
      <h1>{state.name}</h1>
      <input 
      onChange={e => setNameInput(e.target.value)} 
      value={nameInput} />
      <button onClick={() => {
        dispatch({ type: "setName", name: nameInput })
        setNameInput("")
      }}>이름 설정하기</button>
      <button onClick={() => {
        dispatch({ type: "init", name: nameInput })
        setNameInput("")
      }}>이름 지우기</button>
    </>
  )
}

export default App
