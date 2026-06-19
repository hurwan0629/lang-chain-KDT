# \view\login_page\main.py
# 로그인 페이지

from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number
from app.server.data.dto.user_login_dto import UserLoginSuccessDTO
from typing import Optional
from .main_page.main import MainPage

class LoginPage(Page):
  pass
  def __init__(self, service: Service):
    self.__service = service
    
  
  def run_page(self):
    while True:
      print("==========================")
      print(f"  로그인")
      print(f"  *나가시고 싶으시면 '0'을 입력해주세요")
      print("==========================")

      r: tuple[Optional[UserLoginSuccessDTO | None], bool] = self.try_login()
      result, exit_flag =  r

      if exit_flag:
        print("메인 메뉴로 돌아갑니다.")
        break
      
      if result is None:
        print("비밀번호 또는 아이디가 잘못되었습니다. 다시 입력해주세요")
        input("(아무키를 입력해주세요)")
      else:
        print("로그인 성공!")
        input("아무 키를 눌러 메인 페이지로 들어가세요")
        print()
        MainPage(self.__service).run_page()
        break
    

  def try_login(self) -> tuple[Optional[UserLoginSuccessDTO | None], bool]:
    username = input("아이디를 입력해주세요: ")
    if username == "0":
      return None, True
    password = input("비밀번호를 입력해주세요: ")
    if password == "0":
      return None, True
    
    # 혹시 sql 에러 안나게 길이 확인해주기
    if len(username) >= 90:
      print("사용자 아이디의 길이는 90보다 짧아야합니다.")
      return None, False
    if len(password) >= 20:
      print("사용자 비밀번호의 길이는 20보다 짧아야합니다.")
      return None, False
    
    user_login_dto: UserLoginSuccessDTO | None = self.__service.try_login(username, password) 

    return user_login_dto, False
    
