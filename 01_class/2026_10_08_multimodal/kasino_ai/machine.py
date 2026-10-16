import random

class Machine:
  def __init__(self, p=0.5):

    self.p = p

  def spin(self):
    return 1 if random.random() < self.p else 0

  def __repr__(self) -> str:
    return f"Machine (p={self.p})"

class MachineFactory:
  @staticmethod
  def create_machines() -> list[Machine]:
    probabilities = [0.2, 0.5, 0.1, 0.8, 0.3]
    return [Machine(p) for p in probabilities]
