from abc import ABC, abstractmethod
from app.server.data.db_common.conn import service_decorator

class BaseService(ABC):
  def __init__(self, dao, db):
    self.__dao = dao
    selfdb = db

  @abstractmethod
  def heartbeat(self) -> bool:

    # dao -> db 살아있는지 확인
    # 살이있으면 True 반환
    pass
