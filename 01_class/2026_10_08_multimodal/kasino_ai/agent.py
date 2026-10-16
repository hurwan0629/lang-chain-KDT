from machine import Machine
from strategy.strategy import Strategy

class Player:

  def __init__(self, left_spin=1000):
    self.left_spin = left_spin
    """
    {
      Machine: {
        spin_count: 0,
        score: 0,
        q: 0.0 
      }
    }
    """
    self.status: dict[Machine, dict[str, int | float]] = {}
    self.strategy: Strategy | None = None
    self.rewards: list[int] = []
    self.total_reward = 0

    # 돌릴 수 있는 슬롯머신
    self.choice: list[Machine] = []

  def append_choice(self, machine: Machine):
    if machine in self.choice:
      raise Exception("중복된 슬롯머신이 이미 존재합니다.")

    self.choice.append(machine)
    self.status[machine] = {
      "spin_count": 0,
      "score": 0,
      "q": 0.0,
    }

  def get_choice_len(self):
    return len(self.choice)

  def current_status(self):
    return self.status

  def get_status(self):
    return self.status

  def _spin_machine(self, index):
    if self.left_spin <= 0:
      raise ValueError("남은 실행 횟수가 없습니다.")

    if not 0 <= index < len(self.choice):
      raise IndexError("존재하지 않는 슬롯머신입니다.")

    selected_machine: Machine = self.choice[index]
    self.left_spin -= 1
    result = selected_machine.spin()

    self.rewards.append(result)
    self.total_reward += result

    status = self.status.setdefault(
      selected_machine, # q는 추정 확률
      {"spin_count": 0, "score": 0, "q": 0.0}
    )

    status["spin_count"] += 1
    status["score"] += result
    # 나온 수에서 기존의 확률을 뺴고 다시 확률로 가하면 
    # (q(n-1) + result) / n = q + (result-q)/n
    status["q"] += (result - status["q"]) / status["spin_count"]

    return { "idx": index, "status": status }

  def set_strategy(self, strategy_choice: Strategy):
    self.strategy = strategy_choice

  def current_strategy(self) -> str:
    if self.strategy == None:
      return "Strategy - None"
    return str(self.strategy)

  def play(self):
    if self.strategy == None:
      raise Exception("set_strategy(Strategy)를 통해 전략을 설정해주세요")
    
    selected_machine = self.strategy.select_machine(self.status)
    index = self.choice.index(selected_machine)
    return self._spin_machine(index)
