from torchvision.datasets import ImageFolder
from pathlib import Path
from torch.utils.data import Subset, DataLoader

from .env import IS_CUDA, NUM_WORKERS, IMAGE_PATH
from .transforms import train_transform, test_transform
from sklearn.model_selection import train_test_split
import numpy as np

TRAIN_DATADIR = IMAGE_PATH / "train"
TEST_DATADIR = IMAGE_PATH / "test"

# # # # # # # # # # # # # # # # # # # # # # # # # # # #
#              ImageFolder -> DataLoader              #
# # # # # # # # # # # # # # # # # # # # # # # # # # # #

full_train_dataset = ImageFolder(
    root=TRAIN_DATADIR,
    transform=train_transform
)

full_val_dataset = ImageFolder(
    root=TRAIN_DATADIR,
    transform=test_transform
)

test_dataset = ImageFolder(
    root=TEST_DATADIR,
    transform=test_transform
)

train_indices = np.arange(len(full_train_dataset))

train_idx, val_idx = train_test_split(
    train_indices,
    test_size=0.2,
    random_state=42,
    stratify=full_train_dataset.targets
)

train_dataset = Subset(full_train_dataset, train_idx)
val_dataset = Subset(full_val_dataset, val_idx)

train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=32,
    shuffle=True,
    drop_last=False,
    pin_memory=IS_CUDA,
    num_workers=NUM_WORKERS,
    persistent_workers=(NUM_WORKERS > 0)
)

val_loader = DataLoader(
    dataset=val_dataset,
    batch_size=32,
    shuffle=False,
    drop_last=False,
    pin_memory=IS_CUDA,
    num_workers=NUM_WORKERS,
    persistent_workers=(NUM_WORKERS > 0)
)

test_loader = DataLoader(
    dataset=test_dataset,
    batch_size=32,
    shuffle=False,
    drop_last=False,
    pin_memory=IS_CUDA,
    num_workers=NUM_WORKERS,
    persistent_workers=(NUM_WORKERS > 0)
)