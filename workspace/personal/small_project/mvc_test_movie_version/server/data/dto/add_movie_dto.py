from dataclasses import dataclass
from datetime import datetime

@dataclass
class AddMovieDTO:
  title: str
  subtitle: str
  genre_pk: int