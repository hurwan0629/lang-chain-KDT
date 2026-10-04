from __future__ import annotations

import torch
from torch import nn
import torch.nn.functional as F


class ActivityGRU(nn.Module):
    """CLIP frame embeddings -> recurrent activity representation."""

    def __init__(
        self,
        input_dim: int = 512,
        hidden_dim: int = 256,
        output_dim: int = 512,
        num_layers: int = 1,
    ) -> None:
        super().__init__()
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.num_layers = num_layers

        self.gru = nn.GRU(
            input_size=input_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
        )
        self.projection = nn.Linear(hidden_dim, output_dim)

    def forward(self, sequence: torch.Tensor) -> torch.Tensor:
        output, _ = self.gru(sequence)
        representation = self.projection(output[:, -1])
        return F.normalize(representation, dim=-1)

    def step(
        self,
        frame_embedding: torch.Tensor,
        hidden: torch.Tensor | None = None,
    ) -> tuple[torch.Tensor, torch.Tensor]:
        if frame_embedding.ndim == 1:
            frame_embedding = frame_embedding.unsqueeze(0)

        output, hidden = self.gru(
            frame_embedding.unsqueeze(1),
            hidden,
        )
        representation = self.projection(output[:, -1])
        return F.normalize(representation, dim=-1), hidden
