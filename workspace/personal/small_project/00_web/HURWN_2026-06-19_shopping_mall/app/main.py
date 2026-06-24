from .server.data.db_common import app_db_decorator
from .server.service.service import Service
from .view.main import StartPage
from .server.data.dao import Dao

# 실제로 실행시켜줄 작업
class App:
  def __init__(self):
    print(f"[ {__name__} ] 앱 실행")

  @app_db_decorator
  def run_app(self, db):
    print(f"[ {__name__} ] run_app() 시작합니다.")
    print(f"[ {__name__} ] DB: {db}")

    dao = Dao()

    service = Service(dao, db)

    # View (컨트롤러 겸 페이지 객체 생성)
    page = StartPage(service)

    page.run_page()




def run_app():
  
  # # # DAO 생성 # # # 


  # # # Service 생성 # # # 
  app = App()

  app.run_app()