from __future__ import annotations

import torch
import torch.nn.functional as F
from PIL import Image
from transformers import CLIPModel, CLIPProcessor

from .config import CLIP_MODEL_NAME


class ClipEncoder:
    """Frozen CLIP encoder for screen frames and label text."""

    def __init__(
        self,
        model_name: str = CLIP_MODEL_NAME,
        device: str | None = None,
    ) -> None:
        self.device = torch.device(
            device or ("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.processor = CLIPProcessor.from_pretrained(model_name)
        self.model = CLIPModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.model.eval()

        for parameter in self.model.parameters():
            parameter.requires_grad_(False)

        self.embedding_dim = int(self.model.config.projection_dim)

    @torch.inference_mode()
    def encode_images(self, images: list[Image.Image]) -> torch.Tensor:
        if not images:
            raise ValueError("images가 비어 있습니다.")

        inputs = self.processor(
            images=[image.convert("RGB") for image in images],
            return_tensors="pt",
        )
        pixel_values = inputs["pixel_values"].to(self.device)

        vision_output = self.model.vision_model(pixel_values=pixel_values)
        pooled = vision_output.pooler_output
        embeddings = self.model.visual_projection(pooled)
        return F.normalize(embeddings, dim=-1).cpu()

    @torch.inference_mode()
    def encode_texts(self, texts: list[str]) -> torch.Tensor:
        if not texts:
            raise ValueError("texts가 비어 있습니다.")

        inputs = self.processor(
            text=texts,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        input_ids = inputs["input_ids"].to(self.device)
        attention_mask = inputs.get("attention_mask")
        if attention_mask is not None:
            attention_mask = attention_mask.to(self.device)

        text_output = self.model.text_model(
            input_ids=input_ids,
            attention_mask=attention_mask,
        )
        pooled = text_output.pooler_output
        embeddings = self.model.text_projection(pooled)
        return F.normalize(embeddings, dim=-1).cpu()
