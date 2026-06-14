from data import *

class Todo_service:
  def __init__(self):
    self.__dao = Dao()
  
  def create_todo(self):
    title = input("할일 제목: ")
    content = input("할일 상세: ")

    result = self.__dao.insert(dto_insert=Dto_insert(todo_title=title, todo_content=content))

    if result is None:
      print("에러")
    elif result > 0:
      print("생성 완료")
  
  def show_all_list(self):
    results = self.__dao.select_all()
    if results is None:
      print("에러")
    elif len(results) <= 0:
      print("검색 결과 0건")
      return

    for r in results:
      print(r)

  def search_title(self):
    title = input("검색어를 입력하세요: ")

    results = self.__dao.search_by_title(todo_title=title)

    if results is None:
      print("에러")
    elif len(results) <= 0:
      print("검색 결과 0건")
      return

    for r in results:
      print(r)
    
  def delete_todo(self):
    todo_pk = input("삭제할 pk를 입력하세요: ")

    result = self.__dao.delete(dto_delete=Dto_delete(int(todo_pk)))
    if result is None:
      print("에러")
    elif result > 0:
      print("삭제 완료")
    else:
      print("삭제 0건")
  
  def update_todo(self):
    pk = int(input("수정할 pk를 입력하세요: "))
    content = input("덮어씌울 내용을 입력하세요: ")
    result = self.__dao.update(dto_update=Dto_update(todo_pk=pk, todo_content=content))
    if result is None:
      print("에러")
    elif result > 0:
      print("업데이트 완료")
    else:
      print("업데이트 0건")
  