from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number
from tabulate import tabulate
from app.view.component.print_product_default import print_product_table

class ItemSearchPage(Page):
  def __init__(self, service: Service):
    self.__service = service

  def run_page(self) -> bool:
    user_input = input("검색어를 통해 상품을 검색하세요: ")

    result = self.__service.get_all_product_by_keyword(user_input)

    print_product_table(result)
    
    input("아무키나 눌러서 나가기: ")
    return False