from contextlib import nullcontext

import torch
from torch import nn
from torch import optim

try:
    from .dataset import create_train_val_loaders
    from .env import (
        CHECKPOINT_FILE,
        DEVICE,
        EPOCHS,
        LEARNING_RATE,
        WEIGHT_DECAY,
        EARLY_STOPPING_PATIENCE,
        USE_AMP,
        RESUME_TRAINING,
    )
    from .model import create_model, count_parameters
except ImportError:
    from dataset import create_train_val_loaders
    from env import (
        CHECKPOINT_FILE,
        DEVICE,
        EPOCHS,
        LEARNING_RATE,
        WEIGHT_DECAY,
        EARLY_STOPPING_PATIENCE,
        USE_AMP,
        RESUME_TRAINING,
    )
    from model import create_model, count_parameters


def train_one_epoch(
    model,
    loader,
    criterion,
    optimizer,
    scaler,
    device,
):
    model.train()

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    amp_enabled = USE_AMP and device.type == "cuda"

    for images, labels in loader:
        images = images.to(
            device,
            non_blocking=True,
        )
        labels = labels.to(
            device,
            non_blocking=True,
        )

        optimizer.zero_grad(set_to_none=True)

        with torch.autocast(
            device_type=device.type,
            dtype=torch.float16,
            enabled=amp_enabled,
        ):
            logits = model(images)
            loss = criterion(logits, labels)

        if amp_enabled:
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()

        batch_size = labels.size(0)

        total_loss += loss.item() * batch_size
        total_correct += (
            logits.argmax(dim=1) == labels
        ).sum().item()
        total_samples += batch_size

    return {
        "loss": total_loss / total_samples,
        "accuracy": total_correct / total_samples,
    }


@torch.inference_mode()
def validate_one_epoch(
    model,
    loader,
    criterion,
    device,
):
    model.eval()

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    amp_enabled = USE_AMP and device.type == "cuda"

    for images, labels in loader:
        images = images.to(
            device,
            non_blocking=True,
        )
        labels = labels.to(
            device,
            non_blocking=True,
        )

        with torch.autocast(
            device_type=device.type,
            dtype=torch.float16,
            enabled=amp_enabled,
        ):
            logits = model(images)
            loss = criterion(logits, labels)

        batch_size = labels.size(0)

        total_loss += loss.item() * batch_size
        total_correct += (
            logits.argmax(dim=1) == labels
        ).sum().item()
        total_samples += batch_size

    return {
        "loss": total_loss / total_samples,
        "accuracy": total_correct / total_samples,
    }


def save_checkpoint(
    model,
    optimizer,
    scheduler,
    epoch,
    best_val_loss,
    class_to_idx,
):
    checkpoint = {
        "model_name": "densenet121",
        "epoch": epoch,
        "num_classes": len(class_to_idx),
        "class_to_idx": class_to_idx,
        "best_val_loss": best_val_loss,

        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "scheduler_state_dict": scheduler.state_dict(),
    }

    torch.save(
        checkpoint,
        CHECKPOINT_FILE,
    )


