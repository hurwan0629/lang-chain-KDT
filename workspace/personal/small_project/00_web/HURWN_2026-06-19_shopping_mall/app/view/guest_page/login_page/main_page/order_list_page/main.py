from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number
from app.view.component.print_order_default import print_order_table

# 주문한것들 페이지
class OrderListPage(Page):
  def __init__(self, service: Service, user_id: int):
    self.__user_id = user_id
    self.__service = service


  def run_page(self) -> bool:
    # ID, 총금액, 상태, 주문 날짜
    orders_data = self.__service.get_user_order_list(self.__user_id)
    print_order_table(orders_data)

    if len(orders_data) == 0:
      input("주문이 존재하지 않습니다! 메인 화면으로 나갑니다. (아무키 누르기)")
      return False

    choice = get_menu_number(("주문 목록 페이지",(
      (1, "주문 상세 보기"),
      (2, "주문 결제하기"),
      (0, "메인 화면으로 나가기")
    )))

    if choice == 0:
      return False
    elif choice == 1:
      self._detail_action(orders_data)
    else:
      if not self._payment_action(orders_data):
        input("아무 키나 눌러서 메인 메뉴로 나가기: ")
        return False
      else:
        input("결제가 완료되었습니다! (아무키나 눌러서 나가기): ")
        return False
  
  def _detail_action(self, orders_data):
    target_order_id = 0
    while True:
      try:
        user_input = int(input("확인할 주문 ID를 입력해주세요: "))

        order_ids = [row[0] for row in orders_data]
        if user_input not in order_ids:
          raise ValueError
        target_order_id = user_input
        break
      except ValueError:
        print("존재하지 않거나 이미 결제된 주문입니다.")
      except TypeError:
        print("올바른 숫자를 입력해주세요")

    product_data = self.__service.get_order_item_by_id(target_order_id)
    
    print(f"주문 상품: {product_data[1]}")
    print(f"주문 수량: {product_data[2]}")
    print(f"상품 개별 금액: {product_data[3]}")
    print(f"주문 총 금액: {product_data[2] * product_data[3]}")
      
  def _payment_action(self, orders_data):
    target_order_id = 0
    while True:
      try:
        user_input = int(input("결제할 주문 ID를 입력해주세요 (0 입력 시 나가기)"))

        if user_input == 0:
          break

        order_ids = [row[0] for row in orders_data]
        if user_input not in order_ids:
          raise ValueError
        if self.__service.check_order_status() != 'ready':
          print("이미 결제되거나 취소된 상품입니다.")
          continue
        target_order_id = user_input
        break
      except ValueError:
        print("존재하지 않거나 이미 결제된 주문입니다.")
      except TypeError:
        print("올바른 숫자를 입력해주세요")

    product_data = self.__service.get_order_item_by_id(target_order_id)
    
    print(f"주문 상품: {product_data[1]}")
    print(f"주문 수량: {product_data[2]}")
    print(f"상품 개별 금액: {product_data[3]}")
    print(f"주문 총 금액: {product_data[2] * product_data[3]}")
    
    user_choice = get_menu_number(("주문 방식을 선택해주세요", (
      (0, "취소"),
      (1, "카드"),
      (2, "계좌이체")
    )))

    if user_choice == 0:
      return False

    pay_method = 'card' if user_choice == 1 else 'bank'

    final_paid: bool = self.__service.insert_user_payment(target_order_id, pay_method, product_data[2] * product_data[3])
    if final_paid:
      print("결제가 완료되었습니다!")
      return True
    else:
      print("결제에 실패하였습니다.")
    return False

