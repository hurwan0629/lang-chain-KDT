import React from "react"
import useProducts from "../hooks/useProducts"
import { useState } from "react"

export default function Products() {
  const [salesOnly, setSalesOnly] = useState(false)

  const handleChange = () => setSalesOnly((prev) => !prev)


  const [ loading, error, products ] = useProducts({ salesOnly })


  if(loading) {
    return <p>Loading 중...</p>
  }
  
  if(error) {
    return <p>{error}</p>
  }

  return (
    <>
      <input id="checkbox" type="checkbox" checked={salesOnly} value={salesOnly} 
        onChange={handleChange}/>
      <label htmlFor="checkbox">세일상품 보기</label>
      <ul>
        {
          products.map((product) => {
            return <li key={product.id}>
              <article>
                <h3>{product.name}</h3>
                <p>{product.price}</p>
              </article>
            </li>
          })
        }
      </ul>
    </>
  )

}