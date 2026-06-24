from .service import Service
from server.data.dao.table1_dao import Table1DAO
from server.data.dao.table2_dao import Table2DAO

class ServiceImpl(Service):
  def __init__(self):
    self.__dao = Table1DAO()