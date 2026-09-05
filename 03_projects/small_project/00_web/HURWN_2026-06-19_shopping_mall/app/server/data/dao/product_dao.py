from typing import Optional

class ProductDAO:
  sql_get_all_products = """
          select id, name, price, 
            case
              when stock = 0 then '품절'
              else stock
            end as stock
          from product
          """
  sql_get_all_products_by_keyword = """
          select id, name, price, 
            case
              when stock = 0 then '품절'
              else stock
            end as stock
          from product
          where name like %s
          """
  sql_check_id_exists = "select 1 from product where id = %s"

  sql_get_one_products_by_id_to_print = """
          select id, name, price, 
            case
              when stock = 0 then '품절'
              else stock
            end as stock
          from product 
          where id = %s
          """
  sql_increase_product_amount = "update product set stock = stock + %s where id = %s"

  """모든 상품 검색"""
  def get_products(self, cur) -> tuple[tuple[int, str, int, int]]:
    cur.execute(self.sql_get_all_products)
    # tuple[tuple[int, str, int, int, datetime.datetime]...]
    result = cur.fetchall()
    # print(f"실험 로그1: {result}")
    # print(f"실험 로그1: {type(result)}")

    return result
  
  """키워드로 상품 검색"""
  def get_products_by_keyword(self, cur, keyword: str) -> tuple[tuple[int, str, int, int]]:
    cur.execute(self.sql_get_all_products_by_keyword, (("%"+keyword +"%"), ))
    # tuple[tuple[int, str, int, int, datetime.datetime]...]
    result = cur.fetchall()
    # print(f"실험 로그1: {result}")
    # print(f"실험 로그1: {type(result)}")

    return result
  
  """상품 ID 존재하는지 확인"""
  def check_product_id_exists(self, cur, id: int) -> int:
    return cur.execute(self.sql_check_id_exists, (id, ))
  
  """출력용(id, 이름, 가격, 재고)"""
  def get_one_products_by_id_to_print(self, cur, id) -> tuple[int, str, int, Optional[str | int]]:
    cur.execute(self.sql_get_one_products_by_id_to_print, (id, ))

    return cur.fetchone()
  
    

  def increase_product_amount(self, cur, amount, id) -> bool:
    return cur.execute(self.sql_increase_product_amount, (amount, id)) > 0
