import MySQLdb
from .base_service import BaseService
from app.server.data.db_common.conn import service_decorator

class OrderService(BaseService):

  @service_decorator(commit=True)
  def order_product_by_user(self, cur, product_id, amount, user_id: int, curr_price) -> int:
    # 재고 먼저 감소시키고 마지막에 재고 한번 더 확인해서 충분하면 커밋

    
    # 0. 혹시 모르니 다시 재고 확인
    data = self._dao.get_one_products_by_id_to_print(cur, product_id)
    stock = 0 if data[3] == "품절" else int(data[3])
    if stock < amount:
      raise MySQLdb.Error("상품 재고 문제 (무결성)로 인해 구매가 중지되었습니다.")
    

    # 1. 재고 감소시키고 
    if not self._dao.increase_product_amount(cur, -1*amount, product_id):
      raise MySQLdb.Error("상품 재고 감소중에 문제가 생겼습니다.")

    # 2. 주문 헤더 생성
    order_id = self._dao.create_order_header(cur, amount*curr_price, user_id)

    # 3. 주문 상세 생성
    if not self._dao.create_order_item(cur, order_id, product_id, amount, curr_price):
      raise MySQLdb.Error("상품 주문 생성중에 문제가 생겼습니다.")
    

    return order_id

  @service_decorator(commit=True)
  def insert_user_payment(self, cur, order_id, method, pay_amount) -> bool:
    if not self._dao.set_order_paid(cur, order_id):
      return False

    return self._dao.create_user_payment(cur, order_id, method, pay_amount)

  @service_decorator()
  def check_order_status(self, cur, order_id) -> str:
    return self._dao.get_order_status_by_id(cur, order_id)

  @service_decorator()
  def get_user_order_list(self, cur, user_id):
    return self._dao.select_all_user_orders(cur, user_id)
  # dao -> db 살아있는지 확인
  # 살이있으면 True 반환
  def heartbeat(self) -> bool:
    if self._dao is None or self.db is None:
      return False
    return True
  
  @service_decorator()
  def get_order_item_by_id(self, cur, order_id) -> tuple[int, str, int, int]:
    return self._dao.select_one_order_item_by_id(cur, order_id)
  