import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from app import ToolCall, app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_plan_supported_request():
    response = client.post(
        "/plan",
        json={"message": "지난주 미배송 주문 찾아줘"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "planned",
        "tool_call": {
            "name": "search_orders",
            "arguments": {"status": "pending", "period": "last_week"},
        },
    }


def test_plan_rejects_empty_message():
    response = client.post("/plan", json={"message": ""})

    assert response.status_code == 422


def test_plan_does_not_invent_a_tool():
    response = client.post(
        "/plan",
        json={"message": "노래 틀어줘"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "status": "no_tool",
        "tool_call": None,
    }


def test_unknown_tool_is_invalid():
    with pytest.raises(ValidationError):
        ToolCall.model_validate({
            "name": "delete_orders",
            "arguments": {"status": "pending", "period": "last_week"},
        })


def test_invalid_tool_argument_is_rejected():
    with pytest.raises(ValidationError):
        ToolCall.model_validate({
            "name": "search_orders",
            "arguments": {"status": "deleted", "period": "last_week"},
        })
