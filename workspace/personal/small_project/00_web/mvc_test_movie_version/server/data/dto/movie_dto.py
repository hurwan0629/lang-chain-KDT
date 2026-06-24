from dataclasses import dataclass
from datetime import datetime

@dataclass
class MovieDTO:
  pk: int
  title: str
  subtitle: str
  genre: str
  release_at: datetime
  deleted: bool