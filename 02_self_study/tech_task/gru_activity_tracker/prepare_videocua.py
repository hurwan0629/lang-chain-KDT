from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable

from .config import (
    ACTIVITY_PROMPTS,
    VIDEO_CUA_DIR,
    VIDEO_CUA_INDEX,
    WEAK_LABEL_KEYWORDS,
)


PLATFORM_LABELS = {
    "intellij": "java_coding",
    "eclipse": "java_coding",
    "thunderbird": "email",
    "outlook": "email",
    "libreoffice writer": "documentation",
    "microsoft word": "documentation",
    "calibre": "reading",
    "mendeley": "reading",
    "zotero": "reading",
    "okular": "reading",
    "vlc": "entertainment_video",
    "kodi": "entertainment_video",
    "emby": "entertainment_video",
}


def infer_label(platform: str, instruction: str) -> str | None:
    text = f"{platform} {instruction}".lower()

    for label, keywords in WEAK_LABEL_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return label

    platform_lower = platform.lower()
    for keyword, label in PLATFORM_LABELS.items():
        if keyword in platform_lower:
            return label

    return None


def safe_name(value: str) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z._-]+", "_", value.strip())
    return cleaned.strip("_") or "unknown"


def write_timeline(
    path: Path,
    action_log: list[dict[str, object]],
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "action_type"])

        for action in action_log:
            writer.writerow([
                action.get("timestamp", ""),
                action.get("action_type", ""),
            ])


def copy_stream(source, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("wb") as output:
        shutil.copyfileobj(source, output, length=1024 * 1024)


def extract_task(
    task_data: dict[str, object],
    video_source,
    source_name: str,
    label_text: str,
) -> dict[str, str]:
    task_id = str(task_data.get("task_id", "")).strip()
    platform = str(task_data.get("platform", "")).strip()
    instruction = str(task_data.get("task_instruction", "")).strip()
    actions = task_data.get("action_log") or []

    if not isinstance(actions, list):
        actions = []
    task_name = safe_name(task_id or f"{platform}_{instruction[:40]}")
    platform_name = safe_name(platform)

    video_rel = Path("videos") / platform_name / f"{task_name}.mp4"
    timeline_rel = Path("timelines") / platform_name / f"{task_name}.csv"

    video_path = VIDEO_CUA_DIR / video_rel
    timeline_path = VIDEO_CUA_DIR / timeline_rel

    if not video_path.exists():
        copy_stream(video_source, video_path)

    write_timeline(timeline_path, actions)

    last_timestamp = 0.0
    for action in actions:
        try:
            last_timestamp = max(
                last_timestamp,
                float(action.get("timestamp", 0.0)),
            )
        except (TypeError, ValueError):
            pass

    return {
        "task_id": task_id,
        "platform": platform,
        "instruction": instruction,
        "label": label_text,
        "video_path": video_rel.as_posix(),
        "timeline_path": timeline_rel.as_posix(),
        "last_action_sec": f"{last_timestamp:.3f}",
        "source": source_name,
    }


def rows_from_zip(
    zip_path: Path,
    include_unlabeled: bool,
    limit_per_label: int,
    counts: Counter[str],
) -> Iterable[dict[str, str]]:
    with zipfile.ZipFile(zip_path) as archive:
        names = set(archive.namelist())

        for action_name in sorted(
            name for name in names if name.endswith("/action_log.json")
        ):
            task_prefix = action_name[: -len("action_log.json")]
            video_name = f"{task_prefix}video/video.mp4"

            if video_name not in names:
                continue

            with archive.open(action_name) as file:
                task_data = json.load(file)

            platform = str(task_data.get("platform", ""))
            instruction = str(task_data.get("task_instruction", ""))
            label = infer_label(platform, instruction)
            label_text = label or "unlabeled"

            if label is None and not include_unlabeled:
                continue
            if limit_per_label > 0 and counts[label_text] >= limit_per_label:
                continue

            with archive.open(video_name) as video_source:
                row = extract_task(
                    task_data,
                    video_source,
                    zip_path.name,
                    label_text,
                )

            counts[label_text] += 1
            yield row


def rows_from_directory(
    source_dir: Path,
    include_unlabeled: bool,
    limit_per_label: int,
    counts: Counter[str],
) -> Iterable[dict[str, str]]:
    for action_path in sorted(source_dir.rglob("action_log.json")):
        video_path = action_path.parent / "video" / "video.mp4"
        if not video_path.exists():
            continue

        with action_path.open("r", encoding="utf-8") as file:
            task_data = json.load(file)

        platform = str(task_data.get("platform", ""))
        instruction = str(task_data.get("task_instruction", ""))
        label = infer_label(platform, instruction)
        label_text = label or "unlabeled"

        if label is None and not include_unlabeled:
            continue
        if limit_per_label > 0 and counts[label_text] >= limit_per_label:
            continue

        with video_path.open("rb") as video_source:
            row = extract_task(
                task_data,
                video_source,
                str(action_path.parent),
                label_text,
            )

        counts[label_text] += 1
        yield row


def write_index(rows: list[dict[str, str]]) -> None:
    VIDEO_CUA_DIR.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "task_id",
        "platform",
        "instruction",
        "label",
        "video_path",
        "timeline_path",
        "last_action_sec",
        "source",
    ]

    with VIDEO_CUA_INDEX.open(
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "VideoCUA에서 학습에 필요한 video + timestamp timeline만 추출합니다."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="VideoCUA raw_data 폴더 또는 압축 해제된 데이터 폴더",
    )
    parser.add_argument(
        "--include-unlabeled",
        action="store_true",
        help="현재 activity label로 매핑되지 않는 task도 보존",
    )
    parser.add_argument(
        "--limit-per-label",
        type=int,
        default=0,
        help="label별 최대 task 수. 0이면 제한 없음",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source

    if not source.exists():
        raise SystemExit(f"source가 존재하지 않습니다: {source}")

    VIDEO_CUA_DIR.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    counts: Counter[str] = Counter()

    zip_files = sorted(source.glob("*.zip")) if source.is_dir() else []
    if source.is_file() and source.suffix.lower() == ".zip":
        zip_files = [source]

    if zip_files:
        for index, zip_path in enumerate(zip_files, start=1):
            print(f"[{index}/{len(zip_files)}] {zip_path.name}")
            for row in rows_from_zip(
                zip_path,
                include_unlabeled=args.include_unlabeled,
                limit_per_label=args.limit_per_label,
                counts=counts,
            ):
                if row["label"] in ACTIVITY_PROMPTS or row["label"] == "unlabeled":
                    rows.append(row)
    else:
        for row in rows_from_directory(
            source,
            include_unlabeled=args.include_unlabeled,
            limit_per_label=args.limit_per_label,
            counts=counts,
        ):
            if row["label"] in ACTIVITY_PROMPTS or row["label"] == "unlabeled":
                rows.append(row)

    write_index(rows)

    print(f"saved tasks: {len(rows)}")
    for label, count in sorted(counts.items()):
        print(f"  {label}: {count}")
    print(f"index: {VIDEO_CUA_INDEX}")


if __name__ == "__main__":
    main()
