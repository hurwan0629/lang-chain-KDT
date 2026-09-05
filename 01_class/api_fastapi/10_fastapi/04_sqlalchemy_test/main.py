# main.py
from fastapi import FastAPI
from router.test_router import router
app = FastAPI()

app.include_router(router)