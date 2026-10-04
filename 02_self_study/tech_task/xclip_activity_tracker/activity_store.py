from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class ActiveSession:
    start_time: datetime
    last_seen_at: datetime
    label: str
    score: float


class ActivityStore:
    """연속된 동일 상태를 하나의 시간 구간으로 묶어 CSV에 저장한다."""

    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.current: ActiveSession | None = None
        self._ensure_header()

    def _ensure_header(self) -> None:
        if self.output_path.exists() and self.output_path.stat().st_size > 0:
            return

        with self.output_path.open(
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as file:
            csv.writer(file).writerow([
                "start_time",
                "end_time",
                "duration_seconds",
                "predicted_label",
                "user_label",
                "score",
            ])

    def update(
        self,
        label: str,
        score: float,
        timestamp: datetime | None = None,
    ) -> None:
        now = timestamp or datetime.now()

        if self.current is None:
            self.current = ActiveSession(
                start_time=now,
                last_seen_at=now,
                label=label,
                score=score,
            )
            return

        if label == self.current.label:
            self.current.last_seen_at = now
            self.current.score = score
            return

        self._flush(end_time=now)
        self.current = ActiveSession(
            start_time=now,
            last_seen_at=now,
            label=label,
            score=score,
        )

    def close(self) -> None:
        if self.current is not None:
            self._flush(end_time=datetime.now())
            self.current = None

    def _flush(self, end_time: datetime) -> None:
        assert self.current is not None

        duration = (end_time - self.current.start_time).total_seconds()

        with self.output_path.open(
            "a",
            newline="",
            encoding="utf-8-sig",
        ) as file:
            csv.writer(file).writerow([
                self.current.start_time.isoformat(timespec="seconds"),
                end_time.isoformat(timespec="seconds"),
                round(duration, 3),
                self.current.label,
                "",
                round(self.current.score, 6),
            ])
