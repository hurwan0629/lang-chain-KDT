from pydantic import BaseModel, ConfigDict

from database import get_session


class UserCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: str
    name: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pk: int
    id: str
    name: str

class OrderCreate(BaseModel):
    user_pk: int
    total_price: int

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    pk: int
    user_pk: int
    total_price: int

