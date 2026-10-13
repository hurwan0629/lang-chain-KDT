# Prompts to send to Codex

## First run (copy into Codex)

`AGENTS.md`, `SPEC.md`, `TASKS.md`를 먼저 읽어. 기존 구현물이 없는 새 프로젝트야. 너는 이 프로젝트의 구현 및 검증을 담당하는 코딩 에이전트야. M0만 구현해. 작업 전에는 파일 구조와 짧은 실행 계획을 제시하고, 작업 후에는 실제 실행한 테스트 명령과 결과를 보고해. M0 완료 조건을 통과한 경우에만 TASKS.md를 갱신해. 아직 M1 이상의 구현을 시작하지 마. 외부 LLM API 또는 사전학습 모델은 사용하지 마.

## Continue (copy into Codex after each phase)

`AGENTS.md`, `SPEC.md`, `TASKS.md`를 다시 확인하고, 가장 먼저 남아 있는 미완료 마일스톤 하나만 구현해. 테스트와 CPU smoke를 실제 실행하고 실패를 수정해. 각 체크리스트 항목의 증거를 남기고, 의도하지 않은 코드 변경이 없는지 점검해. 테스트를 통과하지 못하면 완료로 표시하지 마. 구현한 모듈의 데이터 흐름과 주요 텐서 shape를 나에게 설명해.

## Architecture review (optional)

현재까지의 코드를 아키텍처 관점에서 검토해. 특히 (1) causal mask leakage, (2) 라우터 top-k 구현, (3) sparse MoE가 실제로 선택된 expert만 연산하는지, (4) train/validation leakage, (5) 도구 호출 보안, (6) mock model과 trained model의 차이를 확인해. 발견된 문제는 재현 테스트를 먼저 추가하고 수정해. 추측과 실제 테스트 결과를 구분해서 보고해.

## Experimental comparison (after M3/M4)

Dense FFN과 MoE를 같은 데이터, 시드, 비교 가능한 연산 예산으로 실험해. 파라미터 수, 토큰당 활성 파라미터, train/validation loss, expert 사용 분포, wall-clock 시간을 표로 정리하고 CPU/GPU 및 설정을 명시해. 결과가 유의미하지 않으면 그렇게 보고해.
