import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import database
from app.llm_api.llm_module import get_advertise_content_string
from app.dto.request import PostRequest

app = FastAPI()

origins = [
    "http://127.0.0.1:7860/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/datas")
def get_all_contents():
    """모든 DB의  [요청기록/생성 문구] 를 사용자에게 반환해주기"""
    print("get_all_contents")

    datas = database.get_all_data()
    return { "datas": datas }



@app.post("/content")
async def create_and_persist_content(
        request: PostRequest
):
    """사용자의 요청에 따라 api를 통해 문구를 생성 후 DB에 저장, 사용작에게 반환해주기"""

    print("create_and_persist_content:", request)

    api_reponse_content = await get_advertise_content_string(
        product_name=request.product_name,
        details=request.details,
        tone_and_manner=request.tone_and_manner,
    )

    data = database.insert_data(
        product_name=request.product_name ,
        details=request.details,
        tone_and_manner=request.tone_and_manner,
        ad=api_reponse_content,
        created_at=datetime.datetime.now(),
    )

    return data