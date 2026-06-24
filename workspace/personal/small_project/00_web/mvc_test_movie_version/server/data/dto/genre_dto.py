from dataclasses import dataclass
from datetime import datetime

@dataclass
class GenreDTO:
  pk: int
  name: str
  created_at: datetime
  available: bool