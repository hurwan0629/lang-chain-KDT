from __future__ import annotations

from PIL import Image, ImageGrab


def capture_full_screen() -> Image.Image:
    """전체 화면을 캡처해서 RGB PIL Image로 반환한다."""
    return ImageGrab.grab().convert("RGB")
