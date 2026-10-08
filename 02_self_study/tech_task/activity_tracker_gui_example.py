from __future__ import annotations

import random
import time
import tkinter as tk
from datetime import datetime
from tkinter import ttk


ACTIVITIES = [
    ("coding_or_terminal", "코딩 / 터미널"),
    ("web_browsing", "웹 브라우징"),
    ("paper_or_document", "문서 작업"),
    ("training_monitoring", "학습 모니터링"),
    ("file_or_desktop", "파일 / 데스크톱"),
    ("communication", "커뮤니케이션"),
    ("other_screen_work", "기타 화면 작업"),
    ("non_screen_or_idle", "자리 비움 / 유휴"),
]


class ActivityTrackerDemo(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Activity Tracker")
        self.geometry("900x620")
        self.minsize(780, 540)

        self.running = False
        self.started_at: float | None = None
        self.current_activity = "-"
        self.current_score = 0.0
        self.session_count = 0

        self._configure_style()
        self._build_ui()
        self._tick_clock()

    def _configure_style(self) -> None:
        style = ttk.Style(self)
        if "vista" in style.theme_names():
            style.theme_use("vista")

        style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"))
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10))
        style.configure("CardTitle.TLabel", font=("Segoe UI", 10, "bold"))
        style.configure("Activity.TLabel", font=("Segoe UI", 24, "bold"))
        style.configure("Metric.TLabel", font=("Segoe UI", 17, "bold"))
        style.configure("TButton", font=("Segoe UI", 10), padding=(14, 8))
        style.configure("Treeview", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

    def _build_ui(self) -> None:
        root = ttk.Frame(self, padding=24)
        root.pack(fill="both", expand=True)

        # Header
        header = ttk.Frame(root)
        header.pack(fill="x")

        title_box = ttk.Frame(header)
        title_box.pack(side="left")

        ttk.Label(
            title_box,
            text="Activity Tracker",
            style="Title.TLabel",
        ).pack(anchor="w")

        ttk.Label(
            title_box,
            text="데스크톱 활동 자동 분류 GUI 예시 · 현재는 데모 데이터",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        self.status_badge = ttk.Label(
            header,
            text="● STOPPED",
            font=("Segoe UI", 10, "bold"),
        )
        self.status_badge.pack(side="right", anchor="n", pady=8)

        ttk.Separator(root).pack(fill="x", pady=18)

        # Current activity card
        current = ttk.LabelFrame(root, text=" 현재 활동 ", padding=20)
        current.pack(fill="x")

        self.activity_label = ttk.Label(
            current,
            text="추적을 시작해 주세요",
            style="Activity.TLabel",
        )
        self.activity_label.pack(anchor="w")

        self.activity_key_label = ttk.Label(
            current,
            text="label: -",
            style="Subtitle.TLabel",
        )
        self.activity_key_label.pack(anchor="w", pady=(4, 14))

        score_line = ttk.Frame(current)
        score_line.pack(fill="x")

        ttk.Label(score_line, text="신뢰도").pack(side="left")

        self.score_text = ttk.Label(
            score_line,
            text="0.0%",
            font=("Segoe UI", 10, "bold"),
        )
        self.score_text.pack(side="right")

        self.score_bar = ttk.Progressbar(
            current,
            orient="horizontal",
            mode="determinate",
            maximum=100,
        )
        self.score_bar.pack(fill="x", pady=(6, 0))

        # Metrics
        metrics = ttk.Frame(root)
        metrics.pack(fill="x", pady=18)

        self.elapsed_value = self._metric_card(metrics, "세션 시간", "00:00:00")
        self.samples_value = self._metric_card(metrics, "분류 횟수", "0")
        self.clock_value = self._metric_card(metrics, "현재 시각", "--:--:--")

        # Controls
        controls = ttk.Frame(root)
        controls.pack(fill="x", pady=(0, 16))

        self.start_btn = ttk.Button(
            controls,
            text="▶ 추적 시작",
            command=self.start_tracking,
        )
        self.start_btn.pack(side="left")

        self.stop_btn = ttk.Button(
            controls,
            text="■ 중지",
            command=self.stop_tracking,
            state="disabled",
        )
        self.stop_btn.pack(side="left", padx=8)

        ttk.Button(
            controls,
            text="기록 비우기",
            command=self.clear_history,
        ).pack(side="right")

        # Recent activity table
        history_box = ttk.LabelFrame(root, text=" 최근 활동 ", padding=10)
        history_box.pack(fill="both", expand=True)

        columns = ("time", "activity", "score")
        self.tree = ttk.Treeview(
            history_box,
            columns=columns,
            show="headings",
            height=8,
        )
        self.tree.heading("time", text="시각")
        self.tree.heading("activity", text="활동")
        self.tree.heading("score", text="신뢰도")

        self.tree.column("time", width=120, anchor="center")
        self.tree.column("activity", width=430, anchor="w")
        self.tree.column("score", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            history_box,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        footer = ttk.Label(
            root,
            text="실제 프로젝트에서는 이 데모 분류 부분을 CLIP + GRU 추론 결과로 교체하면 됩니다.",
            style="Subtitle.TLabel",
        )
        footer.pack(anchor="w", pady=(12, 0))

    def _metric_card(
        self,
        parent: ttk.Frame,
        title: str,
        initial: str,
    ) -> ttk.Label:
        card = ttk.LabelFrame(parent, text=f" {title} ", padding=(18, 12))
        card.pack(side="left", fill="x", expand=True, padx=4)

        value = ttk.Label(card, text=initial, style="Metric.TLabel")
        value.pack(anchor="center")
        return value

    def start_tracking(self) -> None:
        if self.running:
            return

        self.running = True
        self.started_at = time.monotonic()
        self.session_count = 0

        self.status_badge.config(text="● RUNNING")
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")

        self._simulate_prediction()

    def stop_tracking(self) -> None:
        self.running = False
        self.status_badge.config(text="● STOPPED")
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

        self.activity_label.config(text="추적이 중지되었습니다")
        self.activity_key_label.config(text=f"label: {self.current_activity}")

    def clear_history(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.session_count = 0
        self.samples_value.config(text="0")

    def _simulate_prediction(self) -> None:
        if not self.running:
            return

        key, display = random.choice(ACTIVITIES)
        score = random.uniform(0.58, 0.98)

        self.current_activity = key
        self.current_score = score
        self.session_count += 1

        self.activity_label.config(text=display)
        self.activity_key_label.config(text=f"label: {key}")
        self.score_bar["value"] = score * 100
        self.score_text.config(text=f"{score * 100:.1f}%")
        self.samples_value.config(text=str(self.session_count))

        now = datetime.now().strftime("%H:%M:%S")
        self.tree.insert(
            "",
            0,
            values=(now, display, f"{score * 100:.1f}%"),
        )

        # Keep only the latest 30 rows.
        items = self.tree.get_children()
        if len(items) > 30:
            self.tree.delete(items[-1])

        self.after(2000, self._simulate_prediction)

    def _tick_clock(self) -> None:
        now = datetime.now()
        self.clock_value.config(text=now.strftime("%H:%M:%S"))

        if self.running and self.started_at is not None:
            elapsed = int(time.monotonic() - self.started_at)
            hours, remainder = divmod(elapsed, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.elapsed_value.config(
                text=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            )

        self.after(500, self._tick_clock)


if __name__ == "__main__":
    app = ActivityTrackerDemo()
    app.mainloop()
