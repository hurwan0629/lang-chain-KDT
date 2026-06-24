from server.service import Service
from view.genre.show_all import show_all_page

def _message(message: str):
    print(f"""
          ┌──────────────────┐
          │    {message}    │ 
          └──────────────────┘
          """)

def _get_string(message: str, max_length: int) -> str:
  max_length = max_length if max_length >0 else 2
  while True:
    _message(message)
    try:
       user_input = input(message)
       if not (0 < len(user_input) <= max_length):
          raise ValueError
       
       return user_input
    except ValueError:
      _message(f"글자 수가 1 ~ {max_length} 이여야 합니다!")

def _get_number(message: str, number_list: list[int]):
  while True:
    _message(message)
    try:
       user_input = int(input(message))
       if user_input not in number_list:
          raise ValueError
       
       return user_input
    except Exception:
      _message(f"{number_list} 중 하나를 골라주세요")

def add_movie_page(service: Service):
  # 사용자에게 받을 값:
  # [제목] [부제목] [장르pk]
  title = _get_string("추가할 영화 제목을 입력해주세요!", 50)
  subtitle = _get_string("추가할 영화 부제목을 입력해주세요!",100)
  
  show_all_page(service)

  genre_pk = _get_number("위 장르에서 장르번호를 입력해주세요!", )



