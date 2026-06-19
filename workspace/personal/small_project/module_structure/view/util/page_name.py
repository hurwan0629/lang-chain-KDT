from collections.abc import Callable
from typing import Any

def page_name(name: str):
  def wrapper(func):
    func.__page_name__ = name
    return func
  
  return wrapper

def get_page_name(method: Callable) -> str:
  func = getattr(method, "__func__", method)
  return getattr(func, "__page_name__")