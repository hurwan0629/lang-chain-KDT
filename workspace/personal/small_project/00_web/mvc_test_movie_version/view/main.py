

class Main:

  def __init__(self, service, ):
    self.service = service

    self.menu_list = {
      1:,
      2:,
      3:,
      4:,
      5:,
      6:,
      
    }


  def run(self):
    while True:
      menu: int = self._show_menu()

      if menu == 0:
        self._message("안녕히가세요")
        break
      else:
        if not self.menu_list.get(menu):
          print("예상하지 못한 이벤트가 발생하였습니다.")

    
  
  def _message(self, message: str):
    print(f"""
          ┌──────────────────┐
          │    {message}    │ 
          └──────────────────┘
          """)
  
  def _show_menu(self) -> int:
    while True:
      print("""
            
            ┌──────────────────┐
            │   [영화 관리창]    │
            │ 0. 프로그램 종료   │
            │ 1. 영화 전체 확인  │
            │ 2. 영화 제목 검색  │
            │ 3. 영화 추가      │
            │ 4. 영화 삭제      │
            │ 5. 장르 전체 확인  │
            │ 6. 장르 관리      │
            └──────────────────┘

            """)
      try:
        user_check = input("메뉴 번호를 입력해주세요: ")
        result = int(user_check)
        
        if not (0 <= result <=6):
          raise Exception
        
        return result
      except Exception:
        print("0~6 중 하나의 숫자만 입력해주세요 ;ㅁ;")
      

  
  @property
  def service(self):
    return self.__service
  
  @service.setter
  def service(self, service):
    self.__service = service

