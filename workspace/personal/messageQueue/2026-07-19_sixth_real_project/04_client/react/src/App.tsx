import './App.css'

function App() {
  async function fetchSomething() {
    const res = await fetch("http://127.0.0.1:8080/api/admin/admin")

    console.log(res.ok)

    const data = await res.json()

    console.log(data)
  }

  return (
    <>
      <button onClick={fetchSomething}>
        hello
      </button>
    </>
  )
}

export default App
