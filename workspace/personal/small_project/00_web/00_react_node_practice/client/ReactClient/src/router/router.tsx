import { createBrowserRouter } from "react-router-dom";
import MainLayout from "../layout/MainLayout";
import NotFoundPage from "../pages/error/404";
import MainPage from "../pages/public/MainPage";
import AuthCheck from "../auth/AuthCheck";
import MyPage from "../pages/user/MyPage";
import RoomCreatePage from "../pages/user/RoomCreatePage";
import RoomDetailPage from "../pages/public/RoomDetailPage";
import RoomListPage from "../pages/public/RoomListPage";
// import GuestLayout from "../layout/GuestLayout";
import LoginPage from "../pages/guest/LoginPage";
import RegisterPage from "../pages/guest/RegisterPage";

const router = createBrowserRouter([
  // 모든 사용자용 [메인페이지, 방 목록, 방 상세페이지 (보기전용)]
  {
    path: "/",
    element: <MainLayout />,
    errorElement: <NotFoundPage />,
    children: [
      {
        index: true,
        element: <MainPage />
      },
      {
        path: "room/all",
        element: <RoomListPage />
      },
      {
        path: "room/:roomId",
        element: <RoomDetailPage />
      },
    ]
  },
  // 비회원 사용자용 [로그인, 회원가입]
  {
    path: "/guest",
    element: (
      <AuthCheck needAuth={false} >
        <MainLayout />
      </AuthCheck>
    ),
    children: [
      {
        path: "login",
        element: <LoginPage />
      },
      {
        path: "register",
        element: <RegisterPage />
      }
    ]
  },
  // 회원 사용자용 [마이페이지, 방 만들기, 입장하기, 수정하기, 삭제하기, 방에 글 작성]
  {
    path: "/user",
    element: (
      <AuthCheck needAuth={true} >
        <MainLayout />
      </AuthCheck>
    ),
    errorElement: <NotFoundPage />,
    children: [
      {
        path: "mypage",
        element: <MyPage />
      },
      {
        path: "room/create",
        element: <RoomCreatePage />
      },
    ]
  }
])

export default router