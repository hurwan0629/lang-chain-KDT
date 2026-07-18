import { createContext, useContext } from "react";
import type { ReactNode } from "react";


export type AuthContextValue = {
  isAuth: boolean;
}

export const AuthContext = createContext<AuthContextValue | null>(null)

export function useAuth() {
  const auth = useContext(AuthContext)

  if(!auth) {
    throw new Error("useAuth는 AuthContextProvider 내부에서 사용해야합니다.")
  }

  return auth
}

export default function AuthProvider({ children }: { children: ReactNode}) {

  const value: AuthContextValue = {
    isAuth: false
  }

  return (
    <AuthContext.Provider value={ value } >
      {children}
    </AuthContext.Provider>
  )
}