from __future__ import annotations


ACTIVITY_NAMES = {
    "coding_or_terminal": "코딩 / 터미널",
    "web_browsing": "웹 브라우징",
    "paper_or_document": "문서 / 자료 읽기",
    "training_monitoring": "학습 모니터링",
    "file_or_desktop": "파일 / 데스크톱",
    "communication": "커뮤니케이션",
    "other_screen_work": "기타 화면 작업",
    "non_screen_or_idle": "자리 비움 / 유휴",
}

ACTIVITY_COLORS = {
    "coding_or_terminal": "#6f7cff",
    "web_browsing": "#f4ae4f",
    "paper_or_document": "#4fd69c",
    "training_monitoring": "#4f9cf9",
    "file_or_desktop": "#8c9cb4",
    "communication": "#ef6f91",
    "other_screen_work": "#9a78ff",
    "non_screen_or_idle": "#59667a",
}


def display_name(label: str) -> str:
    return ACTIVITY_NAMES.get(label, label.replace("_", " ").title())


def activity_color(label: str) -> str:
    return ACTIVITY_COLORS.get(label, "#74839b")
