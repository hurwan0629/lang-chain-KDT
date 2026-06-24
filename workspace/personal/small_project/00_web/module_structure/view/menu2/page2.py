from server.service.service import Service
# from view.util.page_name import page_name
from collections.abc import Callable

class Page2:
  
  def __init__(self, service: Service):
    self.__service = service
  
  # ../util.page_name.py 에서 데코레이터로 속성 넣어줘서 찾았는데 그냥 메서드 하나 만들어서 관리하는게 편할거같아서 없앰
  # @page_name("페이지 이름")
  def _page2(self):

    while True:
      # 1. 페이지 출력
      # 2. 입력 받기 
      # 3. 프론트 유효값 검사
      # 4. service 사용
      # 5. 값 반환 및 break
      break
    
    return
  
  def get_page_services(self) -> list[tuple[str, Callable]]:
    return [
      ("page2 출력 명", self._page2),
    ]