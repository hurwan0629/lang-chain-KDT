from pydantic import BaseModel


class PostRequest(BaseModel):
    product_name: str
    details: str
    tone_and_manner: str