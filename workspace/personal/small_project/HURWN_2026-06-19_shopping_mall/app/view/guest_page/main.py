from abc import abstractmethod
from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number

from .login_page.main import LoginPage
from .register_page.main import RegisterPage

class GuestPage(Page):
  def __init__(self, service: Service):
    self.__service = service

    self.__menu = ("온라인 스토어", (
      (1, "회원가입"),
      (2, "로그인"),
      (0, "프로그램 종료"),
    ))

    self.__menu_func = {
      1: RegisterPage(service).run_page,
      2: LoginPage(service).run_page,
    }
  
  # 페이지 시작
  def run_page(self):
    
    while True:
      # 사용자에게 값 정상적으로 받기
      user_input = get_menu_number(self.__menu)
      # 먼저 프로그램 종료
      if user_input == 0:
         print("\n --- 프로그램을 종료합니다. --- \n")
         return True
      result = self.__menu_func.get(user_input, None)

      # 이미 정확하지만 혹시 모르니 에러 잡기
      try:
        if result is not None:
          if result():
            print("\n --- 프로그램을 종료합니다. --- \n")
            return True
          else:
            continue
      except Exception as e:
        print(f"[ {__name__} ] 예상하지 못한 에러 발생: {e}")
