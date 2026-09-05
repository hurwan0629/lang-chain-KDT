class Todo_dto_insert():

  def __init__(self, todo_title, todo_content):
    self.todo_title = todo_title
    self.todo_content = todo_content
  
  def __repr__(self):
    return f"""
    Todo_dto(
      todo_title='{self.todo_title}',
      todo_content='{self.todo_content}',
    )
    """

  @property
  def todo_title(self):
    return self.__todo_title

  @todo_title.setter
  def todo_title(self, todo_title):
    if not todo_title:
      raise ValueError("제목은 존재해야합니다")
    self.__todo_title = todo_title


  @property
  def todo_content(self):
    return self.__todo_content

  @todo_content.setter
  def todo_content(self, todo_content):
    if not todo_content:
      raise ValueError("내용은 존재해야합니다.")
    self.__todo_content = todo_content













class Todo_dto_update():

  def __init__(self, todo_pk, todo_content):
    self.todo_pk = todo_pk
    self.todo_content = todo_content
  
  def __repr__(self):
    return f"""
    Todo_dto(
      todo_pk='{self.todo_pk}',
      todo_content='{self.todo_content}'
    )
    """
  
  @property
  def todo_pk(self):
    return self.__todo_pk

  @todo_pk.setter
  def todo_pk(self, todo_pk):
    self.__todo_pk = todo_pk

  @property
  def todo_content(self):
    return self.__todo_content
  
  @todo_content.setter
  def todo_content(self, todo_content):
    self.__todo_content = todo_content


class Todo_dto_delete():

  def __init__(self, todo_pk):
    self.todo_pk = todo_pk
  
  def __repr__(self):
    return f"""
    Todo_dto(
      todo_pk='{self.todo_pk}'
    )
    """
  
  @property
  def todo_pk(self):
    return self.__todo_pk

  @todo_pk.setter
  def todo_pk(self, todo_pk):
    self.__todo_pk = todo_pk