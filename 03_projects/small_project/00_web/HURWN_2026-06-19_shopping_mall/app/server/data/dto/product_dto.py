from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductDTO:
  id: int
  name: str
  price: int
  stock: int
  created_at: datetime