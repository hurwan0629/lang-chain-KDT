from .user_service import UserService

class Service(UserService):

  def __init__(self, dao, db):
    super().__init__(dao, db)