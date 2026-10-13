# Mini MoE Lab

LLM과 MoE 구조를 직접 구현하고 학습하는 로컬 연구·교육용 Python 프로젝트입니다.
현재 **M0: 실행 환경 검증**, **M1: 합성 데이터와 토크나이저**를 구현했습니다.
외부 LLM API, 사전학습 모델, 데이터 다운로드를 사용하지 않습니다.
개발을 담당하는 Codex와 이후 구현할 `agent/` 런타임 하네스는 별개입니다.

## 설치

Python 3.11 이상이 필요합니다. 아래 CPU 설치 경로는 CPython 3.12를 기준으로 합니다.
최초 설치에는 패키지 다운로드가 필요하며, 설치 후 테스트와 M0/M1 smoke는 오프라인으로 실행됩니다.
PyTorch, NumPy, pytest 버전은 `pyproject.toml`에 고정합니다.

Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m mini_moe.environment --seed 42
```

MSYS Python이 PATH에 잡힌 경우에도 `py -3.12`로 CPython을 선택합니다.
가상환경 활성화 없이 위 명령을 실행하므로 PowerShell 실행 정책 변경이 필요 없습니다.
가상환경을 활성화했다면 `python -m pytest -q`와
`python -m mini_moe.environment --seed 42`를 사용할 수 있습니다.

Linux:

```bash
python3.12 -m venv .venv
.venv/bin/python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip install -e '.[dev]'
.venv/bin/python -m pip check
.venv/bin/python -m pytest -q
.venv/bin/python -m mini_moe.environment --seed 42
```

macOS에서는 첫 번째 pip 명령을 `.venv/bin/python -m pip install torch==2.5.1`로 바꿉니다.
완전한 오프라인 설치에는 각 OS/Python용 의존성 wheel을 미리 준비해야 합니다.

## M0 실행과 재현성

환경 CLI는 JSON으로 Python·OS·CPU·PyTorch·CUDA 정보를 출력합니다.
GPU가 있더라도 smoke 연산은 CPU에서 실행됩니다.
Python `random`, NumPy, PyTorch CPU/CUDA 난수 시드를 설정하고 결정적 연산을 요구합니다.
동일 시드로 난수 재생을 확인한 뒤 `[2, 2]` 행렬 곱의 정답을 검증합니다.
실패하면 종료 코드가 0이 아닙니다. 모델 학습이나 성능 벤치마크는 아닙니다.

재현성은 동일한 소프트웨어·하드웨어 환경을 전제로 합니다. 서로 다른 PyTorch 버전이나
CPU/GPU 간 결과 일치는 보장하지 않습니다. GPU 결정성은 M0에서 검증하지 않습니다.
해시 순서가 중요해지는 경우 `PYTHONHASHSEED`는 프로세스 시작 전에 설정해야 합니다.
NumPy는 PyTorch의 배열 연동 초기화 경고를 방지하고 난수 재현성도 함께 검증합니다.

## 코드 구조

```text
pyproject.toml                # 패키지, 의존성, pytest 설정
src/mini_moe/
  __init__.py
  environment.py             # 환경 정보, 시드 설정, CPU smoke CLI
  data/synthetic.py          # M1: 패턴 생성과 예제 단위 분할
  data/prepare.py            # M1: 생성 CLI, manifest와 데이터 카드
  tokenizer/character.py    # M1: 학습/저장/인코딩
  model/__init__.py          # M2/M3: causal Transformer와 sparse MoE
  training/__init__.py       # M4/M6: 사전학습과 도구 사용 SFT
  inference/__init__.py      # M4: 체크포인트와 샘플링
  agent/__init__.py          # M5: 안전한 도구와 bounded loop
