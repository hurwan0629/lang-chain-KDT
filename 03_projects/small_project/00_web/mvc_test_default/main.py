from service import Todo_service

class Menu:
  def __init__(self):
    self.service = Todo_service()
    
    # 함수 - callable = ()

    self.menu = {
      1: self.service.create_todo,
      2: self.service.show_all_list,
      3: self.service.search_title,
      4: self.service.update_todo,
      5: self.service.delete_todo
    }

  def run(self):
    while True:
      print()
      print("===== Todo 프로그램 =====")
      print("1. 할 일 등록")
      print("2. 할 일 전체 조회")
      print("3. 제목으로 검색")
      print("4. 할 일 수정")
      print("5. 할 일 삭제")
      print("6. 프로그램 종료")

      try:
        menu = int(input("메뉴를 선택하세요: ")) # menu = int("5")
      except ValueError:
        print("숫자를 입력해주세요.")
        continue

      try:
        
        func = self.menu.get(menu, None) # self.menu(5, None) -> func = self.service.delete_todo
        
        if func is not None:
          func() # self.service.delete_todo()

        elif menu == 6:
          print("프로그램을 종료합니다.")
          break
        
        else:
          print("메뉴는 1부터 6까지만 선택할 수 있습니다.")
        
      except ValueError:
        print("입력값의 형식이 올바르지 않습니다.")
      except Exception as e:
        print("오류:", e)


if __name__ == "__main__":
  menu = Menu()
  menu.run()

  menu2 = Menu()
  menu2.run()
