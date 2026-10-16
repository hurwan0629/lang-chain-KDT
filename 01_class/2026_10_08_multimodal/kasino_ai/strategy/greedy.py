from machine import Machine
import random
from .strategy import Strategy

class Greedy(Strategy):
  """현재까지 가장 좋은 결과가 있었던 선택을 합니다."""

  def __init__(self):
    pass

  def select_machine(self, status: dict[Machine, dict[str, int | float]]) -> Machine:

    max_q = max(record["q"] for record in status.values())

    candidates = [
        machine
        for machine, record in status.items()
        if record["q"] == max_q
    ]
    
    return random.choice(candidates)

  def __repr__(self) -> str:
    return "Strategy - greedy"