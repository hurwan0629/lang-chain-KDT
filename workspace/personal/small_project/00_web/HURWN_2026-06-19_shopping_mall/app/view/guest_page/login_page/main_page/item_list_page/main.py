from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number
from app.server.data.dto.product_dto import ProductDTO
from tabulate import tabulate

"""상품 목록 조회 페이지"""
class ItemListPage(Page):
  def __init__(self, service: Service):
    self.__service = service


  def run_page(self) -> bool:
    # 이건 메뉴 목록이 아니라 존재하는 상품 전체 가져온 열들
    result = self.__service.get_all_product()
    headers = ["ID", "상품명", "가격", "재고"]
    # print(result)
    self.__product_table = tabulate(result, headers=headers, tablefmt="grid")

    print(self.__product_table)
    input("아무키나 눌러서 메인 메뉴로 나가기: ")
    return False
