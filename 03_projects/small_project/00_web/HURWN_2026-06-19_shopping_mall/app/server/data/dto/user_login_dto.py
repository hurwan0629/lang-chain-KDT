from dataclasses import dataclass

@dataclass
class UserLoginSuccessDTO:
  """pk"""
  id: int
  """사용자 아이디"""
  username: str 
  """사용자 이름"""
  name: str