from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import time

import torch

from .activity_store import ActivityStore
from .clip_encoder import ClipEncoder
from .config import DEFAULT_CHECKPOINT
from .model import ActivityGRU
from .screen_capture import capture_full_screen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", default=str(DEFAULT_CHECKPOINT))
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("gru_activity_log.csv"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.interval <= 0:
        raise SystemExit("--interval은 0보다 커야 합니다.")

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

    store = ActivityStore(args.output)
    hidden: torch.Tensor | None = None

    print("GRU activity tracker started. Press Ctrl+C to stop.")
    print(f"Output: {args.output.resolve()}")

    try:
        while True:
            started_at = time.monotonic()
            frame = capture_full_screen()
            frame_embedding = encoder.encode_images([frame])[0].to(device)

            with torch.inference_mode():
                representation, hidden = model.step(
                    frame_embedding,
                    hidden,
                )
                logits = representation @ text_embeddings.T / temperature
                probabilities = logits.softmax(dim=-1)[0]
                best_index = int(probabilities.argmax().item())

            label = labels[best_index]
            score = float(probabilities[best_index].item())
            now = datetime.now()
            store.update(label, score, now)

            print(
                f"[{now.strftime('%H:%M:%S')}] "
                f"{label} ({score:.3f})"
            )

            elapsed = time.monotonic() - started_at
            time.sleep(max(args.interval - elapsed, 0.01))

    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        store.close()


if __name__ == "__main__":
    main()
