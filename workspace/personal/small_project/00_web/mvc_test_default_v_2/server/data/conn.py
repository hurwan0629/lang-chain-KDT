import MySQLdb

def sql_dec(do_commit=False, cursor_type=None):
  def decorator(func):
    def with_conn(*args, **kwargs):
      result = None

      try:
        conn = MySQLdb.connect(host="localhost", user="root", password="1234", db="temp_db")
        cur = None
        if cursor_type is not None:
          cur = conn.cursor(cursor_type)
        else:
          cur = conn.cursor()

        try:

          s, *rest = args
          result = func(s, cur, *rest, **kwargs)

          if do_commit:
            conn.commit()
        
        except MySQLdb.Error as e:
          print(f"에러 발생")
          print(e)
          if do_commit:
            conn.rollback()
        except Exception as e:
          print(f"에러 발생")
          print(e)
          if do_commit:
            conn.rollback()
        finally:
          if cur is not None:
            cur.close()
          if conn is not None:
            conn.close()
      except Exception as e:
        print("DB/커서 연결 에러")
        print(e)

      return result
  
    return with_conn
  return decorator