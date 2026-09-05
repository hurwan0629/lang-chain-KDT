// 전체 레이아웃

import { Outlet } from "react-router-dom";
import Header from "../components/Header";
import Footer from "../components/Footer";


export default function MainLayout() {
  
  return (
    <main className="min-h-screen bg-gray-100 flex flex-col">
      <Header />
      <div className="flex-1 w-full bg-red-100 flex">
        <Outlet />
      </div>
      <Footer />
    </main>
  )
}