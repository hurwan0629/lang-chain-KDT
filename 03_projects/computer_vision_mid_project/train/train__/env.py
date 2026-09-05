from pathlib import Path
import random

import numpy as np
import torch


# -----------------------------
# Path
# -----------------------------
TRAIN_PACKAGE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TRAIN_PACKAGE_DIR.parent

DATASET_DIR = PROJECT_DIR / "dataset"
TRAIN_DATA_DIR = DATASET_DIR / "train"
TEST_DATA_DIR = DATASET_DIR / "test"

MODEL_DIR = PROJECT_DIR / "models"
MODEL_DIR.mkdir(parents=True, exist_ok=True)

CHECKPOINT_FILE = MODEL_DIR / "face_densenet121_best.pth"


# -----------------------------
# Runtime
# -----------------------------
SEED = 42

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

IMAGE_SIZE = 224
BATCH_SIZE = 32
NUM_WORKERS = 0

VAL_SIZE = 0.2

EPOCHS = 30
LEARNING_RATE = 1e-3
WEIGHT_DECAY = 1e-4

EARLY_STOPPING_PATIENCE = 7

# CUDA일 때만 AMP 사용
USE_AMP = DEVICE.type == "cuda"

# checkpoint가 있고 현재 클래스 구성이 같으면 이어서 학습
RESUME_TRAINING = True


# DenseNet121 ImageNet pretrained normalization
IMAGENET_MEAN = [0.485, 0.456, 0.406]
IMAGENET_STD = [0.229, 0.224, 0.225]


def seed_everything(seed: int = SEED) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


seed_everything()
