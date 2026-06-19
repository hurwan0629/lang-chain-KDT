from view import Menu
from server import single_service

if __name__ == "__main__":
  app = Menu(single_service)
  app.run()