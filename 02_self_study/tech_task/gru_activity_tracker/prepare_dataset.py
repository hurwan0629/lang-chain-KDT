from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import shutil
from pathlib import Path
from typing import Any

import torch
from PIL import Image

from .clip_encoder import ClipEncoder
from .config import (
    ACTIVITY_PROMPTS,
    PROCESSED_DIR,
    RAW_DIR,
    SOURCES_CSV,
    VIDEO_CUA_DIR,
    VIDEO_CUA_INDEX,
    WEAK_LABEL_KEYWORDS,
)


VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm"}


def infer_weak_label(text: str) -> str | None:
    lowered = text.lower()
    for label, keywords in WEAK_LABEL_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            return label
    return None


def split_for_source(source_id: str) -> str:
    bucket = int(hashlib.md5(source_id.encode("utf-8")).hexdigest(), 16) % 10
    if bucket == 0:
        return "test"
    if bucket == 1:
        return "val"
    return "train"


def require_module(name: str, install_name: str | None = None) -> Any:
    try:
        return importlib.import_module(name)
    except ImportError as exc:
        package = install_name or name
        raise RuntimeError(
            f"'{package}' 패키지가 필요합니다. pip install {package}"
        ) from exc


def read_sources() -> list[dict[str, str]]:
    if not SOURCES_CSV.exists():
        return []

    with SOURCES_CSV.open("r", newline="", encoding="utf-8-sig") as file:
        return [
            {key: (value or "").strip() for key, value in row.items()}
            for row in csv.DictReader(file)
            if (row.get("url") or "").strip()
        ]


