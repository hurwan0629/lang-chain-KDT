from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number

class MainPage(Page):
  def __init__(self, service: Service):
    self.__service = service

    self.__menu = ("메인 메뉴", (
      (1, "상품 목록 조회"),
      (2, "상품 검색"),
      (3, "주문하기"),
      (4, "주문 내역 조회"),
      (5, "로그아웃"),
      (0, "프로그램 종료"),
    ))
  
  # 페이지 시작
  def run_page(self):
    
    while True:
      # 사용자에게 값 정상적으로 받기
      user_input = get_menu_number(self.__menu)

  # 상품 목록 조회
