from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path
from typing import Any

import cv2
import pyarrow.parquet as pq
import torch
from huggingface_hub import HfApi, hf_hub_download
from PIL import Image

from .clip_encoder import ClipEncoder
from .config import (
    PIE2F_DIR,
    PIE2F_INDEX_DIR,
    PIE2F_PROCESSED_DIR,
)


REPO_ID = "Parergon/PIE2F-LongHorizon"


def first_existing(mapping: dict[str, Any], names: list[str]) -> Any:
    for name in names:
        if name in mapping and mapping[name] is not None:
            return mapping[name]
    raise KeyError(f"필요한 컬럼을 찾을 수 없습니다. candidates={names}")


def maybe_existing(mapping: dict[str, Any], names: list[str]) -> Any | None:
    for name in names:
        if name in mapping and mapping[name] is not None:
            return mapping[name]
    return None


def normalize_split(value: str | None, session_id: str) -> str:
    if value:
        split = value.lower()
        if split in {"validation", "valid"}:
            return "val"
        if split in {"train", "val", "test"}:
            return split

    bucket = int(hashlib.md5(session_id.encode("utf-8")).hexdigest(), 16) % 20
    if bucket == 0:
        return "test"
    if bucket == 1:
        return "val"
    return "train"


def load_table(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"필요한 index가 없습니다: {path}")
    return pq.read_table(path).to_pylist()


def load_taxonomy() -> tuple[list[str], dict[str, str]]:
    path = PIE2F_INDEX_DIR / "activity_taxonomy.json"
    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    labels = list(data["labels"])
    prompt_ensembles = data.get("prompt_ensembles", {})
    prompts = {
        label: str((prompt_ensembles.get(label) or [label])[0])
        for label in labels
    }
    return labels, prompts


def resolve_session_id(row: dict[str, Any]) -> str:
    return str(first_existing(
        row,
        ["session_id", "id", "session", "source_session_id", "video_id"],
    ))


def resolve_video_repo_path(
    row: dict[str, Any],
    session_id: str,
    repo_files: list[str],
) -> str:
    direct = maybe_existing(
        row,
        [
            "video_path",
            "video_relpath",
            "relative_path",
            "file_path",
            "path",
            "video_file",
        ],
    )
    if direct:
        path = str(direct).replace("\\", "/")
        if path.startswith("data/videos/"):
            return path
        candidate = f"data/videos/{path.lstrip('/')}"
        if candidate in repo_files:
            return candidate

    matches = [
        path
        for path in repo_files
        if path.startswith("data/videos/")
        and session_id.lower() in Path(path).stem.lower()
    ]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        raise RuntimeError(f"video path를 찾을 수 없습니다: session={session_id}")
    raise RuntimeError(
        f"video path 후보가 여러 개입니다: session={session_id}, matches={matches[:5]}"
    )


def segment_fields(row: dict[str, Any]) -> tuple[str, float, float, str]:
    session_id = str(first_existing(
        row,
        ["session_id", "session", "source_session_id", "video_id"],
    ))
    start = float(first_existing(
        row,
        ["start_sec", "start_time", "start_seconds", "start_s", "t_start"],
    ))
    end = float(first_existing(
        row,
        ["end_sec", "end_time", "end_seconds", "end_s", "t_end"],
    ))
    label = str(first_existing(
        row,
        [
            "activity_label",
            "label",
            "smoothed_activity_label",
            "raw_activity_label",
        ],
    ))
    return session_id, start, end, label


def encode_segment(
    capture: cv2.VideoCapture,
    encoder: ClipEncoder,
    start_sec: float,
    end_sec: float,
    sample_interval: float,
    batch_size: int,
) -> torch.Tensor:
    if end_sec <= start_sec:
        return torch.empty((0, encoder.embedding_dim), dtype=torch.float32)

    timestamps: list[float] = []
    current = start_sec
    while current < end_sec:
        timestamps.append(current)
        current += sample_interval

    embeddings: list[torch.Tensor] = []
    images: list[Image.Image] = []

    def flush() -> None:
        if not images:
            return
        embeddings.append(encoder.encode_images(images))
        images.clear()

    for timestamp in timestamps:
        capture.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000.0)
        ok, frame = capture.read()
        if not ok:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        images.append(Image.fromarray(rgb).convert("RGB"))

        if len(images) >= batch_size:
            flush()

    flush()

    if not embeddings:
        return torch.empty((0, encoder.embedding_dim), dtype=torch.float32)

    return torch.cat(embeddings, dim=0)


def save_windows(
    embeddings: torch.Tensor,
    label: str,
    session_id: str,
    segment_start: float,
    split: str,
    sequence_length: int,
    stride_frames: int,
    sample_interval: float,
    counters: dict[str, int],
) -> int:
    if embeddings.shape[0] < sequence_length:
        return 0

    saved = 0
    out_dir = PIE2F_PROCESSED_DIR / split
    out_dir.mkdir(parents=True, exist_ok=True)

    for start in range(
        0,
        embeddings.shape[0] - sequence_length + 1,
        stride_frames,
    ):
        sequence = embeddings[start:start + sequence_length].half()
        index = counters[split]
        output = out_dir / f"sample_{index:07d}.pt"

        torch.save(
            {
                "sequence": sequence,
                "label": label,
                "session_id": session_id,
                "start_sec": segment_start + start * sample_interval,
            },
            output,
        )

        counters[split] += 1
        saved += 1

    return saved


