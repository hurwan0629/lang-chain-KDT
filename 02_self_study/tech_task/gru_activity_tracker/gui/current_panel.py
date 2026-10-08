from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QProgressBar, QVBoxLayout

from gru_activity_tracker.gui.constants import display_name


class CurrentActivityPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("CurrentPanel")
        self.setMinimumHeight(270)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 22)
        layout.setSpacing(10)

        title = QLabel("●  현재 상태")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        layout.addSpacing(16)

        self.activity = QLabel("추적을 시작해 주세요")
        self.activity.setObjectName("CurrentActivity")
        self.activity.setWordWrap(True)
        layout.addWidget(self.activity)

        self.raw_label = QLabel("-")
        self.raw_label.setObjectName("RawLabel")
        self.raw_label.setMaximumWidth(260)
        layout.addWidget(self.raw_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addStretch(1)

        score_row = QHBoxLayout()
        score_title = QLabel("신뢰도")
        score_title.setObjectName("Muted")
        score_row.addWidget(score_title)
        score_row.addStretch(1)
        self.score_text = QLabel("0%")
        self.score_text.setStyleSheet("font-weight: 800; color: #e8eef9;")
        score_row.addWidget(self.score_text)
        layout.addLayout(score_row)

        self.progress = QProgressBar()
        self.progress.setRange(0, 1000)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)
        layout.addWidget(self.progress)

    def set_activity(self, label: str, score: float) -> None:
        self.activity.setText(display_name(label))
        self.raw_label.setText(label)
        percent = max(0.0, min(score * 100.0, 100.0))
        self.score_text.setText(f"{percent:.1f}%")
        self.progress.setValue(round(percent * 10))

    def set_stopped(self) -> None:
        self.activity.setText("추적이 중지되었습니다")
        self.raw_label.setText("-")
        self.score_text.setText("0%")
        self.progress.setValue(0)
