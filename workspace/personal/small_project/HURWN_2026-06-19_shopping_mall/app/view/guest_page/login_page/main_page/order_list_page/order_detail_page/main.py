from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number

class OrderPage(Page):
  def __init__(self, service: Service):
    self.__service = service

  def run_page(self):
    pass