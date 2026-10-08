from __future__ import annotations

from collections import Counter

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QPen
from PySide6.QtWidgets import QWidget

from gru_activity_tracker.gui.constants import activity_color


class DonutChart(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.counts: Counter[str] = Counter()
        self.setMinimumSize(210, 210)

    def add_sample(self, label: str) -> None:
        self.counts[label] += 1
        self.update()

    def clear(self) -> None:
        self.counts.clear()
        self.update()

    def paintEvent(self, event) -> None:  # type: ignore[override]
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        size = max(min(self.width(), self.height()) - 58, 80)
        rect = QRectF((self.width() - size) / 2, 14, size, size)

        total = sum(self.counts.values())
        if total == 0:
            painter.setPen(QPen(QColor("#26344a"), 18))
            painter.drawEllipse(rect)
        else:
            start_angle = 90 * 16
            pen_width = max(14, int(size * 0.12))
            for label, count in self.counts.most_common():
                span = -int(360 * 16 * count / total)
                painter.setPen(QPen(QColor(activity_color(label)), pen_width))
                painter.drawArc(rect, start_angle, span)
                start_angle += span

        painter.setPen(QColor("#f5f8fc"))
        painter.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(total))

        painter.setPen(QColor("#8290a5"))
        painter.setFont(QFont("Segoe UI", 9))
        caption_rect = QRectF(rect.x(), rect.center().y() + 18, rect.width(), 24)
        painter.drawText(caption_rect, Qt.AlignmentFlag.AlignCenter, "samples")
