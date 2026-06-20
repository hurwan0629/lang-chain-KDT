# \view\login_page\main.py
# 로그인 페이지

from app.server.service.service import Service
from app.view.page_interface import Page
from app.server.data.dto.user_login_dto import UserLoginSuccessDTO
from typing import Optional
from .main_page.main import MainPage

class LoginPage(Page):
  pass
  def __init__(self, service: Service):
    self.__service = service
    
  """False 반환 시 메인 메뉴로, True 반환 시 프로그램 종료"""
  def run_page(self) -> bool:
    while True:
      print("\n"*10)
      print("==========================")
      print(f"  로그인")
      print(f"  *나가시고 싶으시면 '0'을 입력해주세요")
      print("==========================")

      r: tuple[Optional[UserLoginSuccessDTO | None], bool] = self.try_login()
      result, exit_flag =  r

      if exit_flag:
        print("메인 메뉴로 돌아갑니다.")
        return False
      
      if result is None:
        print("\n"*10)
        print("비밀번호 또는 아이디가 잘못되었습니다. 다시 입력해주세요")
      else:
        print(f"로그인 성공! 환영합니다 {result.name}님!")
        input("아무 키를 눌러 메인 페이지로 들어가세요: ")
        print()
        return MainPage(self.__service, result.id, result.name, result.username).run_page()
        
  def try_login(self) -> tuple[Optional[UserLoginSuccessDTO | None], bool]:
    username = input("아이디를 입력해주세요: ")
    if username == "0":
      return None, True
    password = input("비밀번호를 입력해주세요: ")
    if password == "0":
      return None, True
    
    # 혹시 sql 에러 안나게 길이 확인해주기
    if len(username) > 90:
      print("사용자 아이디의 길이는 90이하입니다.")
      return None, False
    if len(password) > 20:
      print("사용자 비밀번호의 길이는 20이하입니다.")
      return None, False
    
    user_login_dto: UserLoginSuccessDTO | None = self.__service.try_login(username, password) 

    return user_login_dto, False
    
