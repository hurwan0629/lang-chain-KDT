from PIL import Image, ImageGrab


def capture_full_screen() -> Image.Image:
    """Capture the full desktop as an RGB PIL image."""
    return ImageGrab.grab().convert("RGB")
