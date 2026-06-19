import MySQLdb
from functools import wraps

def app_db_decorator(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    _db = None
    try:

      _db = MySQLdb.connect(
        host="localhost",
        user="root",
        password="1234",
        db="test"
      )
      func(_db, *args, **kwargs)
    except MySQLdb.Error as e:
      print("서버 시작 오류:")
      print(e)
    
    finally:
      if _db is not None:
        _db.close()
    
  return wrapper

def dao_decorator(commit: bool = False):
  def my_decorator(func):
    @wraps(func)
    # # # # [커서 연결 후 수행] # # # #
    def wrapper(self, *args, **kwargs):
      if self.db is None:
        raise Exception(f"[{type(self).__name__} 에러] dao의 db가 정의되어있지 않습니다.")
      cur = self.db.cursor()
      try:

        result = func(self, cur, *args, **kwargs)
        
        if commit:
          self.db.commit()
        
        return result
      
      # # # # [에러 탐지] # # # #
      except MySQLdb.Error as e:
        print(f"[DB 에러] {e}")
        if commit and cur is not None:
          self.db.rollback()
          return None

      except Exception as e:
        print(f"[예상하지 못한 에러] {e}")
        if commit and cur is not None:
          self.db.rollback()
          return None

      # # # # [커서 닫기] # # # #
      finally:
        if cur is not None:
          cur.close()
        
  
    return wrapper
  return my_decorator
