import { Link } from "react-router-dom"
import { useAuth } from "../auth/AuthContext"

export default function Header() {

  const { isAuth } = useAuth()

  return (
    <div className="w-full h-[150px] bg-green-100 flex items-center justify-center">
      <div className="w-24 p-6 m-8">
        로고
      </div>
      <div className="flex-1 p-4 border border-black">
      헤더입니다.
      (useAuth Provider을 이용해서 isAuth를 기반으로 사용자 로그인 상태 확인하기.)

      이를 통해 사용자에게 회원가입/로그인 vs 마이페이지/로그아웃 선택지 보여주기
      </div>
      <div className="flex m-6 gap-3">
        {
          isAuth
          ? (
          <div >
            <Link to="/guest/login"
              className="rounded-md border border-black p-1 bg-white"
            >로그인</Link>
            <Link to="/guest/register"
              className="rounded-md border border-black p-1 bg-white"
            >회원가입</Link>
          </div>
          )
          : (
          <div >
            <Link to="/guest/login"
              className="rounded-md border border-black p-1 bg-white"
            >로그인</Link>
            <Link to="/guest/register"
              className="rounded-md border border-black p-1 bg-white"
            >회원가입</Link>
          </div>
          )
        }
      </div>
    </div>
  )
}