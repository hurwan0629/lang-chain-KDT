import time

from fastapi import FastAPI, status, HTTPException
import asyncio
from pydantic import BaseModel
from sqlalchemy import select

from database import SessionLocal
from models import Todo
from router import index_router

app = FastAPI()

class TodoCreateRequest(BaseModel):
    title: str
    content: str

class TodoUpdateRequest(BaseModel):
    content: str

app.include_router(index_router)
@app.get("/health")
def healthCheck():
    return {
        "message": "healthy"
    }
@app.get("/todo")
def getAllPost() :
    # 모든 todo 목록을 가져오기
    return {}

@app.get("/todo/{todo_id}")
def getPostById(todo_id: int):
    print(f"GET /todo/todo/{todo_id}")

    if todo_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="todo_id not found"
        )

    return {
        "meesage": f"todo: {todo_id}"
    }

@app.post(
    "/todo",
    status_code=status.HTTP_201_CREATED
)
def createPost(request: TodoCreateRequest):
    print("type request:", type(request))
    print("request:", request)
    print("request.title:", request.title)
    print("request.content:", request.content)

    with SessionLocal() as session:

        # Todo 함수를 이용해서
        new_todo = Todo(
            title=request.title,
            content=request.content
        )
        session.add(new_todo)

        session.flush()

        stmt = select(Todo)

        added_todo = session.scalars(stmt).first()

        print("added_todo type:", type(added_todo))
        print("added_todo:", added_todo)

        session.commit()

    return {
        "title": request.title,
        "content": request.content
    }

@app.patch("/todo/{todo_id}")
def updatePostContent(check: bool, todo_id: int, request: TodoUpdateRequest, query: str):
    print("todo_id:", todo_id)
    print("request:", request)
    print("query:", query)
    print("check:", check)
    return {
        "todo_id": todo_id,
        "request": request
    }

@app.post("/asyncio/{code}")
async def async_timer(code: int):
    print(f"asyncio-{code} start")
    corr = asyncio.sleep(2)
    print(f"asyncio-{code} corr:", type(corr))
    res = await corr
    print(f"asyncio-{code} res:", type(res))
    # time.sleep(1)
    print(f"asyncio-{code} end")
    return {
        "asyncio-result": "success",
        "code": code
    }

@app.post("/thread-pool/{code}")
def thread_timer(code: int):
    print(f"thread-timer:{code} start")
    time.sleep(2)
    print(f"thread-timer:{code} end")
    return {
        "message": "success"
    }