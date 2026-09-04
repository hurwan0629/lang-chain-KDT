from contextlib import nullcontext

import torch
from torch import nn
from torch import optim

try:
    # 데이터셋에서 훈련용 데이터 로더를 불러오기
    from .dataset import create_train_val_loaders
    # env 파일에서 설정해놓은 형태의 환경변수들을 가져오기
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
    # 런타임에 모델 객체를 하나 만들기 위한 create_model 함수와
    # (total, trainable) 를 반환하는 count_parameters 함수를 가져오기 (model.py 에서)
    from .model import create_model, count_parameters
except ImportError:
    # 상대경로에서 에러가 날 일은 없겠지만 난다면 파이썬 인터프리터 실행 위치를 기준으로 불러오기
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
    """
    모델, 데이터 로더, 손실함수, 옵티마이저, 스케일러, 디바이스 여부를 인자로 받아서
    모델에 존재하는 파라미터를 1_epoch를 돌면서 업데이트해준 뒤,
    다음 값을 반환

    `{ "loss": float, "accuracy": float }`
    """
    model.train()

    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    # USE_AMP 플래그가 켜져있고
    # 디바이스가 cuda로 AMP를 사용할 수 있는 경우에 amp_enabled 플래그를 켜주기
    amp_enabled = USE_AMP and device.type == "cuda"

    # 로더에서 이미지 데이터 (현재 기준 224x224)와 정답 (ImageFolder의 폴더 인식) 라벨을 가져와줌
    # 이미지 데이터의 형태는 (B, 3, 224, 224)이며 labels의 경우에는 (B) 로 되어있음
    for images, labels in loader:
        # 텐서 배치를 비동기로 처리하되 device.type=="cpu" 이면 동작하지 않음
        # 하지만 True여서 문제가 생기는 것은 아니기 때문에 그대로 채택
        images = images.to(
            device,
            non_blocking=True,
        )
        labels = labels.to(
            device,
            non_blocking=True,
        )

        # 기존 optimizer의 대상이 되어있는 Parameter.grad = None로 변경하기
        optimizer.zero_grad(set_to_none=True)

        # PyTorch에서 연산별로 미리 정해진 autocast 정책에 따라 실행하는 방식
        # 예를 들어 Conv, Linear, 행렬곱 등은 모두 곱셈/덧셈이 정말 많지만
        # FP16/BF16을 사용해도 어느정도 성능이 잘 유지되기 때문에 해당 방식을 사용
        with torch.autocast(
            device_type=device.type,    # 어디서 연산할지에 맞춰 autocast 규칙을 적용
            dtype=torch.float16,        # 낮은 정밀도로 바꿀 연산에서 사용할 타입 설정해주기
            enabled=amp_enabled,        #
        ):
            logits = model(images)              # 모델에 이미지 넣고 logits 뽑아주기
            loss = criterion(logits, labels)    # loss 함수 (보통 CELoss)

        if amp_enabled:
            # amp에 의해 gradient가 너무 작아져서 특정 소숫점 이하로 0이 사라지는
            # 문제를 막기 위해 scaler을 통해서 조금씩 크기를 키워주거나 하기
            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            optimizer.step()

        # 배치 사이즈는 라벨의 (B) 에서 뽑아서 계산 및 누적해주기
        batch_size = labels.size(0)

        total_loss += loss.item() * batch_size
        # logits는 (B, (num_classes))로 나오기 때문에 이를 모두 합쳐서 사용하기
        total_correct += (
            logits.argmax(dim=1) == labels
        ).sum().item()
        # batch_size 추가해보기
        total_samples += batch_size

    # 손실값과 정확도를 반환해주기
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
    """
    pytorch에서 제공해주는 inference_mode() 데코레이터를 이용한 함수

    model, loader, criterion, device 를 인자로 받아서
    모델을 inference_mode + eval 형태로 DAG 및 특정 레이어들의 train 시의 다른 동작을
    eval의 형태로 변경해주어 동작을 합니다.

    해당 함수의 내부 동작은 train_one_epoch와 거의 동일합니다.
    """
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
    """
    env.py의 CHECKPOINT_FILE경로에 다음과 같은 정보를 저장합니다.

    model_name: 모델 이름 (densenet121 로 고정)
    epoch: 에포크 횟수
    num_classes: 최종 출력 logits 개수
    class_to_idx: 클래스에 대한 logits[idx] 의 idx
    best_val_loss: 최고 검증 loss
    model_state_dict: 파라미터 정보들 모두 저장하기 (+Buffer)
    optimizer_state_dict: 옵티마이저 정보 저장
    scheduler_state_dict: 스케줄러 정보 저장
    """
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
    env.py 파일에 존재하는 CHECKPOINT_FILE에 존재하는 .pth를 이용하여
    학습 상태를 해당 시점으로 만들어주며 `current_class_to_idx`를
    기준으로 해당 파일과 동기화 할 수 있는지를 판단

    존재하지 않으면 epoch=0, best_val_loss=float('inf') 를 반환
    """
    if not RESUME_TRAINING:
        return 0, float("inf")

    if not CHECKPOINT_FILE.exists():
        return 0, float("inf")

    # checkpoint 파일이 존재하면 있다고 알려주기
    print(f"[checkpoint] 발견: {CHECKPOINT_FILE}")

    try:
        # 체크포인즈 파일을 불러오기
        # 체크포인트를 불러올 때 불러오는 기준은 체크포인트 파일을 저장할 시점에
        # 해당 파라미터들이 저장되어있던 디바이스 이기 때문에
        # map_location 인자를 이용하여 불러오는 위치를 정확하게 만들어주기.
        checkpoint = torch.load(
            CHECKPOINT_FILE,
            map_location=DEVICE,
        )

        # # # # # # # # # # # # # # # # # # # # # # # # # # #
        #            다음과 같은 요소 다시 적용해주기             #
        # # # # # # # # # # # # # # # # # # # # # # # # # # #
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
    # 로더 정보를 가져와서 준비하기
    # + 클래스 배열과 함께 class_to_idx 형태를 가져와주기
    train_loader, val_loader, classes, class_to_idx = (
        create_train_val_loaders()
    )

    print("DEVICE:", DEVICE)
    print("classes:", classes)
    print("class_to_idx:", class_to_idx)

    # model.py에 존재하는 create_model 함수를 이용하여 densenet121()에
    # weight를 넣어놓은 모델을 가져와주기
    # 여기에서 num_classes와 freeze_features를 설정하여 마지막 레이어만 수정해주기
    model = create_model(
        num_classes=len(classes),
        freeze_features=True,
    ).to(DEVICE) # + 디바이스를 env.py에 맞추어 넣어주기

    total, trainable = count_parameters(model)

    print(f"전체 parameter: {total:,}")
    print(f"학습 parameter: {trainable:,}")

    criterion = nn.CrossEntropyLoss()

    # 기본 모델로 AdamW를 선택해보기
    optimizer = optim.AdamW(
        filter(
            lambda p: p.requires_grad,
            model.parameters(),
        ),
        lr=LEARNING_RATE,
        weight_decay=WEIGHT_DECAY,
    )

    # 스케줄러 ReduceLROnPlateau 선택해보기
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

    # epoch와 best_val_loss 상태를 받아와주기
    # 각각의 객체에 파라미터/buffer 값을 주입해주기
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
