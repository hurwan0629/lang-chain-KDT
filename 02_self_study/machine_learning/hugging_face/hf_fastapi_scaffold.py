from functools import lru_cache

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(title="Hugging Face LLM Lab")


class ChatRequest(BaseModel):
    prompt: str = Field(min_length=1)


class ChatResponse(BaseModel):
    answer: str


@lru_cache(maxsize=1)
def get_generator():
    from transformers import pipeline

    return pipeline("text-generation", model="HuggingFaceTB/SmolLM2-135M-Instruct")


def run_llm(prompt: str) -> str:
    result = get_generator()(
        # 프롬프트 스키마만 넣어주면 자동으로 파이프라인을 통해 생성
        [{"role": "user", "content": prompt}],
        max_new_tokens=128,
        do_sample=False, # 확률적 샘플링을 할지
        return_full_text=False, # 반환 결과에 입력 프롬프트를 포함할지 결정
    )
    return result[0]["generated_text"]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    answer = run_llm(request.prompt)
    return ChatResponse(answer=answer)