def load_progress() -> dict[str, Any]:
    path = PIE2F_PROCESSED_DIR / "progress.json"
    if not path.exists():
        return {
            "completed_sessions": [],
            "counters": {"train": 0, "val": 0, "test": 0},
        }

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_progress(progress: dict[str, Any]) -> None:
    PIE2F_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with (PIE2F_PROCESSED_DIR / "progress.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(progress, file, ensure_ascii=False, indent=2)


def prepare_pie2f(
    sequence_length: int = 10,
    sample_interval: float = 2.0,
    stride_seconds: float = 20.0,
    batch_size: int = 16,
    max_sessions: int = 0,
    keep_videos: bool = False,
    reset: bool = False,
) -> dict[str, int]:
    sessions_path = PIE2F_INDEX_DIR / "sessions.parquet"
    segments_path = PIE2F_INDEX_DIR / "segments.parquet"

    sessions = load_table(sessions_path)
    segment_rows = load_table(segments_path)
    labels, prompts = load_taxonomy()
    label_set = set(labels)

    if reset and PIE2F_PROCESSED_DIR.exists():
        shutil.rmtree(PIE2F_PROCESSED_DIR)

    PIE2F_PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    cache_dir = PIE2F_DIR / "_video_cache"
    cache_dir.mkdir(parents=True, exist_ok=True)

    progress = load_progress()
    completed = set(progress.get("completed_sessions", []))
    counters = {
        "train": int(progress.get("counters", {}).get("train", 0)),
        "val": int(progress.get("counters", {}).get("val", 0)),
        "test": int(progress.get("counters", {}).get("test", 0)),
    }

    segments_by_session: dict[str, list[tuple[float, float, str]]] = {}
    for row in segment_rows:
        session_id, start, end, label = segment_fields(row)
        if label not in label_set:
            continue
        segments_by_session.setdefault(session_id, []).append((start, end, label))

    for values in segments_by_session.values():
        values.sort(key=lambda item: item[0])

    api = HfApi()
    repo_files = api.list_repo_files(REPO_ID, repo_type="dataset")
    encoder = ClipEncoder()

    processed_session_count = 0
    stride_frames = max(
        1,
        int(round(stride_seconds / sample_interval)),
    )

    for index, session_row in enumerate(sessions, start=1):
        session_id = resolve_session_id(session_row)

        split = normalize_split(
            str(maybe_existing(session_row, ["split", "dataset_split"]) or ""),
            session_id,
        )

        if session_id in completed:
            continue
        if session_id not in segments_by_session:
            continue
        if max_sessions > 0 and processed_session_count >= max_sessions:
            break
        if False:
            if split not in {"val", "test"}:
              continue

        
        repo_path = resolve_video_repo_path(
            session_row,
            session_id,
            repo_files,
        )

        print(
            f"[{index}/{len(sessions)}] "
            f"{session_id} | {split} | {repo_path}"
        )

        local_video = Path(hf_hub_download(
            repo_id=REPO_ID,
            repo_type="dataset",
            filename=repo_path,
            local_dir=cache_dir,
        ))

        capture = cv2.VideoCapture(str(local_video))
        if not capture.isOpened():
            raise RuntimeError(f"영상을 열 수 없습니다: {local_video}")

        saved_for_session = 0

        try:
            for start_sec, end_sec, label in segments_by_session[session_id]:
                embeddings = encode_segment(
                    capture,
                    encoder,
                    start_sec,
                    end_sec,
                    sample_interval,
                    batch_size,
                )
                saved_for_session += save_windows(
                    embeddings,
                    label,
                    session_id,
                    start_sec,
                    split,
                    sequence_length,
                    stride_frames,
                    sample_interval,
                    counters,
                )
        finally:
            capture.release()

        print(f"  saved sequences: {saved_for_session}")

        completed.add(session_id)
        progress = {
            "completed_sessions": sorted(completed),
            "counters": counters,
        }
        save_progress(progress)
        processed_session_count += 1

        if not keep_videos:
            try:
                local_video.unlink()
            except OSError:
                pass

    metadata = {
        "source": REPO_ID,
        "sequence_length": sequence_length,
        "sample_interval": sample_interval,
        "stride_seconds": stride_seconds,
        "labels": labels,
        "prompts": prompts,
        "counts": counters,
    }
    with (PIE2F_PROCESSED_DIR / "metadata.json").open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

    print("prepared:", counters)
    return counters


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "PIE2F index를 읽어 세션 영상을 하나씩 다운로드하고 "
            "CLIP sequence dataset으로 변환합니다."
        )
    )
    parser.add_argument("--sequence-length", type=int, default=10)
    parser.add_argument("--sample-interval", type=float, default=2.0)
    parser.add_argument("--stride-seconds", type=float, default=20.0)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--max-sessions", type=int, default=0)
    parser.add_argument("--keep-videos", action="store_true")
    parser.add_argument("--reset", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.sequence_length <= 0:
        raise SystemExit("--sequence-length은 1 이상이어야 합니다.")
    if args.sample_interval <= 0:
        raise SystemExit("--sample-interval은 0보다 커야 합니다.")
    if args.stride_seconds <= 0:
        raise SystemExit("--stride-seconds는 0보다 커야 합니다.")

    prepare_pie2f(
        sequence_length=args.sequence_length,
        sample_interval=args.sample_interval,
        stride_seconds=args.stride_seconds,
        batch_size=args.batch_size,
        max_sessions=args.max_sessions,
        keep_videos=args.keep_videos,
        reset=args.reset,
    )


if __name__ == "__main__":
    main()
