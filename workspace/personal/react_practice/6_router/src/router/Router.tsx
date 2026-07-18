import { createBrowserRouter } from "react-router-dom";
import MainPage from "../pages/MainPage";
import AuthLayout from "../layout/AuthLayout";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <MainPage />,
    children: [
      // 홈
      // 방 목록
      // 마이페이지
      // 로그인/로그아웃
    ]
  },
  {
    path: "/login",
    element: <AuthLayout />,
    children: [
      // 로그인 페이지
    ]
  },
  {
    path: "/"
  }
])