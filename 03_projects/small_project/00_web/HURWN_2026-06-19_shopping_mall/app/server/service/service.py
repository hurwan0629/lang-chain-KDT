from .user_service import UserService
from .product_service import ProductService
from .order_service import OrderService

class Service(UserService, ProductService, OrderService):

  def __init__(self, dao, db):
    super().__init__(dao, db)