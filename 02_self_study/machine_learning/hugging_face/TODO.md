# TODO — Agent Reliability Lab

## 0. 현재: 계약과 최소 실행 흐름
- [x] 해결 문제와 MVP 범위를 README에 정의
- [x] `GET /health`, `POST /plan` 계약 작성
- [x] API/스키마 테스트 먼저 작성
- [x] 실제 LLM 없는 규칙 기반 Planner 구현
- [ ] **로컬 가상환경에서 pytest 실행하고 결과 확인**
- [ ] /docs에서 정상 요청과 오류 요청 직접 보내보기

## 1. LLM을 연결할 준비
- [ ] `propose_tool_call()`의 입력/출력 타입 다시 설계
- [ ] Prompt v1 작성: 허용 도구 목록과 JSON 출력 형식
- [ ] 잘못된 LLM 출력(존재하지 않는 Tool/잘못된 타입) 테스트
- [ ] 모델은 서버에서 한 번만 로드하도록 수명주기 설계

## 2. 평가 기준부터 만들기
- [ ] 정상/거부/모호한 요청을 포함한 평가 사례 20~30개
- [ ] Tool 선택 정확도, 인자 정확도, 잘못된 실행 허용률 정의
- [ ] Baseline 결과 기록 후 Prompt와 생성 옵션 비교

## 3. 실제 LLM 및 스트리밍
- [ ] Transformers Pipeline 또는 직접 generate() 연결
- [ ] 추론 지연시간과 오류 기록
- [ ] SSE 이벤트 명세(start, status, done, error) 정의
- [ ] 스트리밍의 정상 종료·오류·연결 해제 테스트

## 4. 이후 실험
- [ ] 모델 버전(revision)과 실행 환경 고정
- [ ] 개선이 필요한 실패 유형을 분류
- [ ] LoRA 학습 필요성 판단 및 소규모 비교 실험
- [ ] FastAPI 리소스 제한·동시성·타임아웃 점검

## 이번 학습에서 직접 설명할 내용
- [ ] `response_model=PlanResponse`와 `-> PlanResponse`는 어떻게 다른가?
- [ ] `Literal["search_orders"]`는 왜 Tool Call의 허용 목록이 되는가?
- [ ] 왜 Planner의 출력을 실행 전에 검증해야 하는가?

**범위 제한:** 지금은 외부 API 호출, 데이터베이스, Agent 프레임워크, Fine-tuning, 실제 스트리밍을 구현하지 않습니다.
