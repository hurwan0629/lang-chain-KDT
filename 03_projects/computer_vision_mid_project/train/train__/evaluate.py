import torch
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
)

try:
    from .dataset import create_test_loader
    from .env import CHECKPOINT_FILE, DEVICE
    from .model import create_model
except ImportError:
    from dataset import create_test_loader
    from env import CHECKPOINT_FILE, DEVICE
    from model import create_model


@torch.inference_mode()
def evaluate():
    if not CHECKPOINT_FILE.exists():
        raise FileNotFoundError(
            f"checkpoint가 없습니다: {CHECKPOINT_FILE}"
        )

    checkpoint = torch.load(
        CHECKPOINT_FILE,
        map_location=DEVICE,
    )

    class_to_idx = checkpoint["class_to_idx"]
    num_classes = checkpoint["num_classes"]

    idx_to_class = {
        idx: name
        for name, idx in class_to_idx.items()
    }

    test_loader, test_classes, test_class_to_idx = (
        create_test_loader()
    )

    if test_class_to_idx != class_to_idx:
        raise ValueError(
            "학습 checkpoint와 test 데이터의 class_to_idx가 다릅니다.\n"
            f"checkpoint: {class_to_idx}\n"
            f"test: {test_class_to_idx}"
        )

    model = create_model(
        num_classes=num_classes,
        freeze_features=True,
    ).to(DEVICE)

    model.load_state_dict(
        checkpoint["model_state_dict"]
    )

    model.eval()

    y_true = []
    y_pred = []

    total_correct = 0
    total_samples = 0

    for images, labels in test_loader:
        images = images.to(
            DEVICE,
            non_blocking=True,
        )
        labels = labels.to(
            DEVICE,
            non_blocking=True,
        )

        logits = model(images)
        predictions = logits.argmax(dim=1)

        total_correct += (
            predictions == labels
        ).sum().item()
        total_samples += labels.size(0)

        y_true.extend(
            labels.cpu().tolist()
        )
        y_pred.extend(
            predictions.cpu().tolist()
        )

    accuracy = total_correct / total_samples

    labels_order = list(range(num_classes))
    target_names = [
        idx_to_class[idx]
        for idx in labels_order
    ]

    print(f"test accuracy: {accuracy:.4f}")

    print("\nconfusion matrix")
    print(
        confusion_matrix(
            y_true,
            y_pred,
            labels=labels_order,
        )
    )

    print("\nclassification report")
    print(
        classification_report(
            y_true,
            y_pred,
            labels=labels_order,
            target_names=target_names,
            digits=4,
            zero_division=0,
        )
    )


if __name__ == "__main__":
    evaluate()
