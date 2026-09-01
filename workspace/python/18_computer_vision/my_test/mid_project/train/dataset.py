from pathlib import Path

import numpy as np
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Subset
from torchvision.datasets import ImageFolder

try:
    from .env import (
        TRAIN_DATA_DIR,
        TEST_DATA_DIR,
        BATCH_SIZE,
        NUM_WORKERS,
        VAL_SIZE,
        SEED,
        DEVICE,
    )
    from .transforms import train_transform, test_transform
except ImportError:
    from env import (
        TRAIN_DATA_DIR,
        TEST_DATA_DIR,
        BATCH_SIZE,
        NUM_WORKERS,
        VAL_SIZE,
        SEED,
        DEVICE,
    )
    from transforms import train_transform, test_transform


def _check_dataset_dir(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"데이터 폴더가 없습니다: {path}\n"
            "예: dataset/train/person_a/*.jpg"
        )


def create_train_val_loaders():
    """
    같은 train 폴더를 2개의 ImageFolder로 읽는다.

    이유:
    - train subset  -> train_transform
    - validation    -> test_transform

    두 ImageFolder의 samples 순서는 같은 root를 사용하므로 동일하다.
    """
    _check_dataset_dir(TRAIN_DATA_DIR)

    train_source = ImageFolder(
        root=TRAIN_DATA_DIR,
        transform=train_transform,
    )

    val_source = ImageFolder(
        root=TRAIN_DATA_DIR,
        transform=test_transform,
    )

    indices = np.arange(len(train_source))

    train_idx, val_idx = train_test_split(
        indices,
        test_size=VAL_SIZE,
        random_state=SEED,
        shuffle=True,
        stratify=train_source.targets,
    )

    train_dataset = Subset(train_source, train_idx)
    val_dataset = Subset(val_source, val_idx)

    pin_memory = DEVICE.type == "cuda"

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=pin_memory,
        drop_last=False,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=pin_memory,
        drop_last=False,
    )

    return train_loader, val_loader, train_source.classes, train_source.class_to_idx


def create_test_loader():
    _check_dataset_dir(TEST_DATA_DIR)

    test_dataset = ImageFolder(
        root=TEST_DATA_DIR,
        transform=test_transform,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=(DEVICE.type == "cuda"),
        drop_last=False,
    )

    return test_loader, test_dataset.classes, test_dataset.class_to_idx


if __name__ == "__main__":
    train_loader, val_loader, classes, class_to_idx = create_train_val_loaders()

    print("classes:", classes)
    print("class_to_idx:", class_to_idx)
    print("train samples:", len(train_loader.dataset))
    print("validation samples:", len(val_loader.dataset))

    images, labels = next(iter(train_loader))

    print("images.shape:", images.shape)  # [B, 3, 224, 224]
    print("labels.shape:", labels.shape)  # [B]
