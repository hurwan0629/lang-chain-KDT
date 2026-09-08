from model import SimpleCNN
from torch.utils.data import DataLoader
from torch.nn import Module
from env import DEVICE, WEIGHT_DECAY, LEARNING_RATE
import torch


model = SimpleCNN().to(DEVICE)

# 여러개의 클래스가 나오기 떄문에 CrossEntropyLoss로 설정
criterion = torch.nn.CrossEntropyLoss()

optimizer = torch.optim.SGD(
    params=model.parameters(),
    lr=0.01,
    momentum=0.9
)

# torch.optim.AdamW(
#     params=model.parameters(),
#     lr=LEARNING_RATE,
#     weight_decay=WEIGHT_DECAY,
#     betas=(0.9, 0.999), # \beta_1, \beta_2
# )

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer=optimizer,
    mode="min",
    patience=10,
    factor=0.1
)

scaler = torch.amp.GradScaler("cuda")

def train_one_epochs(
       model: Module,
       data_loader: DataLoader,
       criterion,
       device,
       optimizer=None,
       scaler=None
):
    # 학습중 상태 확인
    is_training = False if optimizer is None else True
    # 학습 여부에 따라 모델 상태 정의
    model.train() if is_training else model.eval()
    # 학습 상태에 따른 컨택스트 저장
    context = torch.enable_grad() if is_training else torch.inference_mode()

    # 반환을 위한 상태 저장
    total_loss = 0.0
    total_correct = 0
    total_samples = 0

    with context:
        for images, labels in data_loader:
            # 디바이스 맞춰주기
            images = images.to(device)
            labels = labels.to(device)

            # torch.amp.autocast를 쓰면 train이든 eval이든
            # autocast 컨텍스트로 들어가게 됨.
            # 여기에서 모든 연산을 바꾸는 것은 아니고, 정밀도를 조금 포기하고
            # 연산 속도를 빠르게 하는 이유이며
            # 여기에서 torch.amp.autocast를 사용하는 이유는
            # 대부분의 conv, linear 연산은 모두 여기에서 발생하기 때문임
            with torch.amp.autocast(
                device_type="cuda",
                dtype=torch.float16
            ):
                # 모델 예측하기
                logits = model(images)
                # 손실함수 값 받아주기
                # CrossEntropyLoss는 내부적으로 softmax를 걸어주며
                # 함께 loss 를 구해주는 방식을 이용해서 softmax는 생략
                # criterion을 autocast에 넣어도 수치적으로 민감한 loss, CrossEntropyLoss
                # 같은 연산은 CUDA autocast에서 보통 FP32 쪽으로 처리됩니다.
                loss = criterion(logits, labels)

            # 학습중이라면 학습 시켜주기
            if is_training:
                # backward하면 기존의 Parameter의 grad에 누적합 시켜주는 방식이기
                # 떄문에 이를 이미 초기화시켜주기
                optimizer.zero_grad()
                if scaler is not None:
                    # 손실함수를 이용하여 모든 leaf parameter에 가중치 누적해주기
                    scaler(loss).backward()
                    # 옵티마이저 스템 밟아주기
                    scaler.step(optimizer)
                    # 스케일러가 가해주는 값을 업데이트 시켜주기
                    scaler.update()
                else:
                    loss.backward()
                    # 더해주기
                    optimizer.step()

            # 이후에 결과를 봐주기
            total_samples += len(images)
            total_correct += (logits.argmax(dim=1) == labels).sum()
            total_loss += loss.item() * len(images)

    # 결과 반환해주기
    return total_correct/total_samples, total_loss/total_samples




if __name__ == "__main__":
    print(DEVICE)