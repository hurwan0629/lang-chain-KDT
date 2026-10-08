from __future__ import annotations

from pathlib import Path
import shutil

from transformers import CLIPModel, CLIPProcessor

from gru_activity_tracker.config import CLIP_MODEL_NAME


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SOURCE_CHECKPOINT = PACKAGE_DIR / "checkpoints" / "activity_gru.pt"
BUNDLE_ASSETS_DIR = PACKAGE_DIR / "bundle_assets"
BUNDLE_CHECKPOINT = BUNDLE_ASSETS_DIR / "activity_gru.pt"
BUNDLE_CLIP_DIR = BUNDLE_ASSETS_DIR / "clip"


def _copy_checkpoint() -> None:
    if not SOURCE_CHECKPOINT.exists():
        raise FileNotFoundError(
            "학습 checkpoint를 찾을 수 없습니다: "
            f"{SOURCE_CHECKPOINT}\n"
            "먼저 학습을 완료해 checkpoints/activity_gru.pt를 만들어 주세요."
        )

    BUNDLE_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    if (
        not BUNDLE_CHECKPOINT.exists()
        or SOURCE_CHECKPOINT.stat().st_size != BUNDLE_CHECKPOINT.stat().st_size
        or SOURCE_CHECKPOINT.stat().st_mtime > BUNDLE_CHECKPOINT.stat().st_mtime
    ):
        shutil.copy2(SOURCE_CHECKPOINT, BUNDLE_CHECKPOINT)
        print(f"[assets] checkpoint copied: {BUNDLE_CHECKPOINT}")
    else:
        print("[assets] checkpoint already up to date")


def _clip_assets_ready() -> bool:
    required = [
        BUNDLE_CLIP_DIR / "config.json",
        BUNDLE_CLIP_DIR / "preprocessor_config.json",
        BUNDLE_CLIP_DIR / "tokenizer_config.json",
        BUNDLE_CLIP_DIR / "vocab.json",
        BUNDLE_CLIP_DIR / "merges.txt",
    ]
    has_weights = any(
        (BUNDLE_CLIP_DIR / filename).exists()
        for filename in ("model.safetensors", "pytorch_model.bin")
    )
    return all(path.exists() for path in required) and has_weights


def _prepare_clip() -> None:
    if _clip_assets_ready():
        print("[assets] local CLIP model already prepared")
        return

    BUNDLE_CLIP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[assets] preparing CLIP model: {CLIP_MODEL_NAME}")
    print("[assets] first build may download the model from Hugging Face")

    processor = CLIPProcessor.from_pretrained(CLIP_MODEL_NAME)
    model = CLIPModel.from_pretrained(CLIP_MODEL_NAME)
    processor.save_pretrained(BUNDLE_CLIP_DIR)
    model.save_pretrained(BUNDLE_CLIP_DIR)
    print(f"[assets] CLIP saved locally: {BUNDLE_CLIP_DIR}")


def main() -> None:
    _copy_checkpoint()
    _prepare_clip()
    print("[assets] ready")


if __name__ == "__main__":
    main()
