from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number
from collections.abc import Callable
from typing import Optional

from .item_list_page.main import ItemListPage
from .item_search_page.main import ItemSearchPage
from .order_page.main import OrderPage
from .order_list_page.main import OrderListPage

class MainPage(Page):
  def __init__(self, service: Service, id, name, username):
    # 상태 저장
    self.__id = id
    self.__name = name
    self.__username = username

    self.__service = service

    self.__menu = ("메인 메뉴", (
      (1, "상품 목록 조회"),
      (2, "상품 검색"),
      (3, "주문하기"),
      (4, "주문 내역 조회"),
      (5, "로그아웃"),
      (0, "프로그램 종료"),
    ))

    self.__menu_func = {
      1: ItemListPage(service).run_page,
      2: ItemSearchPage(service).run_page,
      3: OrderPage(service, self.__id).run_page,
      4: OrderListPage(service, self.__id).run_page,
    }
  
  # 페이지 시작
  """메인 페이지 시작. False 반환 시 로그아웃, True 반환 시 프로그램 종료"""
  def run_page(self) -> bool:
    
    while True:
      # 사용자에게 값 정상적으로 받기
      user_input: int = get_menu_number(self.__menu)

      # 프로그램 종료
      if user_input == 0:
        return True
      elif user_input == 5:
        return False
      
      result: Optional[Callable | None] = self.__menu_func.get(user_input, None)
      try:
        if result is not None:
          result()
      except Exception as e:
        print(f"[ {__name__} ] 예상하지 못한 에러 발생: {e}")


  # 상품 목록 조회
