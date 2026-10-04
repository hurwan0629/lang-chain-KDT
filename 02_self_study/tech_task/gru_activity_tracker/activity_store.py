from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class ActiveSession:
    start_time: datetime
    label: str
    score: float


class ActivityStore:
    def __init__(self, output_path: Path) -> None:
        self.output_path = output_path
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        self.current: ActiveSession | None = None

        if not output_path.exists():
            with output_path.open("w", newline="", encoding="utf-8-sig") as file:
                csv.writer(file).writerow([
                    "start_time",
                    "end_time",
                    "duration_seconds",
                    "predicted_label",
                    "score",
                ])

    def update(self, label: str, score: float, now: datetime) -> None:
        if self.current is None:
            self.current = ActiveSession(now, label, score)
            return

        if self.current.label == label:
            self.current.score = score
            return

        self._flush(now)
        self.current = ActiveSession(now, label, score)

    def close(self) -> None:
        if self.current is not None:
            self._flush(datetime.now())
            self.current = None

    def _flush(self, end_time: datetime) -> None:
        assert self.current is not None
        duration = (end_time - self.current.start_time).total_seconds()

        with self.output_path.open("a", newline="", encoding="utf-8-sig") as file:
            csv.writer(file).writerow([
                self.current.start_time.isoformat(timespec="seconds"),
                end_time.isoformat(timespec="seconds"),
                round(duration, 3),
                self.current.label,
                round(self.current.score, 6),
            ])
