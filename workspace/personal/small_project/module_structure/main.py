from view import App
from server import *




if __name__ == "__main__":
  service = ServiceImpl()
  app = App(service)
  
  app.run()