from app.view.page_interface import Page
from .guest_page.main import GuestPage
from app.server.service.service import Service

class StartPage(Page):
  def __init__(self, service: Service):
    self.guest_page = GuestPage(service)
  
  def run_page(self):
    self.guest_page.run_page()
