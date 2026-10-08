from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import time

import torch

from gru_activity_tracker.activity_store import ActivityStore
from gru_activity_tracker.clip_encoder import ClipEncoder
from gru_activity_tracker.model import ActivityGRU
from gru_activity_tracker.runtime.paths import (
    bundled_checkpoint_path,
    bundled_clip_dir,
    default_log_path,
)
from gru_activity_tracker.screen_capture import capture_full_screen


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="GRU desktop activity tracker")
    parser.add_argument("--interval", type=float, default=1.0)
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--checkpoint", type=Path, default=None)
    parser.add_argument("--clip-model", type=Path, default=None)
    return parser.parse_args()


def _require_path(path: Path, description: str) -> Path:
    if not path.exists():
        raise FileNotFoundError(
            f"{description}을(를) 찾을 수 없습니다: {path}\n"
            "build_release.bat으로 배포본을 다시 생성해 주세요."
        )
    return path


def main() -> None:
    args = parse_args()
    if args.interval <= 0:
        raise SystemExit("--interval은 0보다 커야 합니다.")

    checkpoint_path = _require_path(
        args.checkpoint or bundled_checkpoint_path(),
        "GRU checkpoint",
    )
    clip_model_dir = _require_path(
        args.clip_model or bundled_clip_dir(),
        "CLIP model",
    )
    output_path = args.output or default_log_path()

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(checkpoint_path, map_location=device)

    labels: list[str] = list(checkpoint["labels"])
    prompts: dict[str, str] = dict(checkpoint["prompts"])
    temperature = float(checkpoint["temperature"])

    encoder = ClipEncoder(model_name=str(clip_model_dir), device=str(device))
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

    store = ActivityStore(output_path)
    hidden: torch.Tensor | None = None

    print("GRU activity tracker started. Press Ctrl+C to stop.")
    print(f"Device: {device}")
    print(f"Output: {output_path.resolve()}")

    try:
        while True:
            started_at = time.monotonic()
            frame = capture_full_screen()
            frame_embedding = encoder.encode_images([frame])[0].to(device)

            with torch.inference_mode():
                representation, hidden = model.step(frame_embedding, hidden)
                logits = representation @ text_embeddings.T / temperature
                probabilities = logits.softmax(dim=-1)[0]
                best_index = int(probabilities.argmax().item())

            label = labels[best_index]
            score = float(probabilities[best_index].item())
            now = datetime.now()
            store.update(label, score, now)

            print(f"[{now.strftime('%H:%M:%S')}] {label} ({score:.3f})")

            elapsed = time.monotonic() - started_at
            time.sleep(max(args.interval - elapsed, 0.01))
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        store.close()
