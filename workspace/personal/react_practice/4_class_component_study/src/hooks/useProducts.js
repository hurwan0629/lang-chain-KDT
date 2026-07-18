import React, { useEffect, useState } from "react"
import Products from "../components/Products"

export default function useProducts({ salesOnly }) {

  const [loading, setLoading] = useState(true)
  const [error, setError] = useState()
  const [products, setProducts] = useState([])

  // useEffect 관련
  useEffect(() => {
    fetch(`data/${salesOnly ? "sale_" : ""}products.json`)
      .then((res) => res.json())
      .then((data) => {
        console.log(`[useProducts.useEffect] fetch(data/${salesOnly ? "sale_" : ""}products.json)`)
        console.log(`[useProducts.useEffect] data:`)
        console.log(data)

        setProducts(data)
      })
      .catch(e => setError(e.message))
      .finally(() => {
        console.log(`[useProducts.useEffect] fetch end`)
        setLoading(false)
      })

    return () => {
      console.log("useProducts.useEffect cleaned")
    }
  }, [salesOnly])

  return [
    loading,
    error,
    products,
  ]
}