from abc import ABC, abstractmethod
from server.data.db_common.conn import dao_decorator

class Table1DAO(ABC):
  
  @abstractmethod
  def __init__(self, db):
    self.db = db
  
  @abstractmethod
  @dao_decorator()
  def db_action(self, cur):
    pass