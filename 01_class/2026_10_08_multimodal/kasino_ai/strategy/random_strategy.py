from machine import Machine
import random
from .strategy import Strategy

class RandomStrategy(Strategy):
  """항상 랜덤한 선택을 합니다."""

  def __init__(self, epsilon=0.1):
    self.epsilon = epsilon

  def select_machine(self, status: dict[Machine, dict[str, int | float]]) -> Machine:
      
    selected_machine = random.choice(list(status))
    
    return selected_machine
  
  def __repr__(self) -> str:
      return "Strategy - random"