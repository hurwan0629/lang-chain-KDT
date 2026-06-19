from abc import ABC, abstractmethod
from server.data.db_common.conn import dao_decorator

class Service(ABC):
  def __init__(self, dao):
    self.__dao = dao
    
  @abstractmethod
  def first_service(self):
    pass

  @abstractmethod
  def heartbeat(self):
    # dao -> db 살아있는지 확인
    # 살이있으면 True 반환
    pass
