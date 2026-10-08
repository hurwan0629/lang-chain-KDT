from __future__ import annotations

from PySide6.QtWidgets import QCheckBox, QFrame, QLabel, QPushButton, QVBoxLayout


class ControlPanel(QFrame):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("Panel")
        self.setMinimumWidth(245)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title = QLabel("⚡  빠른 제어")
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        layout.addSpacing(8)

        self.start_button = QPushButton("▶   추적 시작")
        self.start_button.setObjectName("PrimaryButton")
        layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Ⅱ   일시정지")
        self.pause_button.setObjectName("SecondaryButton")
        self.pause_button.setEnabled(False)
        layout.addWidget(self.pause_button)

        self.stop_button = QPushButton("■   중지")
        self.stop_button.setObjectName("DangerButton")
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        layout.addStretch(1)

        self.auto_save = QCheckBox("자동 저장")
        self.auto_save.setChecked(True)
        self.auto_save.setEnabled(False)
        layout.addWidget(self.auto_save)

        caption = QLabel("활동 변경과 종료 시 CSV에 자동 저장됩니다.")
        caption.setObjectName("Muted")
        caption.setWordWrap(True)
        layout.addWidget(caption)

    def set_tracking(self, running: bool, paused: bool = False) -> None:
        self.start_button.setEnabled(not running)
        self.pause_button.setEnabled(running)
        self.stop_button.setEnabled(running)
        self.pause_button.setText("▶   계속하기" if paused else "Ⅱ   일시정지")
