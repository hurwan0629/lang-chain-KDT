# 숫자로 먼저 이해하는 MoE

MoE(Mixture of Experts)는 **여러 expert를 가지고 있으면서, 입력마다 일부 expert만 선택해서 계산하는 구조**입니다. 모델의 전체 용량을 늘리면서도 입력 하나가 사용하는 expert 계산량을 제한할 수 있습니다.

이 폴더는 Python 기본 라이브러리만 사용합니다. GPU, PyTorch, NumPy 설치 없이 실행할 수 있습니다.

## 실행

프로젝트 루트(`moemoe`)에서 실행하세요.

```powershell
# 입력마다 expert 하나만 실행
python tests/moe_demo/demo.py

# 입력마다 expert 두 개를 실행하고 결과를 가중합
python tests/moe_demo/demo.py --top-k 2

# expert 세 개를 모두 사용하는 경우와 비교
python tests/moe_demo/demo.py --top-k 3

# 직접 입력을 바꾸며 관찰. --input은 여러 번 지정할 수 있습니다.
python tests/moe_demo/demo.py --top-k 2 --input 1 1 --input -2 -2

# 동작 검증
python -m unittest discover -s tests/moe_demo -p "test_*.py" -v
```

## 무엇을 보나요?

각 입력 `(x, y)`는 토큰 하나의 임베딩을 흉내 낸 2차원 벡터입니다. 문장을 실제로 토큰화하거나 의미를 해석하지는 않습니다.

```text
입력 벡터 → Router → 선택한 expert만 실행 → 선택 확률로 가중합 → 출력
```

Router는 선형 계산으로 `[x, y, -x-y]`를 만든 다음 softmax로 선택 확률을 구합니다. Expert는 서로 다른 가중치를 가진 작은 `Linear → ReLU → Linear` 네트워크입니다. 여기서는 결과를 쉽게 확인하도록 다음 동작을 하게 설정했습니다.

| Expert | 동작 | 예시 |
|---|---|---|
| `boost_x` | 첫 번째 값을 2배 | `(2, 0) → (4, 0)` |
| `boost_y` | 두 번째 값을 2배 | `(0, 2) → (0, 4)` |
| `flip_sign` | 두 값의 부호 반전 | `(-2, -2) → (2, 2)` |

기본 실행에서 `(2, 0)`은 `boost_x`, `(0, 2)`는 `boost_y`, `(-2, -2)`는 `flip_sign`으로 갑니다. **입력이 달라지면 실제로 실행되는 네트워크가 달라지는 것**이 핵심입니다.

`--top-k 2 --input 1 1`에서는 `boost_x`와 `boost_y`가 선택됩니다. 두 expert의 출력 `(2, 1)`, `(1, 2)`를 각각 0.5의 비중으로 합쳐 `(1.5, 1.5)`를 얻습니다. 이 예제는 선택된 expert들의 확률 합이 1이 되도록 다시 정규화합니다. 실제 MoE에는 선택 후에도 원래 gate 확률을 유지하는 방식도 있습니다.

출력의 `Router`는 전체 선택 확률, `RUN`은 실행한 expert와 가중치, `MoE output`은 최종 결과입니다. `All-expert mixture`는 같은 router로 세 expert를 모두 섞은 비교 결과이며, 일반 Dense Transformer의 FFN과 동일한 구조는 아닙니다.

입력 4개에 대해 top-1 경로는 expert를 총 4번, 전체 expert 경로는 총 12번 실행합니다. 프로그램은 비교 결과도 출력하므로 비교용 계산까지 실제로 수행합니다. 마지막 호출 횟수는 두 경로를 각각 계산한 수치이며 실행 시간 측정치는 아닙니다.

## Transformer에서의 역할

일반 Transformer 블록의 FFN을 MoE 층으로 바꾸는 구성을 생각하면 됩니다.

```text
일반 블록: Attention → 하나의 FFN
MoE 블록:  Attention → Router → 선택한 여러 FFN → 가중합
```

위 그림은 LayerNorm과 residual 연결을 생략했습니다. Attention은 토큰 사이의 관계를 반영하고, MoE는 각 토큰에 어떤 FFN 계산을 적용할지 선택합니다. 모든 층을 MoE로 바꿀 필요는 없습니다.

여기서는 router와 expert의 가중치를 사람이 설정했습니다. 실제 모델은 보통 학습으로 이 가중치를 조정하며, expert의 역할도 학습 결과로 정해집니다. 처음부터 ‘수학 담당’, ‘번역 담당’처럼 의미가 정해지는 것은 아닙니다.

## 알아둘 한계와 다음 단계

- 이 예제는 routing과 희소 실행을 보는 실험이며, 학습·Attention·언어 이해 기능은 없습니다.
- 일부 expert만 실행해도 전체 expert 가중치는 저장해야 합니다. 연산량 감소가 같은 비율의 메모리 감소를 뜻하지는 않습니다.
- 실제 속도는 routing, 배치 처리, 하드웨어 등의 영향을 받으므로 expert 호출 횟수만으로 판단할 수 없습니다.
- 다음 단계는 PyTorch로 학습 가능한 router와 expert를 만들고, 한 expert로 입력이 몰리는 현상과 load-balancing loss를 관찰하는 것입니다.

참고: [Hugging Face Switch Transformers](https://huggingface.co/docs/transformers/model_doc/switch_transformers), [Switch Transformers 논문](https://arxiv.org/abs/2101.03961).
