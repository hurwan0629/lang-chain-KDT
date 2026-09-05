# [Pytorch] 파이토치 다시 부수기
> 이번에도 파이토치를 자유주제로 탐구합니다.

파이토치의 세계는 방대하면서도 이를 모르면 쉬운길도 어렵게 가는 방향으로 만들어질 수 있습니다.

이를 막기 위하여 다시 한번 크게 둘러보며 때로는 깊이 파고들기도 해보겠습니다.

## 파이토치를 크게 나눠보기
파이토치는 크게 다음과 같은 형태로 이루어져있습니다.
- 데이터: Dataset, TensorDataset, ImageFolder, Subset, DataLoader
- 데이터 변환: Compose, ToTensor, Normalize, Resize, augmentation
- 모델: Linear, Conv2d, ReLU, BatchNorm, Pooling, Dropout
- 학습: Loss, Autograd, Optimizer, Scheduler
- 평가/운영: eval, inference_mode, EarlyStopping, checkpoint 등

## 데이터
Dataset은 기본적으로 단순한 인터페이스를 가졌습니다.

이전에도 다뤄보았지만 크게 `len`, `getitem` 등의 매직메서드 정도로 이루어져있습니다.

이번에는 Dataset을 바라보는 시점은 여러 자식 클래스들입니다.

Dataset는 인터페이스에 가까운 클래스로 여러 클래스들이 이를 상속하여 구현하게 됩니다. 예시로는 다음과 같습니다.
- 사용자 커스텀
- TensorDataset (Tensor들을 묶음)
- ImageFolder: 폴더 구조를 이미지 Dataset으로 만듦. 이를 통해서 필요할 때마다 데이터를 가져오는 형식을 사용함
- FashionMNIST 등과 같은 VisionDataset: 기본적으로 tensorvision에서 제공하는 VisionDataset 계열의 데이터셋입니다. 다른 예시로는 EuroSAT, CIFAR10 등이 있습니다.
- Subset: 원본 Dataset를 가리키는 서브셋 데이터

> 이는 모두 `dataset[i]` 를 가능하게 해주는 객체입니다.

이후 나오는 클래스가 바로 DataLoader입니다.

Dataset가 map-style dataset에 해당한다면 DataLoader은 데이터 관련 클래스들을 하나로 묶어서 iterable 하게 제공해주는 클래스입니다.

이때 torch.transforms.Transform도 Dataset의 흐름 안에 존재하게 됩니다.

일반적으로 transforms.Compose를 통해 묶어주는 transform 클래스들은 사용자(개발자)가 직접 사용하는 경우는 상대적으로 적습니다.

보통은 다음과 같은 형식을 사용합니다.

```python
transform = transforms.Compose([
  transforms.Resize((128, 128)),
  transforms.RandomHorizontalFlip(),
  transforms.ToTensor(),
  transforms.Normalize(mean=(...,), std=(...,)),
  ...
])
```

이렇게 만들어진 transform.Compose 객체는 파이썬에서 제공하는 `PIL.Image` 라는 파이썬 기본 제공 타입을 가공하여 텐서로 변환해주게 됩니다.

여기에서 Compose의 흐름을 크게 2가지로 나눌 수 있습니다.
- preprocessing: 전처리로 데이터를 모델에 적합한 형태로 만드는 것을 말합니다.
  - Resize
  - ToTensor
  - Normalize
- augmentation: 같은 데이터를 조금씩 변형하여 새로운 학습 사례처럼 만드는 것을 말합니다. (증강)
  - RandomHorizontalFlip
  - RandomRotation
  - RandomCrop
  - RandomInvert

## 신경망의 수학
신경망의 수학의 경우에는 이전까지 공부한 내용이 있어서 설명을 하면 이제 어느정도 속도감 있게 학습이 될 수 있습니다.

현재 병목 지점은 신경망의 그래프 형태의 노드들의 그림이 너무 강하게 머리에 박혀있고 상대적으로 수학적으로 생각하는 것이 자연스럽게 이루어지지 않는다는 점입니다.

한번 더 복기해보면
1. Tensor을 선형/아핀 변환
2. 비선형 변환
3. 위 작업을 n번 반복
4. 위 작업동안 연산 그래프가 생성 (값과 연산 클래스) (각각의 노드는 자신의 이전 노드를 가리키며 의존성 그래프를 그리게됨)
5. 최종적으로는 몇번의 정리 후, Loss 함수를 통과하여 값을 만들게 됨
6. Loss를 사용자에게 출력하거나 사용을 한 뒤 해당 loss_fn 까지 적용한 수식을 저장하는 loss 객체에 `.backward()`를 실행함
7. 현재까지 존재했던 모든 수식에 대해서 `requires_grad=True`인 `leaf node`까지의 경로대로 역전파하여 미분을 통해 `grad += new_grad` 를 하게 됩니다. 그중 거슬러 올라가는 과정에서 다른 Tensor에 대해서는 `.grad` 값을 누적하지 않습니다.

또한 CNN의 Conv2d 의 경우에도 학습 가능한 선형 변환으로 행렬곱보다 개념적으로 단순하게 동일한 인덱스 위치의 값들끼리 더한 값을 합하여 결과를 내는 방식으로 대상 텐서보다 높이와 너비가 `-1`씩 된 행렬 x 채널 x batch 를 반환하게 됩니다.

Conv에도 동일하게 weight(kernel, filter)과 bias가 존재합니다. (하나의 출력 채널을 만드는 kernel 묶음을 filter이라고 부릅니다.)

예를 들어 weight = (16, 4, 3, 3)이라고 한다면 
- filter 16개
- 입력 채널 3개에 대응하는 3x3 kernel 4개 가 되게 됩니다.

## 조금 더 좋아 보이는 pytorch 공부 방향
현재까지도 그래왔긴 했지만 이제 조금 더 구체적인 축을 기준으로 프레임워크를 이해하려 합니다.

- 레이어 모듈에서 파라미터가 있는가?
- 입출력은 어떻게 되는가?
- forward에서 무슨 계산을 하는가?
- 현재의 DAG 형태는 어떤가?
- 실제 수식은 어떤 형태인가?
- 해당 객체에는 어떤 주요 속성이 존재하며 다른 모듈에 영향을 받는 요소는 무엇인지
- 어떤 상태를 가지는지

또한 기법 또는 레이어의 구분은 현재로 크게 다음과 같이 하려고 합니다.
- 모델 구조: Conv, Linear, Pooling 등
- 데이터: Normalize, ColorJitter 등
- 최적화 기법: SGD, Momentum, Adam 등
- Learning rate: StepLR, CosineAnnealingLR 등
- Training control: Early stopping, Checkpoint, Best model, Epoch 등

> 바로 이어서 다음 포스팅에서 공부 방향을 적용하여 포스팅을 올리려 합니다.