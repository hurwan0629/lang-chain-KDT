// 로그인 및 회원가입 용 레이아웃


import { Outlet } from "react-router-dom";


export default function GuestLayout() {
  
  return (
    <>
      <h1>
        당신은 게스트입니다. (로그인/회원가입)
      </h1>
      <Outlet />
    </>
  )
}