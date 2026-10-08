from __future__ import annotations

from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from gru_activity_tracker.gui.constants import activity_color, display_name


class ActivityTable(QTableWidget):
    def __init__(self) -> None:
        super().__init__(0, 3)
        self.setHorizontalHeaderLabels(["시간", "활동", "신뢰도"])
        self.verticalHeader().setVisible(False)
        self.setShowGrid(False)
        self.setAlternatingRowColors(True)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        header = self.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.setMinimumHeight(190)

    def add_activity(self, when: datetime, label: str, score: float) -> None:
        self.insertRow(0)

        time_item = QTableWidgetItem(when.strftime("%H:%M:%S"))
        activity_item = QTableWidgetItem(display_name(label))
        score_item = QTableWidgetItem(f"{score * 100:.1f}%")

        activity_item.setForeground(QColor(activity_color(label)))
        time_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        score_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setItem(0, 0, time_item)
        self.setItem(0, 1, activity_item)
        self.setItem(0, 2, score_item)

        while self.rowCount() > 8:
            self.removeRow(self.rowCount() - 1)
