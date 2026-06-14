from .conn import sql_dec
from .Todo_dto import Todo_dto_insert as Dto_insert
from .Todo_dto import Todo_dto_update as Dto_update
from .Todo_dto import Todo_dto_delete as Dto_delete
import MySQLdb
from MySQLdb.cursors import DictCursor

class Todo_dao():
  
  # SQL
  sql_select_all = "select todo_pk, todo_title, todo_content, created_at, updated_at from todo"
  sql_search_by_title = "select todo_pk, todo_title, todo_content, created_at, updated_at from todo where todo_title like concat('%', %s, '%')"
  sql_insert = "insert into todo (todo_title, todo_content) values (%s, %s)"
  sql_update = "update todo set todo_content = %s, updated_at = now() where todo_pk = %s"
  sql_delete = "delete from todo where todo_pk = %s"



  def __init__(self):
    pass

  @sql_dec(cursor_type=DictCursor)
  def search_by_title(self, cur, todo_title):
    cur.execute(self.sql_search_by_title, (todo_title, ))

    return cur.fetchall()

  @sql_dec(cursor_type=DictCursor)
  def select_all(self, cur):
    cur.execute(self.sql_select_all)
    return cur.fetchall()

  
  @sql_dec(do_commit=True)
  def insert(self, cur, dto_insert: Dto_insert):
    return cur.execute(self.sql_insert, (dto_insert.todo_title, dto_insert.todo_content))

  @sql_dec(do_commit=True)
  def update(self, cur, dto_update: Dto_update):
    return cur.execute(self.sql_update, (dto_update.todo_content, dto_update.todo_pk))

  @sql_dec(do_commit=True)
  def delete(self, cur, dto_delete: Dto_delete):
    return cur.execute(self.sql_delete, (dto_delete.todo_pk, ))
  