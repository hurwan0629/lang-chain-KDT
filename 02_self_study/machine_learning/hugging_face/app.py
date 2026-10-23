from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field


app = FastAPI(title="Agent Reliability Lab")


class PlanRequest(BaseModel):
    message: str = Field(min_length=1, max_length=500)


class SearchOrdersArgs(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal["pending"]
    period: Literal["last_week"]


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: Literal["search_orders"]
    arguments: SearchOrdersArgs


class PlanResponse(BaseModel):
    status: Literal["planned", "no_tool"]
    tool_call: ToolCall | None


def propose_tool_call(message: str) -> dict | None:
    # 임시 규칙 기반 구현. 추후 LLM 출력으로 교체합니다.
    text = message.replace(" ", "")

    if (
        "지난주" in text
        and "주문" in text
        and ("미배송" in text or "배송되지않" in text)
    ):
        return {
            "name": "search_orders",
            "arguments": {"status": "pending", "period": "last_week"},
        }

    return None


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/plan", response_model=PlanResponse)
def plan(request: PlanRequest) -> PlanResponse:
    candidate = propose_tool_call(request.message)

    if candidate is None:
        return PlanResponse(status="no_tool", tool_call=None)

    return PlanResponse(
        status="planned",
        tool_call=ToolCall.model_validate(candidate),
    )
