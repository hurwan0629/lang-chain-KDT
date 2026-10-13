"""한국어 문장으로 토크나이저 → Dataset → Transformer → 학습을 따라가는 예제."""

import argparse
from pathlib import Path

import torch
from torch import nn
from torch.utils.data import DataLoader, Dataset
from transformers import AutoTokenizer


# 0은 부정, 1은 긍정입니다. 외부 데이터셋 대신 흐름을 읽기 쉬운 작은 데이터를 씁니다.
TRAIN_SAMPLES = [
    ("이 영화는 정말 재미있어요", 1),
    ("이 영화는 너무 지루해요", 0),
    ("음식이 맛있고 만족스러워요", 1),
    ("음식이 맛없고 실망스러워요", 0),
    ("상품의 품질이 좋아요", 1),
    ("상품의 품질이 나빠요", 0),
    ("직원들이 친절해서 좋았어요", 1),
    ("직원들이 불친절해서 싫었어요", 0),
    ("배송이 빨라서 만족해요", 1),
    ("배송이 느려서 불만이에요", 0),
    ("다시 구매하고 싶어요", 1),
    ("다시는 구매하고 싶지 않아요", 0),
    ("정말 훌륭하고 추천하고 싶어요", 1),
    ("정말 별로이고 추천하지 않아요", 0),
    ("즐겁고 행복한 시간이었어요", 1),
    ("불쾌하고 짜증 나는 시간이었어요", 0),
]

# 학습에 넣지 않는 문장입니다. 4개뿐이므로 정확도는 사용법을 보여주는 수치입니다.
EVAL_SAMPLES = [
    ("영화가 재미있어서 만족해요", 1),
    ("음식이 맛있어서 다시 먹고 싶어요", 1),
    ("상품이 나빠서 실망했어요", 0),
    ("배송이 느리고 직원도 불친절해요", 0),
]

MAX_LENGTH = 32
BATCH_SIZE = 4
LABEL_NAMES = ("부정", "긍정")
# 토크나이저 파일만 프로젝트 안에 캐시합니다. BERT 모델 가중치는 받지 않습니다.
CACHE_DIR = Path(__file__).resolve().parents[2] / ".cache" / "huggingface"


class ReviewDataset(Dataset):
    """문장과 정답을 받아 모델에 전달할 텐서를 준비합니다."""

    def __init__(self, samples, tokenizer):
        texts = [text for text, label in samples]
        self.labels = torch.tensor([label for text, label in samples], dtype=torch.long)
        self.encodings = tokenizer(
            texts,
            padding="max_length",  # 짧은 문장 뒤에 PAD를 붙여 길이를 맞춥니다.
            truncation=True,  # 긴 문장은 MAX_LENGTH 안으로 자릅니다.
            max_length=MAX_LENGTH,
            return_tensors="pt",  # Python 리스트 대신 PyTorch 텐서를 받습니다.
            return_token_type_ids=False,  # 이번 모델은 문장 구분 ID를 사용하지 않습니다.
        )

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        # Dataset은 한 문장을, DataLoader는 여러 문장을 묶은 배치를 반환합니다.
        return {
            "input_ids": self.encodings["input_ids"][index],
            "attention_mask": self.encodings["attention_mask"][index],
            "labels": self.labels[index],
        }


class TinyTransformerClassifier(nn.Module):
    """사전학습 가중치 없이 작은 Transformer Encoder를 구성합니다."""

    def __init__(self, vocab_size, pad_token_id):
        super().__init__()
        hidden_size = 64
        # 토큰 ID를 64차원 벡터로 바꿉니다. 이 임베딩도 처음부터 학습합니다.
        self.token_embedding = nn.Embedding(vocab_size, hidden_size, padding_idx=pad_token_id)
        # Attention 자체에는 순서 정보가 없으므로 위치 벡터를 더합니다.
        self.position_embedding = nn.Embedding(MAX_LENGTH, hidden_size)

        # 이 층 안에 Multi-Head Self-Attention, FFN, residual, LayerNorm이 있습니다.
        layer = nn.TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=4,
            dim_feedforward=128,
            dropout=0.1,
            batch_first=True,  # 텐서 순서: [배치, 토큰 길이, 벡터 차원]
        )
        # 첫 단계는 한 층만 사용하고 일반 텐서 형태로 계산합니다.
        self.encoder = nn.TransformerEncoder(layer, num_layers=1, enable_nested_tensor=False)
        self.classifier = nn.Linear(hidden_size, 2)

    def forward(self, input_ids, attention_mask):
        sequence_length = input_ids.size(1)
        positions = torch.arange(sequence_length, device=input_ids.device).unsqueeze(0)
        hidden = self.token_embedding(input_ids) + self.position_embedding(positions)

        # 토크나이저: 1=유효 토큰, 0=PAD. PyTorch 마스크: True=무시할 위치입니다.
        padding_mask = attention_mask == 0
        hidden = self.encoder(hidden, src_key_padding_mask=padding_mask)

        # 문장을 벡터 하나로 요약합니다. PAD는 평균 계산에서도 제외합니다.
        # [CLS], [SEP]는 유효 토큰이므로 이 예제의 평균에는 포함됩니다.
        valid_tokens = attention_mask.unsqueeze(-1).to(hidden.dtype)
        pooled = (hidden * valid_tokens).sum(dim=1) / valid_tokens.sum(dim=1).clamp(min=1)
        # 결과는 [배치, 2]의 logits입니다. 여기서는 softmax를 적용하지 않습니다.
        return self.classifier(pooled)


