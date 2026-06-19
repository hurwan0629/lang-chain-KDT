import MySQLdb
from app.server.data.dto.user_regist_dto import UserRegistDTO
from typing import Optional

class UserDAO:

  sql_check_id_exists = "select 1 from member where id = %s"
  sql_check_email_exists = "select 1 from member where email = %s"
  sql_insert_user = "insert into member (username, password, name, email) values (%s, %s, %s, %s)"
  sql_login_check = "select id, username, name from member where username = %s and password = %s"

  """아이디 존재하는지 확인"""
  def check_id_exists(self, cur, id: str) -> int: 
    return cur.execute(self.sql_check_id_exists, (id, ))
  
  """이메일 존재하는지 확인"""
  def check_email_exists(self, cur, email: str) -> int:
    return cur.execute(self.sql_check_email_exists, (email, ))

  """회원가입 시켜주기"""
  def insert_user(self, cur, id, password, name, email) -> Optional[UserRegistDTO | None]:
      
    if cur.execute(self.sql_insert_user, (id, password, name, email, )) > 0:
      return UserRegistDTO(id, "", name, email)
    return None
  
  """로그인 시도"""
  def login_check(self, cur, username: str, password: str):
    result = cur.execute(self.sql_login_check, (username, password))
    obj= cur.fetchone()