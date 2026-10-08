from __future__ import annotations

import time

from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from gru_activity_tracker.gui.dashboard import Dashboard
from gru_activity_tracker.gui.theme import APP_STYLE
from gru_activity_tracker.gui.tracker_worker import TrackerWorker


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Activity Tracker")
        self.resize(1450, 900)
        self.setMinimumSize(1120, 720)

        self.worker: TrackerWorker | None = None
        self.tracking_started_at: float | None = None
        self.paused = False
        self.last_label: str | None = None
        self.session_count = 0

        root = QWidget()
        root.setObjectName("AppRoot")
        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.nav_buttons: list[QPushButton] = []
        root_layout.addWidget(self._build_sidebar())

        self.page_stack = QStackedWidget()
        self.page_stack.setObjectName("PageStack")

        scroll = QScrollArea()
        scroll.setObjectName("ContentScroll")
        scroll.viewport().setObjectName("ContentViewport")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.dashboard = Dashboard()
        scroll.setWidget(self.dashboard)

        self.page_stack.addWidget(
            self._placeholder_page(
                "대시보드",
                "오늘의 활동 요약과 통계를 표시하는 화면입니다.",
            )
        )
        self.page_stack.addWidget(scroll)
        self.page_stack.addWidget(
            self._placeholder_page(
                "활동 기록",
                "저장된 활동 세션과 CSV 기록을 확인하는 화면입니다.",
            )
        )
        self.page_stack.addWidget(
            self._placeholder_page(
                "타임라인",
                "시간대별 활동 변화를 자세히 확인하는 화면입니다.",
            )
        )
        self.page_stack.addWidget(
            self._placeholder_page(
                "내보내기",
                "활동 기록을 CSV 또는 다른 형식으로 내보내는 화면입니다.",
            )
        )
        self.page_stack.addWidget(
            self._placeholder_page(
                "설정",
                "추적 간격과 저장 위치 같은 옵션을 설정하는 화면입니다.",
            )
        )
        root_layout.addWidget(self.page_stack, 1)

        self.setCentralWidget(root)
        self._connect_controls()
        self.switch_page(1)

        self.clock_timer = QTimer(self)
        self.clock_timer.timeout.connect(self._tick)
        self.clock_timer.start(500)
        self._tick()

    def _build_sidebar(self) -> QFrame:
        sidebar = QFrame()
        sidebar.setObjectName("Sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(18, 24, 18, 18)
        layout.setSpacing(8)

        brand = QLabel("◉  Activity Tracker")
        brand.setObjectName("BrandTitle")
        layout.addWidget(brand)

        subtitle = QLabel("집중을 위한 활동 기록")
        subtitle.setObjectName("BrandSub")
        layout.addWidget(subtitle)
        layout.addSpacing(24)

        items = [
            ("⌂   대시보드", 0),
            ("◉   실시간 추적", 1),
            ("▤   활동 기록", 2),
            ("▥   타임라인", 3),
            ("⇩   내보내기", 4),
            ("⚙   설정", 5),
        ]

        for text, page_index in items:
            button = QPushButton(text)
            button.setObjectName("NavButton")
            button.setProperty("active", page_index == 1)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked=False, index=page_index: self.switch_page(index)
            )
            layout.addWidget(button)
            self.nav_buttons.append(button)

        layout.addStretch(1)

        footer = QFrame()
        footer.setObjectName("Card")
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(12, 12, 12, 12)

        footer_title = QLabel("스마트 활동 추적")
        footer_title.setObjectName("CardTitle")
        footer_layout.addWidget(footer_title)

        footer_text = QLabel("CLIP + GRU로 화면 활동을 실시간 분류합니다.")
        footer_text.setObjectName("Muted")
        footer_text.setWordWrap(True)
        footer_layout.addWidget(footer_text)
        layout.addWidget(footer)

        version = QLabel("v1.0.0")
        version.setObjectName("Muted")
        layout.addWidget(version)
        return sidebar

    def _placeholder_page(self, title_text: str, body_text: str) -> QWidget:
        page = QWidget()
        page.setObjectName("PlaceholderPage")

        layout = QVBoxLayout(page)
        layout.setContentsMargins(30, 28, 30, 30)
        layout.setSpacing(10)

        title = QLabel(title_text)
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        subtitle = QLabel(body_text)
        subtitle.setObjectName("PageSubtitle")
        subtitle.setWordWrap(True)
        layout.addWidget(subtitle)

        card = QFrame()
        card.setObjectName("Panel")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(22, 22, 22, 22)

        message = QLabel("이 메뉴는 선택할 수 있도록 연결되어 있으며, 상세 기능은 이후 확장할 수 있습니다.")
        message.setObjectName("Muted")
        message.setWordWrap(True)
        card_layout.addWidget(message)

        layout.addSpacing(12)
        layout.addWidget(card)
        layout.addStretch(1)
        return page

    def switch_page(self, index: int) -> None:
        if not 0 <= index < self.page_stack.count():
            return

        self.page_stack.setCurrentIndex(index)

        for button_index, button in enumerate(self.nav_buttons):
            button.setProperty("active", button_index == index)
            button.style().unpolish(button)
            button.style().polish(button)
            button.update()

    def _connect_controls(self) -> None:
        controls = self.dashboard.controls
        controls.start_button.clicked.connect(self.start_tracking)
        controls.pause_button.clicked.connect(self.toggle_pause)
        controls.stop_button.clicked.connect(self.stop_tracking)

    def start_tracking(self) -> None:
        if self.worker is not None and self.worker.isRunning():
            return

        self.last_label = None
        self.session_count = 0
        self.paused = False
        self.tracking_started_at = time.monotonic()

        self.dashboard.set_session_count(0)
        self.dashboard.set_status("LOADING")
        self.dashboard.controls.set_tracking(True)

        worker = TrackerWorker(interval=1.0)
        worker.ready.connect(self._on_worker_ready)
        worker.prediction.connect(self._on_prediction)
        worker.failed.connect(self._on_worker_failed)
        worker.finished.connect(self._on_worker_finished)
        self.worker = worker
        worker.start()

    def toggle_pause(self) -> None:
        if self.worker is None or not self.worker.isRunning():
            return

        self.paused = not self.paused
        if self.paused:
            self.worker.pause()
            self.dashboard.set_status("PAUSED")
        else:
            self.worker.resume()
            self.dashboard.set_status("RUNNING")

        self.dashboard.controls.set_tracking(True, paused=self.paused)

    def stop_tracking(self) -> None:
        if self.worker is None:
            return

        self.worker.stop()
        self.dashboard.set_status("STOPPED")
        self.dashboard.controls.set_tracking(False)
        self.dashboard.reset_current()
        self.paused = False

    def _on_worker_ready(self, device: str) -> None:
        self.dashboard.set_status("RUNNING")
        self.statusBar().showMessage(f"AI 모델 준비 완료 · device={device}", 5000)

    def _on_prediction(self, label: str, score: float, when: object) -> None:
        from datetime import datetime

        if not isinstance(when, datetime):
            return

        new_session = label != self.last_label
        if new_session:
            self.session_count += 1
            self.dashboard.set_session_count(self.session_count)
            self.last_label = label

        self.dashboard.update_prediction(label, score, when, new_session)

    def _on_worker_failed(self, message: str) -> None:
        self.dashboard.set_status("STOPPED")
        self.dashboard.controls.set_tracking(False)
        self.dashboard.reset_current()

        QMessageBox.critical(
            self,
            "Activity Tracker",
            "추적 중 오류가 발생했습니다.\n\n" + message,
        )

    def _on_worker_finished(self) -> None:
        if self.worker is not None:
            self.worker.deleteLater()
        self.worker = None
        self.paused = False
        self.dashboard.controls.set_tracking(False)

    def _tick(self) -> None:
        from datetime import datetime

        self.dashboard.update_clock(datetime.now())

        if self.tracking_started_at is not None and self.worker is not None:
            elapsed = int(time.monotonic() - self.tracking_started_at)
            self.dashboard.set_session_elapsed(elapsed)

    def closeEvent(self, event: QCloseEvent) -> None:
        if self.worker is not None and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()


def run_app() -> int:
    app = QApplication.instance()
    owns_app = app is None
    if app is None:
        app = QApplication([])

    app.setApplicationName("Activity Tracker")
    app.setOrganizationName("ActivityTracker")
    app.setStyleSheet(APP_STYLE)

    window = MainWindow()
    window.show()

    if owns_app:
        return app.exec()
    return 0
