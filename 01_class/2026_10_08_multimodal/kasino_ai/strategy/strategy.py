from abc import ABC, abstractmethod
from machine import Machine

class Strategy(ABC):
  """
  진행 전략을 가지고 에이전트가 해당 전략대로 진행하게 만들어냅니다.
  
  Player 클래스의 .set_strategy(Strategy) 메서드를 이용하여 행동 전략을 수립한 뒤 
  play() 를 통해 학습을 하게 만들 수 있습니다.
  """

  def __init__(self):
    pass

  @abstractmethod
  def select_machine(self, status: dict[Machine, dict[str, int | float]]) -> Machine: 
    """
    현재 player이 가지고 있는 Machine과 그에 대한 spin_count, score, q 를 이용하여
    다음으로 돌릴 Machine 객체를 반환해줍니다.
    """
    pass

  def __repr__(self) -> str:
    return super().__repr__()