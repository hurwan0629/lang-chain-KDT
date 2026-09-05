import fastapi
from fastapi import FastAPI

index_router = fastapi.APIRouter(
    prefix="/message",
    tags=["plain"]
)

@index_router.get("/hello/{name}")
def answer_gretting(name: str):
    return {
        "message": f"hello i'm {name}"
    }