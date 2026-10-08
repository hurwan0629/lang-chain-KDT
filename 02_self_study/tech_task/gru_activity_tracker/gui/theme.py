from __future__ import annotations


APP_STYLE = r"""
QMainWindow, QWidget#AppRoot {
    background: #0b1220;
    color: #e8eef9;
    font-family: "Segoe UI", "Malgun Gothic";
    font-size: 13px;
}

QStackedWidget#PageStack,
QScrollArea#ContentScroll,
QWidget#ContentViewport,
QWidget#PlaceholderPage {
    background: #0b1220;
    color: #e8eef9;
    border: none;
}

QFrame#Sidebar {
    background: #101827;
    border-right: 1px solid #1f2a3b;
}

QLabel#BrandTitle {
    font-size: 18px;
    font-weight: 700;
    color: #f6f8fc;
}

QLabel#BrandSub, QLabel#Muted, QLabel#CardCaption {
    color: #8592a8;
}

QLabel#PageTitle {
    font-size: 28px;
    font-weight: 800;
    color: #f8fbff;
}

QLabel#PageSubtitle {
    color: #8f9bb0;
    font-size: 13px;
}

QPushButton#NavButton {
    text-align: left;
    padding: 12px 16px;
    border: 0;
    border-radius: 9px;
    color: #aab6c8;
    background: transparent;
    font-size: 14px;
}

QPushButton#NavButton:hover {
    background: #162238;
    color: #dce7f7;
}

QPushButton#NavButton[active="true"] {
    background: #1d2e4d;
    color: #6fa6ff;
    font-weight: 700;
}

QFrame#Card, QFrame#Panel {
    background: #111b2b;
    border: 1px solid #223047;
    border-radius: 14px;
}

QFrame#CurrentPanel {
    background: #121d31;
    border: 1px solid #293b58;
    border-radius: 16px;
}

QLabel#CardTitle, QLabel#PanelTitle {
    color: #d9e3f2;
    font-weight: 700;
    font-size: 14px;
}

QLabel#CardValue {
    color: #f7f9fd;
    font-weight: 800;
    font-size: 24px;
}

QLabel#CurrentActivity {
    color: #ffffff;
    font-size: 31px;
    font-weight: 800;
}

QLabel#RawLabel {
    color: #9eb4d8;
    background: #1c2940;
    border: 1px solid #2b3a55;
    border-radius: 9px;
    padding: 4px 9px;
}

QLabel#StatusRunning {
    color: #61e7a5;
    background: #123b31;
    border: 1px solid #1d5a48;
    border-radius: 12px;
    padding: 5px 10px;
    font-weight: 700;
}

QLabel#StatusStopped {
    color: #9aa8bc;
    background: #172233;
    border: 1px solid #29384e;
    border-radius: 12px;
    padding: 5px 10px;
    font-weight: 700;
}

QLabel#StatusLoading {
    color: #ffd27a;
    background: #3a2c14;
    border: 1px solid #5d4720;
    border-radius: 12px;
    padding: 5px 10px;
    font-weight: 700;
}

QProgressBar {
    min-height: 13px;
    max-height: 13px;
    border: 0;
    border-radius: 6px;
    background: #243149;
    text-align: right;
    color: transparent;
}

QProgressBar::chunk {
    border-radius: 6px;
    background: #5f88ff;
}

QPushButton#PrimaryButton {
    background: #3ecf8e;
    color: #071a13;
    border: 1px solid #5ce0a4;
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 800;
}

QPushButton#PrimaryButton:hover { background: #54d99b; }
QPushButton#PrimaryButton:disabled { background: #244638; color: #71867d; border-color: #315443; }

QPushButton#SecondaryButton {
    background: #162234;
    color: #d9e2ef;
    border: 1px solid #35455f;
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 700;
}

QPushButton#SecondaryButton:hover { background: #1c2b42; }
QPushButton#SecondaryButton:disabled { color: #607086; border-color: #263348; }

QPushButton#DangerButton {
    background: #321b24;
    color: #ff8d99;
    border: 1px solid #713442;
    border-radius: 10px;
    padding: 12px 16px;
    font-weight: 700;
}

QPushButton#DangerButton:hover { background: #45212c; }
QPushButton#DangerButton:disabled { color: #79515a; border-color: #432934; }

QTableWidget {
    background: transparent;
    alternate-background-color: #101928;
    border: 0;
    gridline-color: #223047;
    color: #cbd6e6;
    selection-background-color: #213657;
}

QHeaderView::section {
    background: #162132;
    color: #8695aa;
    border: 0;
    border-bottom: 1px solid #27364c;
    padding: 8px;
    font-weight: 700;
}

QTableWidget::item {
    padding: 7px;
    border-bottom: 1px solid #1d2a3d;
}

QCheckBox {
    color: #d6e0ee;
    spacing: 9px;
}

QCheckBox::indicator {
    width: 32px;
    height: 17px;
}

QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #31415a;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
"""
