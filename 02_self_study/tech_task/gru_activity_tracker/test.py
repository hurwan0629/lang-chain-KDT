from __future__ import annotations

import argparse

import torch
from torch.utils.data import DataLoader

from .clip_encoder import ClipEncoder
from .config import DEFAULT_CHECKPOINT, PROCESSED_DIR
from .dataset import ActivitySequenceDataset
from .model import ActivityGRU
from .train import collate_batch


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default=str(DEFAULT_CHECKPOINT))
    parser.add_argument("--batch-size", type=int, default=32)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(args.checkpoint, map_location=device)

    labels: list[str] = list(checkpoint["labels"])
    prompts: dict[str, str] = dict(checkpoint["prompts"])
    temperature = float(checkpoint["temperature"])

    encoder = ClipEncoder(device=str(device))
    text_embeddings = encoder.encode_texts(
        [prompts[label] for label in labels]
    ).to(device)

    model = ActivityGRU(
        input_dim=int(checkpoint["input_dim"]),
        hidden_dim=int(checkpoint["hidden_dim"]),
        output_dim=int(checkpoint["output_dim"]),
    ).to(device)
    model.load_state_dict(checkpoint["model_state"])
    model.eval()

    dataset = ActivitySequenceDataset(PROCESSED_DIR / "test")
    loader = DataLoader(
        dataset,
        batch_size=args.batch_size,
        shuffle=False,
        collate_fn=collate_batch,
    )

    correct = 0
    total = 0

    with torch.inference_mode():
        for sequences, batch_labels in loader:
            sequences = sequences.to(device)
            representations = model(sequences)
            logits = representations @ text_embeddings.T / temperature
            predictions = logits.argmax(dim=-1).cpu().tolist()

            for predicted_index, actual_label in zip(
                predictions,
                batch_labels,
            ):
                predicted_label = labels[predicted_index]
                correct += int(predicted_label == actual_label)
                total += 1

    accuracy = correct / max(total, 1)
    print(f"test samples: {total}")
    print(f"test accuracy: {accuracy:.3f}")


if __name__ == "__main__":
    main()
