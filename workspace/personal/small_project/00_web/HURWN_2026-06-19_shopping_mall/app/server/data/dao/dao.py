from .user_dao import UserDAO
from .product_dao import ProductDAO
from .order_dao import OrderDAO

class Dao(UserDAO, ProductDAO, OrderDAO):
  def __init__(self):
    super().__init__()