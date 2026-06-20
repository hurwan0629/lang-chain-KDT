# 메뉴 번호 입력받기
"""tuple(menu_title: 메뉴 제목, menu: ((메뉴 번호, 메뉴 내용), ... )) 입력 시 순서대로 출력됩니다."""
def get_menu_number(menu_info: tuple[str, tuple[tuple[int, str], ...]]) -> int:
  menu_title = menu_info[0]
  menu = menu_info[1]

  available_number = [a for (a, s) in menu]

  while True:
    print("\n"*10)
    print("==========================")
    print(f"  {menu_title}")
    print("==========================")
    for m in menu:
      print(f"{m[0]}. {m[1]}")
    print("==========================")
    try:
      user_input = int(input("메뉴 번호를 선택하세요: "))
      
      if user_input not in available_number:
        raise Exception

      return user_input
    except Exception:
      input("올바른 메뉴 번호를 입력해주세요 (아무키나 입력)" )

  
# 회원가입 페이지 폼