def try_resume(
    model,
    optimizer,
    scheduler,
    current_class_to_idx,
):
    """
    기존 checkpoint의 클래스 구성이 현재 데이터셋과 동일할 때만 이어서 학습.
    맞지 않거나 load에 실패하면 ImageNet pretrained 상태부터 새로 시작.
    """
    if not RESUME_TRAINING:
        return 0, float("inf")

    if not CHECKPOINT_FILE.exists():
        return 0, float("inf")

    print(f"[checkpoint] 발견: {CHECKPOINT_FILE}")

    try:
        checkpoint = torch.load(
            CHECKPOINT_FILE,
            map_location=DEVICE,
        )

        if checkpoint.get("class_to_idx") != current_class_to_idx:
            print(
                "[checkpoint] 현재 class_to_idx와 달라서 "
                "checkpoint를 사용하지 않습니다."
            )
            return 0, float("inf")

        model.load_state_dict(
            checkpoint["model_state_dict"]
        )

        if "optimizer_state_dict" in checkpoint:
            optimizer.load_state_dict(
                checkpoint["optimizer_state_dict"]
            )

        if "scheduler_state_dict" in checkpoint:
            scheduler.load_state_dict(
                checkpoint["scheduler_state_dict"]
            )

        start_epoch = checkpoint.get("epoch", -1) + 1
        best_val_loss = checkpoint.get(
            "best_val_loss",
            float("inf"),
        )

        print(
            f"[checkpoint] epoch {start_epoch}부터 이어서 학습합니다."
        )

        return start_epoch, best_val_loss

    except Exception as error:
        print(
            "[checkpoint] load 실패. "
            "ImageNet pretrained 상태에서 다시 시작합니다."
        )
        print("reason:", error)

        return 0, float("inf")


def main():
    train_loader, val_loader, classes, class_to_idx = (
        create_train_val_loaders()
    )

    print("DEVICE:", DEVICE)
    print("classes:", classes)
    print("class_to_idx:", class_to_idx)

    model = create_model(
        num_classes=len(classes),
        freeze_features=True,
    ).to(DEVICE)

    total, trainable = count_parameters(model)

    print(f"전체 parameter: {total:,}")
    print(f"학습 parameter: {trainable:,}")

    criterion = nn.CrossEntropyLoss()

    optimizer = optim.AdamW(
        filter(
            lambda p: p.requires_grad,
            model.parameters(),
        ),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
    )

    scheduler = optim.lr_scheduler.ReduceLROnPlateau(
        optimizer,
        mode="min",
        factor=0.5,
        patience=2,
    )

    amp_enabled = USE_AMP and DEVICE.type == "cuda"

    # torch.amp.GradScaler의 device 인자는 버전에 따라 다를 수 있어
    # 현재 PyTorch에서 가장 널리 호환되는 CUDA scaler를 사용.
    scaler = torch.amp.GradScaler(
        "cuda",
        enabled=amp_enabled,
    )

    start_epoch, best_val_loss = try_resume(
        model,
        optimizer,
        scheduler,
        class_to_idx,
    )

    epochs_without_improvement = 0

    for epoch in range(start_epoch, EPOCHS):
        train_result = train_one_epoch(
            model=model,
            loader=train_loader,
            criterion=criterion,
            optimizer=optimizer,
            scaler=scaler,
            device=DEVICE,
        )

        val_result = validate_one_epoch(
            model=model,
            loader=val_loader,
            criterion=criterion,
            device=DEVICE,
        )

        scheduler.step(
            val_result["loss"]
        )

        current_lr = optimizer.param_groups[0]["lr"]

        print(
            f"[{epoch + 1:03d}/{EPOCHS:03d}] "
            f"train loss={train_result['loss']:.4f} "
            f"acc={train_result['accuracy']:.4f} | "
            f"val loss={val_result['loss']:.4f} "
            f"acc={val_result['accuracy']:.4f} | "
            f"lr={current_lr:.2e}"
        )

        if val_result["loss"] < best_val_loss:
            best_val_loss = val_result["loss"]
            epochs_without_improvement = 0

            save_checkpoint(
                model=model,
                optimizer=optimizer,
                scheduler=scheduler,
                epoch=epoch,
                best_val_loss=best_val_loss,
                class_to_idx=class_to_idx,
            )

            print(
                f"  -> best checkpoint 저장: {CHECKPOINT_FILE}"
            )

        else:
            epochs_without_improvement += 1

            if (
                epochs_without_improvement
                >= EARLY_STOPPING_PATIENCE
            ):
                print("Early stopping")
                break

    print("학습 종료")
    print("best checkpoint:", CHECKPOINT_FILE)


if __name__ == "__main__":
    main()
