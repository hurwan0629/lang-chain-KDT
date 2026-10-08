from __future__ import annotations

from datetime import datetime
from pathlib import Path

import torch

from gru_activity_tracker.activity_store import ActivityStore
from gru_activity_tracker.clip_encoder import ClipEncoder
from gru_activity_tracker.model import ActivityGRU
from gru_activity_tracker.runtime.paths import (
    bundled_checkpoint_path,
    bundled_clip_dir,
    default_log_path,
)
from gru_activity_tracker.screen_capture import capture_full_screen


class ActivityPredictor:
    """Stateful CLIP + GRU inference engine used by both CLI and GUI runtimes."""

    def __init__(
        self,
        checkpoint_path: Path | None = None,
        clip_model_dir: Path | None = None,
        output_path: Path | None = None,
        device: str | None = None,
    ) -> None:
        self.checkpoint_path = checkpoint_path or bundled_checkpoint_path()
        self.clip_model_dir = clip_model_dir or bundled_clip_dir()
        self.output_path = output_path or default_log_path()

        self._require_path(self.checkpoint_path, "GRU checkpoint")
        self._require_path(self.clip_model_dir, "CLIP model")

        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )
        checkpoint = torch.load(self.checkpoint_path, map_location=self.device)

        self.labels: list[str] = list(checkpoint["labels"])
        self.prompts: dict[str, str] = dict(checkpoint["prompts"])
        self.temperature = float(checkpoint["temperature"])

        self.encoder = ClipEncoder(
            model_name=str(self.clip_model_dir),
            device=str(self.device),
        )
        self.text_embeddings = self.encoder.encode_texts(
            [self.prompts[label] for label in self.labels]
        ).to(self.device)

        self.model = ActivityGRU(
            input_dim=int(checkpoint["input_dim"]),
            hidden_dim=int(checkpoint["hidden_dim"]),
            output_dim=int(checkpoint["output_dim"]),
        ).to(self.device)
        self.model.load_state_dict(checkpoint["model_state"])
        self.model.eval()

        self.store = ActivityStore(self.output_path)
        self.hidden: torch.Tensor | None = None

    @staticmethod
    def _require_path(path: Path, description: str) -> None:
        if not path.exists():
            raise FileNotFoundError(
                f"{description}을(를) 찾을 수 없습니다: {path}\n"
                "build_release.bat으로 배포본을 다시 생성해 주세요."
            )

    def predict_screen(self) -> tuple[str, float, datetime]:
        frame = capture_full_screen()
        frame_embedding = self.encoder.encode_images([frame])[0].to(self.device)

        with torch.inference_mode():
            representation, self.hidden = self.model.step(
                frame_embedding,
                self.hidden,
            )
            logits = representation @ self.text_embeddings.T / self.temperature
            probabilities = logits.softmax(dim=-1)[0]
            best_index = int(probabilities.argmax().item())

        label = self.labels[best_index]
        score = float(probabilities[best_index].item())
        now = datetime.now()
        self.store.update(label, score, now)
        return label, score, now

    def reset_context(self) -> None:
        self.hidden = None

    def close(self) -> None:
        self.store.close()
