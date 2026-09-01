from torchvision.datasets import ImageFolder
from pathlib import Path

IMG_DIR = Path() / ".." / "dataset"

TRAIN_DATADIR = IMG_DIR / "train"
TEST_DATADIR = IMG_DIR / "test"

train_dataset = ImageFolder(
    root=TRAIN_DATADIR,
    transform=train_transform
)

test_dataset = ImageFolder(
    root=TEST_DATADIR,
    transform=test_transform
)

