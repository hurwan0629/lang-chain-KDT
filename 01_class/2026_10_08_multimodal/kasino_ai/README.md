# 슬롯머신 AI

슬롯머신 5대에서 보상을 얻으며 머신별 당첨 확률을 추정하는 실습입니다.
Random, Greedy, Epsilon-Greedy 전략을 각각 1,000회 실행해 비교합니다.

## 읽는 순서

`todo.md` → `machine.py` → `strategy/strategy.py` → 전략 구현체 3개 → `agent.py` → `run.py` → `run/`의 결과 JSON 순서로 읽습니다.
실행 흐름은 `run.py`의 실험 준비 → `Player.play()` → 전략의 머신 선택 → 보상 획득과 기록 갱신 → JSON 저장입니다.

## 파일과 폴더

```text
kasino_ai/
├── README.md
├── todo.md
├── machine.py
├── agent.py
├── run.py
├── test.ipynb
├── strategy/
│   ├── strategy.py
│   ├── random_strategy.py
│   ├── greedy.py
│   └── epsilon_greedy.py
└── run/
    └── <실행시각>_<전략명>.json
```

### `todo.md`

과제 조건과 구현 목표를 정리한 파일입니다.
당첨 확률, 전략 종류, 학습 기록, 실험 출력 조건을 담고 있습니다.
코드를 읽기 전에 전체 요구사항을 확인할 때 사용합니다.

### `machine.py`

`Machine`은 당첨 시 1, 실패 시 0의 보상을 반환합니다.
`MachineFactory.create_machines()`는 당첨 확률이 `[0.2, 0.5, 0.1, 0.8, 0.3]`인 머신 5대를 생성합니다.
실제 당첨 확률은 보상 판정에 사용하며, 전략은 플레이어가 기록한 추정값으로 선택합니다.

### `strategy/` 폴더

머신을 선택하는 규칙을 모아 둔 폴더입니다.
공통 추상 클래스와 전략 구현체 3개로 구성됩니다.
전략은 다음 머신만 선택하고, 실행과 학습 기록 갱신은 `Player`가 담당합니다.

### `strategy/strategy.py`

모든 전략이 따르는 추상 클래스 `Strategy`를 정의합니다.
`select_machine(status)`는 머신별 기록을 받아 선택한 `Machine` 객체를 반환합니다.
구현체는 이 메서드에 각자의 선택 규칙을 작성합니다.

### `strategy/random_strategy.py`

`RandomStrategy`는 전체 머신 중 하나를 무작위로 선택합니다.
선택할 때 평균 보상 추정값 `q`를 사용하지 않습니다.
다른 전략의 성능을 비교하는 기준으로 사용합니다.

### `strategy/greedy.py`

`Greedy`는 현재 `q`가 가장 높은 머신을 선택합니다.
최댓값이 같은 머신이 여러 개면 그중 하나를 무작위로 선택합니다.
현재 추정값을 우선하므로 초기 결과에 따라 선택이 치우칠 수 있습니다.

### `strategy/epsilon_greedy.py`

`EpsilonGreedy`는 epsilon 확률로 전체 머신 중 하나를 무작위로 선택합니다.
나머지 확률로는 `q`가 가장 높은 머신을 선택하며, 동점이면 무작위로 결정합니다.
`run.py`에서는 epsilon이 0.1인 경우와 0.01인 경우를 각각 실험합니다.

### `agent.py`

`Player`는 머신 목록, 전략, 남은 횟수, 보상 기록을 관리합니다.
`set_strategy()`로 선택 규칙을 설정하고, `play()`를 호출할 때마다 한 번 선택하고 학습합니다.
머신별 선택 횟수 `spin_count`, 누적 보상 `score`, 평균 보상 추정값 `q`를 갱신합니다.
반환값의 `idx`는 0부터 시작하는 머신 인덱스이며, `status`는 선택한 머신의 갱신된 기록입니다.

### `run.py`

상단의 `STRATEGIES`에 등록된 네 실험을 순서대로 실행합니다.
실험마다 새 플레이어와 머신을 만들고, `SPINS`에 지정한 횟수만큼 `play()`를 반복합니다.
매 실행의 머신 선택, 보상, 상태 변경 전후를 복사해 기록합니다.
종료 후 결과 요약을 터미널에 출력하고, 실험당 JSON 하나를 `run/`에 저장합니다.

### `test.ipynb`

머신 생성과 보상 기록을 셀 단위로 확인하는 실습 노트북입니다.
앞부분에는 초기 구현을 실험한 코드가 남아 있습니다.
현재 전체 전략 실험은 `run.py`를 실행해 확인합니다.

## 실행 방법

Python 3.12 환경에서 `kasino_ai` 폴더를 작업 경로로 설정합니다.
실행 코드는 파이썬 표준 라이브러리만 사용하므로 추가 패키지 설치가 필요 없습니다.

```bash
python run.py
```

실험 횟수는 `run.py`의 `SPINS`에서 변경합니다.
실행할 전략과 epsilon 값은 `STRATEGIES`에서 변경합니다.

## 결과 파일

### `run/` 폴더와 JSON

`run/`은 `run.py`와 같은 위치에 자동 생성되는 결과 폴더입니다.
기본 설정에서는 실행할 때마다 JSON 4개가 생성되며, 한국 시각과 마이크로초를 파일명에 넣어 기존 결과를 보존합니다.
JSON의 `strategy`와 `epsilon`은 실험 설정이고, `steps`는 매 실행의 선택 머신 번호, 보상, 누적 보상, 선택한 머신의 변경 전후 기록입니다.
`summary`는 총 실행 횟수, 총보상, 전체 보상 리스트, 가장 많이 선택한 머신 번호, 머신별 최종 기록을 담습니다.

```text
run/
├── <실행시각>_random.json
├── <실행시각>_greedy.json
├── <실행시각>_epsilon_greedy_0.1.json
└── <실행시각>_epsilon_greedy_0.01.json
```

결과 JSON의 머신 번호는 1부터 5까지 표시합니다.
실행할 때마다 난수를 새로 뽑으므로 보상과 선택 기록은 달라질 수 있습니다.
