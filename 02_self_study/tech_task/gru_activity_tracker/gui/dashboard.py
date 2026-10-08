from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from gru_activity_tracker.gui.activity_table import ActivityTable
from gru_activity_tracker.gui.constants import display_name
from gru_activity_tracker.gui.control_panel import ControlPanel
from gru_activity_tracker.gui.current_panel import CurrentActivityPanel
from gru_activity_tracker.gui.donut_chart import DonutChart
from gru_activity_tracker.gui.stat_card import StatCard
from gru_activity_tracker.gui.timeline_widget import TimelineWidget


class Dashboard(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setMinimumWidth(1040)

        root = QVBoxLayout(self)
        root.setContentsMargins(26, 22, 26, 26)
        root.setSpacing(16)

        header = QHBoxLayout()
        title_box = QVBoxLayout()

        title_row = QHBoxLayout()
        title = QLabel("실시간 활동 추적기")
        title.setObjectName("PageTitle")
        title_row.addWidget(title)

        self.status_badge = QLabel("STOPPED")
        self.status_badge.setObjectName("StatusStopped")
        title_row.addWidget(self.status_badge)
        title_row.addStretch(1)

        title_box.addLayout(title_row)

        subtitle = QLabel("지금 하고 있는 활동을 실시간으로 분석하고 기록합니다.")
        subtitle.setObjectName("PageSubtitle")
        title_box.addWidget(subtitle)

        header.addLayout(title_box, 1)

        self.clock_label = QLabel("--")
        self.clock_label.setObjectName("Muted")
        self.clock_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        header.addWidget(self.clock_label)
        root.addLayout(header)

        cards = QGridLayout()
        cards.setHorizontalSpacing(12)
        cards.setVerticalSpacing(12)

        self.activity_card = StatCard("현재 활동", "-", "지금 이 순간의 활동")
        self.confidence_card = StatCard("신뢰도", "0%", "AI 분석 신뢰도")
        self.session_card = StatCard("세션 시간", "00:00:00", "현재 세션 지속 시간")
        self.count_card = StatCard("오늘 기록", "0 세션", "현재 실행에서 감지된 세션")

        for index, card in enumerate(
            (
                self.activity_card,
                self.confidence_card,
                self.session_card,
                self.count_card,
            )
        ):
            card.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Preferred,
            )
            cards.addWidget(card, 0, index)

        root.addLayout(cards)

        middle = QHBoxLayout()
        middle.setSpacing(14)

        self.current_panel = CurrentActivityPanel()
        middle.addWidget(self.current_panel, 3)

        self.controls = ControlPanel()
        middle.addWidget(self.controls, 1)
        root.addLayout(middle)

        bottom = QHBoxLayout()
        bottom.setSpacing(14)

        timeline_panel, timeline_layout = self._panel("▥  오늘의 활동 타임라인")
        self.timeline = TimelineWidget()
        timeline_layout.addWidget(self.timeline)
        bottom.addWidget(timeline_panel, 5)

        history_panel, history_layout = self._panel("◷  최근 활동 기록")
        self.activity_table = ActivityTable()
        history_layout.addWidget(self.activity_table)
        bottom.addWidget(history_panel, 4)

        donut_panel, donut_layout = self._panel("◔  활동 비율")
        self.donut = DonutChart()
        donut_layout.addWidget(self.donut)
        bottom.addWidget(donut_panel, 3)

        root.addLayout(bottom, 1)

    @staticmethod
    def _panel(title_text: str) -> tuple[QFrame, QVBoxLayout]:
        panel = QFrame()
        panel.setObjectName("Panel")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(16, 15, 16, 15)
        layout.setSpacing(8)

        title = QLabel(title_text)
        title.setObjectName("PanelTitle")
        layout.addWidget(title)
        return panel, layout

    def set_status(self, status: str) -> None:
        status = status.upper()
        object_name = {
            "RUNNING": "StatusRunning",
            "LOADING": "StatusLoading",
            "PAUSED": "StatusLoading",
        }.get(status, "StatusStopped")

        self.status_badge.setText(status)
        self.status_badge.setObjectName(object_name)
        style = self.status_badge.style()
        style.unpolish(self.status_badge)
        style.polish(self.status_badge)

    def update_clock(self, now: datetime) -> None:
        weekdays = ("월", "화", "수", "목", "금", "토", "일")
        weekday = weekdays[now.weekday()]
        self.clock_label.setText(
            f"{now:%Y년 %m월 %d일} ({weekday})   {now:%H:%M:%S}"
        )

    def update_prediction(
        self,
        label: str,
        score: float,
        when: datetime,
        new_session: bool,
    ) -> None:
        name = display_name(label)
        self.activity_card.set_value(name)
        self.confidence_card.set_value(f"{score * 100:.1f}%")
        self.current_panel.set_activity(label, score)
        self.timeline.append_sample(label)
        self.donut.add_sample(label)

        if new_session:
            self.activity_table.add_activity(when, label, score)

    def set_session_elapsed(self, elapsed_seconds: int) -> None:
        hours, remainder = divmod(max(elapsed_seconds, 0), 3600)
        minutes, seconds = divmod(remainder, 60)
        self.session_card.set_value(
            f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )

    def set_session_count(self, count: int) -> None:
        self.count_card.set_value(f"{count} 세션")

    def reset_current(self) -> None:
        self.activity_card.set_value("-")
        self.confidence_card.set_value("0%")
        self.current_panel.set_stopped()
