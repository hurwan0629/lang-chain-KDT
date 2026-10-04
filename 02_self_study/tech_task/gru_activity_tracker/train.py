from __future__ import annotations

import argparse

import torch
from torch.utils.data import DataLoader

from .clip_encoder import ClipEncoder
from .config import (
    ACTIVITY_PROMPTS,
    CHECKPOINT_DIR,
    DEFAULT_CHECKPOINT,
    PIE2F_INDEX_DIR,
    PIE2F_PROCESSED_DIR,
    PROCESSED_DIR,
)
from .dataset import ActivitySequenceDataset
from .model import ActivityGRU
from .prepare_dataset import prepare_all
from .prepare_pie2f import prepare_pie2f


def collate_batch(
    batch: list[tuple[torch.Tensor, str]],
) -> tuple[torch.Tensor, list[str]]:
    sequences, labels = zip(*batch)
    return torch.stack(sequences), list(labels)


def evaluate(
    model: ActivityGRU,
    loader: DataLoader,
    text_embeddings: torch.Tensor,
    label_to_index: dict[str, int],
    device: torch.device,
    temperature: float,
) -> float:
    model.eval()
    correct = 0
    total = 0

    with torch.inference_mode():
        for sequences, labels in loader:
            sequences = sequences.to(device)
            representations = model(sequences)
            logits = representations @ text_embeddings.T / temperature
            predictions = logits.argmax(dim=-1)

            targets = torch.tensor(
                [label_to_index[label] for label in labels],
                device=device,
            )
            correct += int((predictions == targets).sum().item())
            total += len(labels)

    return correct / max(total, 1)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--hidden-dim", type=int, default=256)
    parser.add_argument("--lr", type=float, default=1e-3)
    parser.add_argument("--temperature", type=float, default=0.07)
    parser.add_argument(
        "--skip-prepare",
        action="store_true",
        help="processed dataset이 이미 있을 때 데이터 준비 단계를 건너뜁니다.",
    )
    parser.add_argument(
        "--dataset",
        choices=["auto", "pie2f", "legacy"],
        default="auto",
        help="auto면 PIE2F index가 있을 때 PIE2F를 우선 사용합니다.",
    )
    parser.add_argument(
        "--max-prepare-sessions",
        type=int,
        default=0,
        help="PIE2F 자동 준비 시 처리할 최대 세션 수. 0이면 전체.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    has_pie2f = (
        (PIE2F_INDEX_DIR / "sessions.parquet").exists()
        and (PIE2F_INDEX_DIR / "segments.parquet").exists()
    )
    use_pie2f = (
        args.dataset == "pie2f"
        or (args.dataset == "auto" and has_pie2f)
    )
    dataset_dir = PIE2F_PROCESSED_DIR if use_pie2f else PROCESSED_DIR

    if not args.skip_prepare:
        train_files = list((dataset_dir / "train").glob("*.pt"))
        if not train_files:
            if use_pie2f:
                print("PIE2F processed dataset이 없어 자동으로 준비합니다.")
                prepare_pie2f(max_sessions=args.max_prepare_sessions)
            else:
                print("processed dataset이 없어 자동으로 준비합니다.")
                prepare_all()

    metadata_path = dataset_dir / "metadata.json"
    if metadata_path.exists():
        import json

        with metadata_path.open("r", encoding="utf-8") as file:
            metadata = json.load(file)

        labels = list(metadata["labels"])
        prompts = dict(metadata["prompts"])
    else:
        labels = list(ACTIVITY_PROMPTS)
        prompts = dict(ACTIVITY_PROMPTS)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    label_to_index = {label: index for index, label in enumerate(labels)}

    encoder = ClipEncoder(device=str(device))
    text_embeddings = encoder.encode_texts(
        [prompts[label] for label in labels]
    ).to(device)

    train_dataset = ActivitySequenceDataset(dataset_dir / "train")
    val_dataset = ActivitySequenceDataset(dataset_dir / "val")

    train_loader = DataLoader(
        train_dataset,
        batch_size=args.batch_size,
        shuffle=True,
        collate_fn=collate_batch,
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=args.batch_size,
        shuffle=False,
        collate_fn=collate_batch,
    )

    model = ActivityGRU(
        input_dim=encoder.embedding_dim,
        hidden_dim=args.hidden_dim,
        output_dim=encoder.embedding_dim,
    ).to(device)

    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr)
    criterion = torch.nn.CrossEntropyLoss()
    best_val = -1.0

    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    for epoch in range(1, args.epochs + 1):
        model.train()
        running_loss = 0.0

        for sequences, batch_labels in train_loader:
            sequences = sequences.to(device)
            targets = torch.tensor(
                [label_to_index[label] for label in batch_labels],
                device=device,
            )

            representations = model(sequences)
            logits = representations @ text_embeddings.T / args.temperature
            loss = criterion(logits, targets)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            running_loss += float(loss.item())

        val_accuracy = evaluate(
            model,
            val_loader,
            text_embeddings,
            label_to_index,
            device,
            args.temperature,
        )

        average_loss = running_loss / max(len(train_loader), 1)
        print(
            f"epoch {epoch:02d} | "
            f"loss {average_loss:.4f} | "
            f"val_acc {val_accuracy:.3f}"
        )

        if val_accuracy > best_val:
            best_val = val_accuracy
            torch.save(
                {
                    "model_state": model.state_dict(),
                    "input_dim": encoder.embedding_dim,
                    "hidden_dim": args.hidden_dim,
                    "output_dim": encoder.embedding_dim,
                    "labels": labels,
                    "prompts": prompts,
                    "temperature": args.temperature,
                },
                DEFAULT_CHECKPOINT,
            )

    print(f"saved: {DEFAULT_CHECKPOINT}")
    print(f"best validation accuracy: {best_val:.3f}")


if __name__ == "__main__":
    main()