def download_sources() -> list[tuple[Path, list[tuple[float, float | None, str]]]]:
    rows = read_sources()
    if not rows:
        return []

    yt_dlp = require_module("yt_dlp", "yt-dlp")
    download_dir = RAW_DIR / "_downloads"
    download_dir.mkdir(parents=True, exist_ok=True)
    results: list[tuple[Path, list[tuple[float, float | None, str]]]] = []

    for row in rows:
        url = row["url"]
        explicit_label = row.get("label", "")
        if explicit_label and explicit_label not in ACTIVITY_PROMPTS:
            print(f"[skip] unknown label: {explicit_label}")
            continue

        options = {
            "format": "best[ext=mp4]/best",
            "outtmpl": str(download_dir / "%(id)s.%(ext)s"),
            "quiet": True,
            "noplaylist": True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            local_path = Path(ydl.prepare_filename(info))

        duration = float(info.get("duration") or 0)
        segments: list[tuple[float, float | None, str]] = []

        if explicit_label:
            start = float(row.get("start_sec") or 0)
            raw_end = row.get("end_sec", "")
            end = float(raw_end) if raw_end else (duration or None)
            segments.append((start, end, explicit_label))
        else:
            title = str(info.get("title") or "")
            chapters = info.get("chapters") or []

            for chapter in chapters:
                chapter_text = f"{title} {chapter.get('title', '')}"
                label = infer_weak_label(chapter_text)
                if label is None:
                    continue
                segments.append((
                    float(chapter.get("start_time") or 0),
                    float(chapter.get("end_time") or duration or 0) or None,
                    label,
                ))

            if not segments:
                label = infer_weak_label(title)
                if label is not None:
                    segments.append((0.0, duration or None, label))

        if segments:
            results.append((local_path, segments))
        else:
            print(f"[skip] weak label을 만들 수 없음: {url}")

    return results


def local_video_sources() -> list[tuple[Path, list[tuple[float, float | None, str]]]]:
    results: list[tuple[Path, list[tuple[float, float | None, str]]]] = []

    for label in ACTIVITY_PROMPTS:
        label_dir = RAW_DIR / label
        if not label_dir.exists():
            continue

        for path in sorted(label_dir.iterdir()):
            if path.suffix.lower() in VIDEO_EXTENSIONS:
                results.append((path, [(0.0, None, label)]))

    return results


def videocua_sources() -> list[tuple[Path, list[tuple[float, float | None, str]]]]:
    if not VIDEO_CUA_INDEX.exists():
        return []

    results: list[tuple[Path, list[tuple[float, float | None, str]]]] = []

    with VIDEO_CUA_INDEX.open(
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        for row in csv.DictReader(file):
            label = (row.get("label") or "").strip()
            video_rel = (row.get("video_path") or "").strip()

            if label not in ACTIVITY_PROMPTS or not video_rel:
                continue

            video_path = VIDEO_CUA_DIR / video_rel
            if not video_path.exists():
                print(f"[skip] VideoCUA video missing: {video_path}")
                continue

            results.append((video_path, [(0.0, None, label)]))

    return results


def read_segment_frames(
    video_path: Path,
    start_sec: float,
    end_sec: float | None,
    sample_interval: float,
) -> list[Image.Image]:
    cv2 = require_module("cv2", "opencv-python")
    capture = cv2.VideoCapture(str(video_path))
    if not capture.isOpened():
        raise RuntimeError(f"영상을 열 수 없습니다: {video_path}")

    fps = float(capture.get(cv2.CAP_PROP_FPS) or 30.0)
    frame_step = max(int(round(fps * sample_interval)), 1)
    start_frame = max(int(round(start_sec * fps)), 0)
    end_frame = (
        int(round(end_sec * fps))
        if end_sec is not None and end_sec > 0
        else None
    )

    capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    frame_index = start_frame
    frames: list[Image.Image] = []

    while True:
        if end_frame is not None and frame_index >= end_frame:
            break

        ok, frame = capture.read()
        if not ok:
            break

        if (frame_index - start_frame) % frame_step == 0:
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(Image.fromarray(rgb).convert("RGB"))

        frame_index += 1

    capture.release()
    return frames


def clear_processed() -> None:
    if PROCESSED_DIR.exists():
        shutil.rmtree(PROCESSED_DIR)

    for split in ("train", "val", "test"):
        (PROCESSED_DIR / split).mkdir(parents=True, exist_ok=True)


def save_windows(
    encoder: ClipEncoder,
    video_path: Path,
    segments: list[tuple[float, float | None, str]],
    sequence_length: int,
    stride: int,
    sample_interval: float,
    batch_size: int,
    counter: dict[str, int],
) -> None:
    split = split_for_source(str(video_path.resolve()))

    for start_sec, end_sec, label in segments:
        frames = read_segment_frames(
            video_path,
            start_sec,
            end_sec,
            sample_interval,
        )

        if len(frames) < sequence_length:
            print(f"[skip] too short: {video_path.name} / {label}")
            continue

        embeddings: list[torch.Tensor] = []
        for start in range(0, len(frames), batch_size):
            batch = frames[start:start + batch_size]
            embeddings.append(encoder.encode_images(batch))

        sequence_embeddings = torch.cat(embeddings, dim=0)

        for start in range(
            0,
            sequence_embeddings.shape[0] - sequence_length + 1,
            stride,
        ):
            sequence = sequence_embeddings[start:start + sequence_length]
            index = counter[split]
            output = PROCESSED_DIR / split / f"sample_{index:06d}.pt"
            torch.save(
                {
                    "sequence": sequence,
                    "label": label,
                    "source": str(video_path),
                    "start_sec": start_sec + start * sample_interval,
                },
                output,
            )
            counter[split] += 1


def prepare_all(
    sequence_length: int = 20,
    stride: int = 10,
    sample_interval: float = 1.0,
    batch_size: int = 16,
    include_web_sources: bool = True,
) -> dict[str, int]:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    clear_processed()

    sources = local_video_sources()
    sources.extend(videocua_sources())

    if include_web_sources:
        sources.extend(download_sources())

    if not sources:
        raise RuntimeError(
            "학습할 영상이 없습니다. data/raw/<label>/에 영상을 넣거나, "
            "prepare_videocua.py로 VideoCUA를 추출하거나, "
            "data/sources.csv에 사용 허용된 영상 URL을 추가해주세요."
        )

    encoder = ClipEncoder()
    counter = {"train": 0, "val": 0, "test": 0}

    for index, (video_path, segments) in enumerate(sources, start=1):
        print(f"[{index}/{len(sources)}] {video_path.name}")
        save_windows(
            encoder,
            video_path,
            segments,
            sequence_length,
            stride,
            sample_interval,
            batch_size,
            counter,
        )

    metadata = {
        "sequence_length": sequence_length,
        "stride": stride,
        "sample_interval": sample_interval,
        "counts": counter,
        "labels": list(ACTIVITY_PROMPTS),
    }
    with (PROCESSED_DIR / "metadata.json").open("w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False, indent=2)

    print("prepared:", counter)
    return counter


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--sequence-length", type=int, default=20)
    parser.add_argument("--stride", type=int, default=10)
    parser.add_argument("--sample-interval", type=float, default=1.0)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--local-only", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    prepare_all(
        sequence_length=args.sequence_length,
        stride=args.stride,
        sample_interval=args.sample_interval,
        batch_size=args.batch_size,
        include_web_sources=not args.local_only,
    )


if __name__ == "__main__":
    main()
