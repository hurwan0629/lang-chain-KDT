import React from "react"
// import Products from "./components/Products"
import Products from "./components/ProductHook"
import { useState } from "react"

function App() {

  const [showProducts, setShowProducts] = useState(true)

  function handler() {
     setShowProducts(prev => !prev)
  }

  return (
    <>
      <div>
        {
          showProducts 
          && <Products />
        }
        <button onClick={handler}>
          제품 보기
        </button>
      </div>
    </>
  )
}

export default App
