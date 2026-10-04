from __future__ import annotations

from pathlib import Path

import torch
from torch.utils.data import Dataset


class ActivitySequenceDataset(Dataset):
    def __init__(self, split_dir: Path) -> None:
        self.files = sorted(split_dir.glob("*.pt"))
        if not self.files:
            raise FileNotFoundError(
                f"학습 샘플이 없습니다: {split_dir}\n"
                "먼저 prepare_dataset.py를 실행하거나 data/raw에 영상을 넣어주세요."
            )

    def __len__(self) -> int:
        return len(self.files)

    def __getitem__(self, index: int) -> tuple[torch.Tensor, str]:
        sample = torch.load(self.files[index], map_location="cpu")
        return sample["sequence"].float(), str(sample["label"])
