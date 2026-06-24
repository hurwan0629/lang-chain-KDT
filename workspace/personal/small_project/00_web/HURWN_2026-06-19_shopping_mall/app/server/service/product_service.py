from .base_service import BaseService
from app.server.data.db_common.conn import service_decorator
from app.server.data.dto.product_dto import ProductDTO
from typing import Optional


class ProductService(BaseService):
  # def __init__(self, dao, db):
  #   self.__dao = dao
  #   self.db = db

  @service_decorator()
  def get_all_product(self, cur):
    return self._dao.get_products(cur)
  
  
  @service_decorator()
  def get_all_product_by_keyword(self, cur, keyword):
    return self._dao.get_products_by_keyword(cur, keyword)
  
  @service_decorator()
  def check_product_by_id(self, cur, id) -> bool:
    return self._dao.check_product_id_exists(cur, id) > 0

  @service_decorator()
  def get_product_by_id_to_print(self, cur, id) -> tuple[int, str, int, Optional[str | int]]:
    return self._dao.get_one_products_by_id_to_print(cur, id)

  # dao -> db 살아있는지 확인
  # 살이있으면 True 반환
  def heartbeat(self) -> bool:
    if self._dao is None or self.db is None:
      return False
    return True