tests/test_environment.py    # M0 수용 테스트
tests/test_synthetic.py      # M1 분할 재현성과 중복 방지
tests/test_tokenizer.py      # M1 어휘와 특수 토큰, 저장 복원
tests/test_data_prepare.py   # M1 파일 재현성과 검증 문자 누출 방지
```

`model/`, `training/`, `inference/`, `agent/`는 현재 docstring만 있습니다.
학습·평가·데모 CLI는 해당 마일스톤에서 구현합니다. 완료 상태와 실제 검증 근거는
`TASKS.md`를 참고하세요. 체크포인트·데이터·실험 로그·비밀은 `.gitignore`로 제외합니다.

## M0 설계 결정

- `src` 레이아웃과 setuptools를 선택했습니다. 루트 모듈 배치보다 패키지 경계가 명확하며
  editable 설치와 pytest의 `pythonpath` 설정으로 개발할 수 있습니다.
- 별도 스크립트나 CLI 프레임워크 대신 표준 라이브러리 `argparse`와 모듈 실행을 사용합니다.
- CPU wheel을 기본 설치로 선택했습니다. GPU 최적화는 CPU 경로가 완성된 뒤 진행합니다.
- NumPy를 명시적 의존성으로 추가했습니다. 첫 실제 실행에서 PyTorch의 NumPy 연동
  초기화 경고가 발생했으며, 설치 후 경고 없이 CPU 테스트를 통과했습니다.
- 빈 pytest 실행은 종료 코드 5이므로 실제 환경·시드·CPU smoke 테스트를 먼저 제공합니다.
- Windows / Python 3.12.10 / PyTorch 2.5.1+cpu에서 9개 테스트가 1.52초에 통과했고,
  CPU smoke와 `pip check`도 통과했습니다. 자세한 실행 근거는 `TASKS.md`에 기록했습니다.
  GPU와 다른 OS에서는 아직 검증하지 않았습니다.
- 직접 의존성 버전을 고정했지만 전이 의존성 전체를 잠근 환경은 아닙니다.

## M1 데이터 생성과 CPU smoke

Windows PowerShell에서 다음 명령을 실행합니다. 추가 의존성이나 다운로드는 필요 없습니다.

```powershell
.\.venv\Scripts\python.exe -m mini_moe.data.prepare --output-dir data/synthetic --seed 42 --validation-fraction 0.2
.\.venv\Scripts\python.exe -m pytest -q
```

Linux/macOS에서는 실행 파일을 `.venv/bin/python`으로 바꿉니다.
활성화한 환경에서는 `python -m mini_moe.data.prepare --output-dir data/synthetic --seed 42 --validation-fraction 0.2`를 사용합니다.
동일 명령을 다시 실행하면 아래 다섯 파일을 덮어씁니다. 실험별로 보관하려면
`--output-dir`를 별도 폴더로 지정하세요. 생성 파일은 Git에서 제외됩니다.

| 파일 | 내용 |
|---|---|
| `train.jsonl` | 학습 예제 204개, 각 행에 `family`와 `text` |
| `validation.jsonl` | 검증 예제 52개 |
| `tokenizer.json` | 학습 텍스트에서만 얻은 문자 어휘와 고정 특수 토큰 |
| `manifest.json` | 시드·분할 비율·가족별 개수·SHA-256·검증 UNK 수 |
| `dataset_card.md` | 생성 출처·라이선스 상태·분할 방식·한계·누출 주의사항 |

흐름은 **예제 생성 → 분할 확정 → train만으로 어휘 학습 → 저장·재로드 → 인코딩**입니다.
256개는 색/동물/장소 설명 128개와 숫자 세기 128개로 구성됩니다.
시드 42와 검증 비율 0.2에서 각 가족은 train 102개, validation 26개입니다.
가족별 개수는 반올림하고 최소 1개의 학습·검증 예제를 유지하므로 실제 비율은
요청한 비율과 조금 다를 수 있습니다. 전역 RNG를 바꾸지 않는 로컬 RNG로 분할합니다.

문자열은 문자 ID 목록 `[T]`가 되며 기본 `T = len(text) + 2`입니다.
PAD=0, UNK=1, BOS=2, EOS=3이고 `encode()`는 BOS/EOS를 추가합니다.
`decode()`는 PAD/BOS/EOS를 제거하되 미지의 문자는 `<unk>`로 보입니다.
유니코드·공백·개행은 정규화하지 않습니다. 새 문자를 인코딩해도 어휘를 늘리지 않습니다.
예를 들어 저장된 토크나이저는 다음처럼 사용할 수 있습니다.

```python
from mini_moe.tokenizer.character import CharacterTokenizer

tokenizer = CharacterTokenizer.load("data/synthetic/tokenizer.json")
ids = tokenizer.encode("The red bird is near the hill.")
assert tokenizer.decode(ids) == "The red bird is near the hill."
```

실제 CPU smoke에서 어휘는 42개였고 검증 UNK 문자 수는 0이었습니다.
CLI는 저장된 데이터를 다시 읽어 encode/decode 예제 3개를 출력했습니다.
전체 테스트는 **46 passed in 1.48s**, 경고 없음으로 통과했습니다.
재현성 테스트는 서로 다른 출력 경로의 다섯 파일이 바이트 단위로 같은지 확인합니다.

## M1 설계 결정과 한계

- BPE 라이브러리 대신 문자 단위 토크나이저를 직접 구현했습니다. 학습 어휘와 검증 문자
  누출을 눈으로 확인하기 쉽고 추가 설치가 필요 없습니다. BPE에 비해 토큰 수가 많으며
  미지의 문자는 원문 복원이 불가능합니다.
- 가족별 분할로 두 패턴이 양쪽에 포함되게 했습니다. 문장 중복은 거부하고, 토큰 창을
  만든 뒤 분할하는 방식은 사용하지 않습니다. 배치·텐서 패킹은 아직 구현하지 않았습니다.
- 이 holdout은 문장이 다르지만 템플릿·단어·인접 숫자를 공유합니다. 자연어 지능이나
  미지 템플릿 일반화를 입증하지 않습니다. 도구 사용 데이터와 평가는 M6에 남아 있습니다.
- M2 이후는 미구현입니다. 다음 단계는 causal dense GPT와 shape·gradient·causal masking
  테스트, CPU one-batch overfit 진단입니다.

## 지침 문서

- `AGENTS.md`: 구현 규칙
- `SPEC.md`: 기술 명세와 수용 조건
- `TASKS.md`: 마일스톤과 검증 기록
- `PROMPTS.md`: 다음 단계 요청 예시
