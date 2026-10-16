from machine import Machine
import random
from .strategy import Strategy

class EpsilonGreedy(Strategy):
  """기본 행동은 현재까지 가장 좋은 결과가 있었던 선택을 하며 epsilon 확률로 랜덤 확률을 선택하는 전략입니다."""

  def __init__(self, epsilon=0.1):
    self.epsilon = epsilon

  def select_machine(self, status: dict[Machine, dict[str, int | float]]) -> Machine:

    is_greedy = False if random.random() < self.epsilon else True

    if is_greedy:
      # 만약 공동 1위가 존재하면 먼저 걸리는거 선택
      max_q = max(record["q"] for record in status.values())
      
      candidates = [
        machine
        for machine, record in status.items()
        if record["q"] == max_q
      ]
      
      return random.choice(candidates)
    else:
      return random.choice(list(status))

  def __repr__(self) -> str:
    return "Strategy - epsilon greedy"