from dataclasses import dataclass

@dataclass
class UserRegistDTO:
  id: str
  password: str
  name: str
  email: str

