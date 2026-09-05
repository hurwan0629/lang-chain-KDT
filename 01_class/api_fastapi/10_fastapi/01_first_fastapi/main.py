from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# HTML 페이지 제공
# 어노테이션을 이용해서
@app.get("/api/data")
async def get_data(request: Request):
    return { "message": "서버에서 보내는 메시지 입니다." }

@app.get("/", response_class=HTMLResponse)
async def get_page(request: Request):
    return templates.TemplateResponse({"request": request}, "index.html")
