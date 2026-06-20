from datetime import datetime


class OrderDAO:
  sql_create_order_header = "insert into order_header (member_id, total_price) values (%s, %s)"

  sql_create_order_item = "insert into order_item (order_id, product_id, quantity, price) values (%s, %s, %s, %s)"
  
  sql_create_user_payment = "insert into payment (order_id, method, paid_amount) values (%s, %s, %s)"

  sql_select_all_user_orders = sql = """
                SELECT id, total_price, status, created_at
                FROM order_header
                WHERE member_id = %s
                ORDER BY
                    CASE WHEN status = 'ready' THEN 0 ELSE 1 END,
                    created_at DESC
            """

  sql_select_one_order_item_by_id = """
              SELECT 
                o.id,
                p.name,
                o.quantity,
                o.price
              FROM order_item o
              INNER JOIN product p 
              ON o.product_id = p.id
              WHERE o.order_id = %s;
            """
  
  sql_set_order_paid = "update order_header set status = 'paid' where id = %s"

  sql_get_order_status_by_id = "select status from order_header where id = %s"
  
  """주문 헤더 생성 후 id 반환"""
  def create_order_header(self, cur, total_price, user_id) -> int:
    cur.execute(self.sql_create_order_header, (user_id, total_price))

    return cur.lastrowid

  """주문 상세 생성"""
  def create_order_item(self, cur, order_id, product_id, amount, curr_price) -> bool:
    return cur.execute(self.sql_create_order_item, (order_id, product_id, amount, curr_price)) > 0
  
  """사용자 주문 생성"""
  def create_user_payment(self, cur, order_id, method, pay_amount) -> bool:
    return cur.execute(self.sql_create_user_payment, (order_id, method, pay_amount)) > 0

  """사용자 주문(헤더) 조회"""
  def select_all_user_orders(self, cur, user_id) -> tuple[int, int, str, datetime]:
    cur.execute(self.sql_select_all_user_orders, (user_id, ))

    return cur.fetchall()
  
  """사용자 주문 아이템 조회"""
  def select_one_order_item_by_id(self, cur, order_id) -> tuple[int, str, int, int]:
    cur.execute(self.sql_select_one_order_item_by_id, (order_id, ))

    return cur.fetchall()

  """사용자 주문 결제됨 상태로 바꾸기"""
  def set_order_paid(self, cur, order_id) -> bool:
    return cur.execute(self.sql_set_order_paid, (order_id, ))
  
  """주문 상태 확인하기"""
  def get_order_status_by_id(self, cur, order_id) -> str:
    cur.execute(self.sql_get_order_status_by_id, (order_id, ))