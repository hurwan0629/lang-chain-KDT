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
    다음을 반환합니다:
    (train_loader, val_loader): (DataLoader, DataLoader)

    이유:
    - train subset  -> train_transform
    - validation    -> test_transform

    두 ImageFolder의 samples 순서는 같은 root를 사용하므로 동일하다.
    """
    # env.py에 설정되어있는 dir이 존재하는지 확인하기
    # 없으면 에러
    _check_dataset_dir(TRAIN_DATA_DIR)

    # TRAIN_DATA_DIR에서 2개의 소스를 가져오기
    # 같은 디렉토리에서 다른 방식의 transform을 이용하여
    # train의 경우에는증강
    # val의 경우에는 일반 Resize, ToTensor, Normalize 및 변환만 가능하게 설정
    train_source = ImageFolder(
        root=TRAIN_DATA_DIR,
        transform=train_transform,
    )
    val_source = ImageFolder(
        root=TRAIN_DATA_DIR,
        transform=test_transform,
    )

    # 인덱스를 뽑아서 데이터를 분할하기
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

    # 디바이스 설정에 따라 DataLoader의 사용 방식을 변경해주기
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


# DataLoader 만들어서 반환해주기
def create_test_loader():
    """(DataLoader, classes list, class_to_idx: dict) 반환"""
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


"""해당 스크립트를 그대로 실행하면 데이터셋의 종류를 먼저 확인시켜줌"""
if __name__ == "__main__":
    train_loader, val_loader, classes, class_to_idx = create_train_val_loaders()

    print("classes:", classes)
    print("class_to_idx:", class_to_idx)
    print("train samples:", len(train_loader.dataset))
    print("validation samples:", len(val_loader.dataset))

    images, labels = next(iter(train_loader))

    print("images.shape:", images.shape)  # [B, 3, 224, 224]
    print("labels.shape:", labels.shape)  # [B]
