from pydantic import BaseModel

class CreateUserRequest(BaseModel):
    id: str
    name: str