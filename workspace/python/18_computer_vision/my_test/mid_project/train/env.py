import torch
import numpy as np
import random

from pathlib import Path

IS_CUDA=torch.cuda.is_available()

NUM_WORKERS=0

SEED=42

torch.random.seed(SEED)
np.random.seed(SEED)
random.seed(SEED)

IMAGE_PATH=Path() / ".." / "datasets"

CHECKPOINT_FILE= Path() / "checkpoint.pth"