import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import type { ReactNode } from "react";



export default function AuthCheck({ children, needAuth }: { children: ReactNode, needAuth: boolean }) {
  const { isAuth } = useAuth()

  return (
    <>
      {
        needAuth
        ? 
          isAuth 
          ? children
          : <Navigate to="/guest/login" />
        :
          isAuth 
          ? <Navigate to="/" />
          : children
      }
    </>
  )
}