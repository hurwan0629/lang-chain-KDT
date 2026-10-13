# 1단계: PyTorch로 작은 Transformer 학습하기

한국어 문장을 긍정/부정으로 분류하면서 전체 학습 흐름을 확인합니다. 모델의 핵심은 `train.py` 한 파일에 있고, 설명 주석은 한국어입니다.

## 실행

PowerShell에서 프로젝트 루트(`moemoe`)를 기준으로 실행하세요. 일반 `python` 대신 지정한 가상환경의 Python을 사용합니다.

```powershell
$taskPython = 'C:\LANG_CHAIN_2026\2026-05-19_KDT_lang_chain\.venv\Scripts\python.exe'

# 기본 10 epoch: 토큰 확인 → 모델 구성 → 학습 → 평가 → 예측
& $taskPython -X utf8 test/transformer_demo/train.py

# 실행 흐름만 빠르게 보려면 1 epoch
& $taskPython -X utf8 test/transformer_demo/train.py --epochs 1

# 다운로드 없이 CPU에서 모델 동작 검사
& $taskPython -X utf8 -m unittest discover -s test/transformer_demo -p 'test_*.py' -v
```

기존 가상환경의 `torch`, `transformers`를 사용하므로 추가 설치는 없습니다. 첫 실행에는 Hugging Face에서 `klue/bert-base`의 토크나이저 파일을 받기 위한 인터넷 연결이 필요합니다. 파일은 프로젝트 루트의 `.cache/huggingface/`에 저장됩니다. CUDA를 사용할 수 있으면 GPU로 학습하고, 그렇지 않으면 CPU로 실행합니다.

## 코드 읽는 순서

1. `TRAIN_SAMPLES`, `EVAL_SAMPLES`: 문장과 정답을 직접 만듭니다. 정답 0은 부정, 1은 긍정입니다.
2. `AutoTokenizer.from_pretrained`: 문장을 토큰 ID로 바꾸는 한국어 토크나이저를 불러옵니다.
3. `ReviewDataset`: 문장과 정답을 `input_ids`, `attention_mask`, `labels` 텐서로 준비합니다.
4. `DataLoader`: 한 문장씩 꺼내는 Dataset을 4개 문장씩 묶습니다. 학습 데이터는 섞습니다.
5. `TinyTransformerClassifier`: 토큰/위치 임베딩 → Transformer Encoder → PAD를 제외한 평균 → 분류기를 통과합니다.
6. `train_one_epoch`: 기울기 초기화 → 순전파 → 손실 계산 → 역전파 → 가중치 갱신 과정을 확인합니다.
7. `evaluate`, 마지막 예측 부분: 평가 모드에서 학습에 쓰지 않은 문장의 결과를 확인합니다.

`main()` 안에는 위 과정이 `[1]`부터 `[6]`까지 실행 순서대로 적혀 있습니다.

## 모델 내부의 흐름

```text
문장 4개
  ↓ 한국어 토크나이저 + 길이 32로 패딩/자르기
input_ids       [4, 32]       각 토큰의 어휘 ID
attention_mask  [4, 32]       유효 토큰 1, PAD 0
  ↓ 토큰 임베딩 + 학습 가능한 위치 임베딩
벡터            [4, 32, 64]
  ↓ Transformer Encoder 1층
벡터            [4, 32, 64]   토큰 사이 관계 반영
  ↓ PAD를 제외한 토큰 벡터 평균
문장 벡터       [4, 64]
  ↓ Linear 분류기
logits          [4, 2]        부정/긍정의 점수
  ↓ 학습: CrossEntropyLoss / 예측: softmax
```

위치 임베딩은 단어 순서를 알려줍니다. Transformer 층에는 Self-Attention, FFN, residual 연결, LayerNorm이 들어 있습니다. 이번에는 PyTorch가 제공하는 층을 사용하며 Attention 수식을 직접 작성하지는 않습니다.

토크나이저의 `attention_mask`는 1이 유효 토큰이지만, PyTorch의 `src_key_padding_mask`는 `True`가 무시할 위치입니다. 그래서 `attention_mask == 0`으로 변환합니다. 문장 벡터를 평균낼 때도 PAD를 제외해야 합니다. `[CLS]`, `[SEP]`는 이번 예제의 평균에 포함됩니다.

`CrossEntropyLoss`는 softmax 전의 logits와 정답 ID를 받습니다. 예측을 사람이 읽을 확률로 표시할 때만 softmax를 적용합니다.

## 사용한 라이브러리

| 라이브러리 | 이번 예제에서의 역할 |
|---|---|
| `transformers.AutoTokenizer` | 공개 한국어 토크나이저 불러오기 |
| `torch.utils.data.Dataset`, `DataLoader` | 데이터 구성과 배치 생성 |
| `torch.nn` | 임베딩, Transformer, 분류기, 손실 함수 |
| `torch.optim.AdamW` | 역전파로 얻은 기울기에 따라 가중치 갱신 |
| `argparse`, `pathlib` | 실행 옵션과 토크나이저 캐시 경로 관리 |
| `unittest` | 마스크, 출력 모양, 가중치 갱신 검증 |

`datasets` 패키지는 이번 단계에서 사용하지 않습니다. 먼저 PyTorch Dataset의 역할을 익히고 나중에 공개 데이터셋으로 바꾸면 됩니다.

## 이번 단계의 범위

**사전학습된 것은 토크나이저뿐입니다.** BERT 모델 가중치는 불러오지 않고 임베딩·Transformer·분류기를 모두 처음부터 학습합니다. 토크나이저를 불러왔다고 모델이 한국어 의미를 이미 아는 것은 아닙니다.

학습 16문장, 평가 4문장인 동작 확인용 데이터입니다. 손실 감소는 이 데이터에 맞춰 학습했다는 뜻이며, 일반적인 감정 분석 성능을 입증하지 않습니다. 출력 확률도 신뢰도가 검증된 값은 아닙니다.

실제 GPU 실행 확인에서는 10 epoch 동안 학습 loss가 약 `0.7702 → 0.0085`로 감소하고 평가 문장 4개 중 3개를 맞혔습니다. 하지만 새 문장인 `상품이 별로라서 실망했어요`는 긍정으로 잘못 예측했습니다. 작은 학습 데이터의 loss가 낮아져도 새로운 문장을 잘 분류한다는 보장은 없다는 예시입니다. 환경에 따라 실행 수치는 달라질 수 있습니다.

이번 단계에는 MoE, 웹 서비스, 체크포인트 저장을 추가하지 않습니다. 다음 단계에서는 학습 데이터부터 늘려 비교하고, 이후 Transformer의 FFN을 MoE로 바꾸면 변화가 더 잘 보입니다.

공식 참고: [PyTorch TransformerEncoderLayer](https://docs.pytorch.org/docs/stable/generated/torch.nn.TransformerEncoderLayer.html), [PyTorch Dataset/DataLoader](https://docs.pytorch.org/docs/stable/data.html), [KLUE 한국어 토크나이저](https://huggingface.co/klue/bert-base).