def train_one_epoch(model, loader, optimizer, loss_fn, device):
    """정답과 예측의 차이를 계산하고 역전파로 가중치를 갱신합니다."""
    model.train()  # 학습 모드에서는 dropout이 작동합니다.
    total_loss = 0.0
    for batch in loader:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = batch["labels"].to(device)

        optimizer.zero_grad()  # 이전 배치의 기울기를 지웁니다.
        logits = model(input_ids, attention_mask)  # 순전파
        loss = loss_fn(logits, labels)  # CrossEntropyLoss는 logits를 직접 받습니다.
        loss.backward()  # 역전파: 각 가중치의 기울기 계산
        optimizer.step()  # 계산한 기울기로 가중치 갱신
        total_loss += loss.item() * labels.size(0)
    return total_loss / len(loader.dataset)


def evaluate(model, loader, device):
    """학습에 쓰지 않은 문장의 정확도를 계산합니다."""
    model.eval()  # 평가 모드에서는 dropout을 끕니다.
    correct = 0
    with torch.no_grad():  # 평가에는 역전파가 없으므로 기울기를 기록하지 않습니다.
        for batch in loader:
            logits = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
            predictions = logits.argmax(dim=-1)
            correct += (predictions == batch["labels"].to(device)).sum().item()
    return correct / len(loader.dataset)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--epochs", type=int, default=10, help="전체 학습 데이터 반복 횟수")
    args = parser.parse_args()
    if args.epochs < 1:
        parser.error("--epochs는 1 이상이어야 합니다.")

    torch.manual_seed(42)  # 초기화와 배치 섞기의 난수를 고정합니다. 환경별 오차는 가능합니다.
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"사용 장치: {device}")

    # 1. 한국어 토크나이저만 불러옵니다. 사전학습 BERT 모델을 불러오는 것은 아닙니다.
    print("\n[1] 토크나이저 불러오기: klue/bert-base")
    tokenizer = AutoTokenizer.from_pretrained("klue/bert-base", cache_dir=str(CACHE_DIR))

    # 2. 직접 만든 Dataset을 DataLoader에 넣어 배치 단위로 꺼냅니다.
    print("[2] Dataset과 DataLoader 만들기")
    train_dataset = ReviewDataset(TRAIN_SAMPLES, tokenizer)
    eval_dataset = ReviewDataset(EVAL_SAMPLES, tokenizer)
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    eval_loader = DataLoader(eval_dataset, batch_size=BATCH_SIZE)
    sample = train_dataset[0]
    print("원문:", TRAIN_SAMPLES[0][0])
    print("토큰:", tokenizer.convert_ids_to_tokens(sample["input_ids"].tolist()))
    print("토큰 ID:", sample["input_ids"].tolist())
    print("마스크:", sample["attention_mask"].tolist())

    # 3. 작은 모델을 만들고 학습 전에 입출력 모양을 확인합니다.
    print("\n[3] Transformer 만들기")
    model = TinyTransformerClassifier(len(tokenizer), tokenizer.pad_token_id).to(device)
    model.eval()
    with torch.no_grad():
        batch = next(iter(eval_loader))
        logits = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
    embedding_shape = (*batch["input_ids"].shape, model.token_embedding.embedding_dim)
    print(f"입력: {tuple(batch['input_ids'].shape)} → 임베딩: {embedding_shape} → 출력: {tuple(logits.shape)}")
    print(f"학습할 파라미터 수: {sum(parameter.numel() for parameter in model.parameters()):,}")

    # 4. 옵티마이저와 손실 함수를 사용해 모든 모델 가중치를 학습합니다.
    print("\n[4] 학습 시작")
    optimizer = torch.optim.AdamW(model.parameters(), lr=0.003)
    loss_fn = nn.CrossEntropyLoss()
    for epoch in range(1, args.epochs + 1):
        loss = train_one_epoch(model, train_loader, optimizer, loss_fn, device)
        print(f"epoch {epoch:02d}/{args.epochs}: 학습 loss={loss:.4f}")

    # 5. 학습 데이터와 분리한 4개 문장으로 평가합니다.
    accuracy = evaluate(model, eval_loader, device)
    print(f"\n[5] 평가 정확도: {accuracy:.1%} (문장 4개로 보는 동작 예시)")

    # 6. 새로운 문장도 학습 때와 같은 토크나이저를 거쳐 모델에 전달합니다.
    print("\n[6] 문장 예측")
    texts = ["이 영화는 재미있고 좋았어요", "상품이 별로라서 실망했어요"]
    encoded = tokenizer(texts, padding="max_length", truncation=True,
                        max_length=MAX_LENGTH, return_tensors="pt", return_token_type_ids=False)
    model.eval()
    with torch.no_grad():
        logits = model(encoded["input_ids"].to(device), encoded["attention_mask"].to(device))
        probabilities = logits.softmax(dim=-1).cpu()
    for text, probability in zip(texts, probabilities):
        label = LABEL_NAMES[probability.argmax().item()]
        print(f"{text!r} → {label} (부정={probability[0]:.3f}, 긍정={probability[1]:.3f})")


if __name__ == "__main__":
    main()
