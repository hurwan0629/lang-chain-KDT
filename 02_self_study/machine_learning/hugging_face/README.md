# Agent Reliability Lab

자연어 요청을 **허용된 Tool Call**로 변환하고, 잘못된 호출을 검증하는 학습용 FastAPI 프로젝트입니다.

## 해결하려는 문제

LLM은 존재하지 않는 도구나 잘못된 인자를 만들어낼 수 있습니다.
따라서 **모델 출력과 실제 도구 실행 사이에 검증 계층**이 필요합니다.

처음에는 읽기 전용 가짜 도구 `search_orders` 하나만 다룹니다.
실제 주문 데이터 조회, 외부 API 호출, 모델 실행은 아직 하지 않습니다.

## 현재 범위 (MVP 0)

- `GET /health` — 서버 상태
- `POST /plan` — 자연어를 시험용 Tool Call로 변환
- `PlanRequest`, `ToolCall`, `PlanResponse` — Pydantic 계약
- `pytest` — 정상 요청, 비정상 요청, 허용되지 않은 도구/인자 검사

현재 `propose_tool_call()`은 **규칙 기반 스텁**입니다.
이는 LLM의 성능을 보여주는 코드가 아니며, 다음 단계에서 실제 모델 출력으로 교체합니다.

## 프로젝트 파일

```text
app.py              # API + 데이터 계약 + 임시 Planner
tests/test_app.py   # 첫 API 및 Schema 계약 테스트
README.md           # 프로젝트 범위와 실행법
TODO.md             # 확장 순서
hf_fastapi_scaffold.py  # 이전 FastAPI 연습 파일 (그대로 유지)
```

## 실행 (PowerShell)

기존 가상환경을 사용합니다.

```powershell
& "C:\LANG_CHAIN_2026\2026-05-19_KDT_lang_chain\.venv\Scripts\Activate.ps1"

python -m pip install fastapi uvicorn pytest httpx pydantic
python -m pytest -q
python -m uvicorn app:app --reload --port 8000
```

브라우저에서 `http://127.0.0.1:8000/docs`를 열어 API를 확인합니다.

### 요청 예시

```json
{"message": "지난주 미배송 주문 찾아줘"}
```

```json
{
  "status": "planned",
  "tool_call": {
    "name": "search_orders",
    "arguments": {"status": "pending", "period": "last_week"}
  }
}
```

지원하지 않는 요청은 `{"status": "no_tool", "tool_call": null}`을 반환합니다.

## 개발 원칙

1. 구현 전 입력/출력 계약과 실패 테스트를 먼저 작성합니다.
2. 외부 도구는 허용 목록과 Pydantic 스키마를 통과하기 전에는 실행하지 않습니다.
3. API 테스트와 **LLM 품질 평가**는 분리합니다.
4. 프롬프트·모델·평가 데이터의 버전을 기록하고 변경 전후 성능을 비교합니다.
5. 기능이 필요해질 때 파일과 클래스를 분리합니다. 지금은 구조를 최소화합니다.
