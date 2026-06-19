from server.service.service import Service
from collections.abc import Callable
from .menu1.page1 import Page1
from .menu2.page2 import Page2
from view.util.page_name import get_page_name

class App:
  def __init__(self, service: Service):
    if not service.heartbeat:
      raise Exception("[서버 예외] 서버가 준비되지 않았습니다!")

    self.__page1 = Page1(service=service)
    self.__page2 = Page2(service=service)

    page_services = (self.__page1.get_page_services() + self.__page2.get_page_services())

    """
    index: ("service_name", callable_service_func)
    index should not be 0
    """
    self.__menu: dict[int, tuple[str, Callable]] = {
      i: (page_name, page_func)
      for i, (page_name, page_func) in enumerate(page_services, start=1)
    }
  
  def run(self):
    print("서비스가 시작됩니다.")
    while True:
      i = 1
      for m in self.__menu.values():
        print(f"{i}. {m[0]}") 
        i+=1

      try:
          user_input = int(input("메뉴를 선택하세요: "))
      except ValueError:
        print("숫자를 입력해주세요.")
        continue

      if user_input == 0:
        print("프로그램을 종료합니다.")
        break

      try:
        menu = self.__menu.get(user_input, None)
        
        if menu is not None:
          menu[1]()
        else:
          print(f"메뉴는 '{self.__menu.keys()}'만 선택할 수 있습니다.")
        
      except ValueError:
        print("입력값의 형식이 올바르지 않습니다.")
      except Exception as e:
        print("오류:", e)
