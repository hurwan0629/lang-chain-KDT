from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import torch
from PIL import Image
from transformers import XCLIPModel, XCLIPProcessor


MODEL_NAME = "microsoft/xclip-base-patch32"

DEFAULT_LABELS = [
    "a computer screen showing a video game being played",
    "a computer screen showing an entertaining video being watched",
    "a computer screen showing an educational video being watched",
    "a computer screen showing Python code being written",
    "a computer screen showing Java code being written",
    "a computer screen showing emails being read",
    "a computer screen showing a document being written",
    "a computer screen showing a book or ebook being read",
]


@dataclass(frozen=True)
class Prediction:
    label: str
    score: float
    scores: dict[str, float]


class ActivityModel:
    """최근 화면 sequence와 text label을 X-CLIP으로 비교한다."""

    def __init__(
        self,
        labels: list[str] | None = None,
        model_name: str = MODEL_NAME,
        device: str | None = None,
    ) -> None:
        self.labels = labels or DEFAULT_LABELS
        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )

        self.processor = XCLIPProcessor.from_pretrained(model_name)
        self.model = XCLIPModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

    def predict(self, frames: list[Image.Image]) -> Prediction:
        if not frames:
            raise ValueError("frames가 비어 있습니다.")

        video = [
            np.asarray(frame.convert("RGB"))
            for frame in frames
        ]

        inputs = self.processor(
            text=self.labels,
            videos=video,
            return_tensors="pt",
            padding=True,
        )

        inputs = {
            key: value.to(self.device)
            if isinstance(value, torch.Tensor)
            else value
            for key, value in inputs.items()
        }

        with torch.inference_mode():
            outputs = self.model(**inputs)

        logits = outputs.logits_per_video[0]
        probabilities = logits.softmax(dim=-1)

        best_index = probabilities.argmax().item()

        scores = {
            label: float(score)
            for label, score in zip(
                self.labels,
                probabilities.detach().cpu().tolist(),
            )
        }

        return Prediction(
            label=self.labels[best_index],
            score=float(probabilities[best_index].item()),
            scores=scores,
        )
