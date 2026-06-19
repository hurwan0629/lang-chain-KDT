from server.service import Service

def _message(message: str):
    print(f"""
          ┌──────────────────┐
          │    {message}    │ 
          └──────────────────┘
          """)
          
def show_all_page(service: Service):
  # 모든 장르 출력해주기
  genres = service.get_all_genres()

  if len(genres) == 0:
    _message("장르가 존재하지 않습니다 ㅠㅠ 장르를 먼저 추가해주세요")
    return

  print(f"|\t 고유번호 \t|\t 장르 \t|\t 생성일 \t|\t 활성화 여부 \t|")
  for g in genres:
     print(f"|\t {g.pk} \t|\t {g.name} \t|\t {g.created_at} \t|\t {"활성화" if g.available else "비활성화"} \t|")

