from .base_service import BaseService
from app.server.data.db_common.conn import service_decorator
from typing import Optional
from app.server.data.dto.user_regist_dto import UserRegistDTO
from app.server.data.dto.user_login_dto import UserLoginSuccessDTO

class UserService(BaseService):
  def __init__(self, dao, db):
    self.__dao = dao
    self.db = db
  
  # 특정 아이디가 존재하는지 확인
  @service_decorator()
  def check_id_duplicated(self, cur, id: str) -> bool:
    if self.__dao.check_id_exists(cur, id) >= 1:
      return True
    return False
  
  # 특정 이메일이 존재하는지 확인
  @service_decorator()
  def check_email_duplicated(self, cur, email: str) -> bool:
    if self.__dao.check_email_exists(cur, email) >= 1:
      return True
    return False
  
  # 회원가입 해주기
  # 실패하면 null 반환
  @service_decorator(commit=True)
  def regist_user(self, cur, id, password, name, email) -> Optional[UserRegistDTO | None]:
    return self.__dao.insert_user(cur, id, password, name, email)

  # 로그인 시도하기. 성공하면 UserLoginSuccessDTO 반환
  @service_decorator()
  def try_login(self, cur, username, password) -> Optional[UserLoginSuccessDTO | None]:
    result: Optional[UserLoginSuccessDTO | None] = self.__dao.login_check(cur, username, password) 
    return result
      
    






  def heartbeat(self) -> bool:
    if self.__dao is not None: 
      return True
    else:
      return False
  
