from __future__ import annotations

from collections import Counter

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter
from PySide6.QtWidgets import QWidget

from gru_activity_tracker.gui.constants import activity_color, display_name


class TimelineWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.samples: list[str] = []
        self.setMinimumHeight(145)

    def append_sample(self, label: str) -> None:
        self.samples.append(label)
        if len(self.samples) > 180:
            self.samples = self.samples[-180:]
        self.update()

    def clear(self) -> None:
        self.samples.clear()
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = max(self.width() - 20, 1)
        bar = QRectF(10, 26, width, 38)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#1b2638"))
        painter.drawRoundedRect(bar, 8, 8)

        if not self.samples:
            painter.setPen(QColor("#738198"))
            painter.drawText(
                QRectF(10, 72, width, 28),
                Qt.AlignmentFlag.AlignCenter,
                "추적을 시작하면 활동 타임라인이 표시됩니다.",
            )
            return

        runs: list[tuple[str, int]] = []
        for label in self.samples:
            if runs and runs[-1][0] == label:
                prev_label, count = runs[-1]
                runs[-1] = (prev_label, count + 1)
            else:
                runs.append((label, 1))

        total = len(self.samples)
        x = bar.x()
        for label, count in runs:
            segment_width = bar.width() * count / total
            rect = QRectF(
                x + 1,
                bar.y() + 1,
                max(segment_width - 2, 2),
                bar.height() - 2,
            )
            painter.setBrush(QColor(activity_color(label)))
            painter.drawRoundedRect(rect, 6, 6)
            x += segment_width

        painter.setPen(QColor("#708097"))
        painter.setFont(QFont("Segoe UI", 9))
        painter.drawText(10, 87, "Earlier")
        painter.drawText(self.width() - 44, 87, "Now")

        counts = Counter(self.samples)
        legend_y = 110
        legend_x = 10
        for label, _ in counts.most_common(4):
            painter.setBrush(QColor(activity_color(label)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(QRectF(legend_x, legend_y - 8, 9, 9))
            painter.setPen(QColor("#aab6c8"))
            label_text = display_name(label)
            painter.drawText(legend_x + 14, legend_y, label_text)
            legend_x += min(150, 28 + len(label_text) * 11)
