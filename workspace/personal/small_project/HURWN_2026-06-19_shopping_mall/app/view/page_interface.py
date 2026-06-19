from abc import ABC, abstractmethod
from app.server.service.service import Service
from collections.abc import Callable

class Page(ABC):
  
  @abstractmethod
  def __init__(self, service: Service):
    pass
  
  @abstractmethod
  def run_page(self):
    pass

  # """ 
  # 자신이 가지고 있는 페이지들을
  # return [
  #     ("page2 출력 명", self._page2),
  #   ]
  # 형태로 
  # """
  # @abstractmethod
  # def get_page_services(self) -> list[tuple[str, Callable]]:
  #   pass
