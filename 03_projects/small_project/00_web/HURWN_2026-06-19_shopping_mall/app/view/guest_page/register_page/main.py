from abc import abstractmethod
from app.server.service.service import Service
from app.view.page_interface import Page
import re

# 0 입력하면 무조건 메인페이지로 가고
# 순서대로
# 1. 아이디 (중복 불가)
# 2. 비밀번호(암호화)
# 3. 이름 
# 4. 이메일 (중복 불가)
# 해서 받아야함

# ui 친절하게

class RegisterPage(Page):
  def __init__(self, service: Service):
    self.__service = service
  
  # 페이지 시작
  def run_page(self):
    
    while True:
      # 사용자에게 회어원가입 폼 주기
      print("==========================")
      print(f"  회원가입")
      print(f"  *나가시고 싶으시면 '0'을 입력해주세요")
      print("==========================")

      ((id, password, name, email), flag) = self.get_regist_form()

      if flag:
        print("메인페이지로 갑니다.")
        return False

      user_regist_dto = self.__service.regist_user(id, password, name, email)
      if user_regist_dto is not None:
        print(f"회원가입 성공~! 환영합니다 {user_regist_dto.name}님!")
      else:
        print(f"오류로 인해 로그인이 실패하였습니다.")
      
      input("아무 키를 눌러 메인 메뉴로 나가기")
      return False



      

  def get_regist_form(self) -> tuple[tuple[str, str, str, str], bool]:
    flag = False
    user_id = ""
    user_password = ""
    user_name = ""
    user_email = ""

    # # # 1. 사용자 아이디 받기
    while True:
      user_input = input("아이디를 입력해주세요: ")
      if user_input == "0":
        print("회원가입 페이지를 나갑니다.")
        flag = True
        break
      
      # 길이 체크 (8 ~ 90)
      if not (8 <= len(user_input) <= 90):
        print("사용자의 아이디 길이는 8 ~ 90 이여야합니다.")
        continue

      # 중복 체크
      if self.__service.check_username_duplicated(user_input):
        print("중복된 아이디 입니다. 다시 입력해주세요 ㅠㅠ")
        continue

      user_id = user_input
      break
      
    
    if flag:
      return ("", "", "", ""), flag
    
    # # # 2. 비밀번호 입력 받기
    while True:
      user_input = input("사용하실 비밀번호를 입력해주세요: ")
      if user_input == "0":
        print("회원가입 페이지를 나갑니다.")
        flag = True
        break

      # 길이 체크 (8 ~ 20)
      if not (8 <= len(user_input) <= 20):
        print("사용자의 비밀번호 길이는 8 ~ 20 이여야합니다.")
        continue
      
      user_input_check = input("동일한 비밀번호를 다시 입력해주세요: ")

      if user_input_check == "0":
        flag = True
        break

      # 비밀번호 재검사
      if not user_input == user_input_check:
        print("비밀번호를 다시 설정합니다.")
        continue

      user_password = user_input
      break
    
    if flag:
      return ("", "", "", ""), flag
    

    # # # 3. 사용자 이름 받기
    while True:
      user_input = input("이름을 입력해주세요: ")
      if user_input == "0":
        print("회원가입 페이지를 나갑니다.")
        flag = True
        break
      
      # 길이 체크 (8 ~ 90)
      if not (2 <= len(user_input) <= 20):
        print("사용자의 이름 길이는 2 ~ 20 이여야합니다.")
        continue

      user_name = user_input
      break
    
    if flag:
      return ("", "", "", ""), flag

    # # # 4. 사용자 이메일 받기
    while True:
      user_input = input("이메일를 입력해주세요: ")
      if user_input == "0":
        print("회원가입 페이지를 나갑니다.")
        flag = True
        break
      
      # 형식 체크 (8 ~ 90)
      if not (bool(re.fullmatch(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", user_input))):
        print("이메일 형식에 맞춰 입력해주세요.")
        continue

      # 길이 체크 (8 ~ 90)
      if not (8 <= len(user_input) <= 90):
        print("사용자의 이메일 길이는 20 ~ 90 이여야합니다.")
        continue

      # 중복 체크
      if self.__service.check_email_duplicated(user_input):
        print("중복된 이메일 입니다. 다시 입력해주세요 ㅠㅠ")
        continue

      user_email = user_input
      break
    
    return (user_id, user_password, user_name, user_email), flag

      
