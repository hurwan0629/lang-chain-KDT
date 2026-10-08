from __future__ import annotations

import threading
import time

from PySide6.QtCore import QThread, Signal

from gru_activity_tracker.runtime.predictor import ActivityPredictor


class TrackerWorker(QThread):
    ready = Signal(str)
    prediction = Signal(str, float, object)
    failed = Signal(str)

    def __init__(self, interval: float = 1.0) -> None:
        super().__init__()
        self.interval = max(interval, 0.1)
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()

    def pause(self) -> None:
        self._pause_event.set()

    def resume(self) -> None:
        self._pause_event.clear()

    def stop(self) -> None:
        self._stop_event.set()
        self._pause_event.clear()

    def run(self) -> None:
        predictor: ActivityPredictor | None = None
        try:
            predictor = ActivityPredictor()
            self.ready.emit(str(predictor.device))

            while not self._stop_event.is_set():
                if self._pause_event.is_set():
                    self.msleep(100)
                    continue

                started_at = time.monotonic()
                label, score, now = predictor.predict_screen()
                self.prediction.emit(label, score, now)

                remaining = self.interval - (time.monotonic() - started_at)
                while remaining > 0 and not self._stop_event.is_set():
                    sleep_for = min(remaining, 0.1)
                    time.sleep(sleep_for)
                    remaining -= sleep_for
        except Exception as exc:
            self.failed.emit(f"{type(exc).__name__}: {exc}")
        finally:
            if predictor is not None:
                predictor.close()
