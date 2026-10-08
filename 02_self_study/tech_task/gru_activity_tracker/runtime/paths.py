from __future__ import annotations

import os
from pathlib import Path
import sys


def bundle_root() -> Path:
    """Return the read-only root that contains files bundled by PyInstaller."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[1]


def bundled_assets_dir() -> Path:
    return bundle_root() / "bundle_assets"


def bundled_checkpoint_path() -> Path:
    return bundled_assets_dir() / "activity_gru.pt"


def bundled_clip_dir() -> Path:
    return bundled_assets_dir() / "clip"


def user_data_dir() -> Path:
    """Writable per-user directory. Never write logs into the EXE bundle."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    base = Path(local_app_data) if local_app_data else Path.home() / "AppData" / "Local"
    path = base / "GRUActivityTracker"
    path.mkdir(parents=True, exist_ok=True)
    return path


def default_log_path() -> Path:
    return user_data_dir() / "gru_activity_log.csv"
