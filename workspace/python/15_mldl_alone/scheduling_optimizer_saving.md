# [머신러닝] CNN AlexNet 수업 복습
> 이번에는 수업 내용을 더 확실하게 복습하기 위해 정리를 한번 하였습니다. 코드를 따라 치는 것도 좋은 방법이지만 이번에는 수업 내용을 제 언어로 정리를 해보았습니다.

## Alexnet
수업은 AlexNet을 소개하면서 시작되었습니다. 이는 `ImageNet Large Scale Visual Recognition Challenge`에서 우승한 딥러닝 모델로, 딥러닝의 대중화를 이끈 합성곱 신경망이라고 합니다

이는 $3 \times 227^2$ 데이터를 받아 추론하며 `합성곱 5개` + `완전연결 레이어(full connected) 3개`로 이루어져 있습니다.

이는 1000개의 데이터 클래스로 이루어진 데이터 분류문제 약 1,500만개 이미지 셋을 이용하여 만들어졌으며 가장 높은 확률이 맞을 확률 62.5%, 높은 확률 상위 5개중에 포함될 성능이 82.5%로 1000개 클래스 대비 매우 높은 성능을 만들었습니다. (그 당시 기준)

## 수업 프로젝트 시작
수업 프로젝트는 **CIFAR-10** 데이터셋을 이용하여 이루어졌습니다.

이는 $32\times32$ 크기의 컬러 이미지 6만장으로 구성되어있고 학습용:테스트용 = 5:1 비율이며 클래스 수는 10개로 나와있습니다.

## 코드 흐름
### 환경 설정
우선 시드를 결정하고 진행하였습니다.
`SEED=2026`을 통해 상수를 하나 선언한 뒤 `random, np.random, torch.manual_seed`를 통해 시드값을 넣어주었습니다.

이후에 `torch.cuda.is_available()`을 이용하여 `torch.device("cuda")`를 넣어주었습니다. 

### 데이터셋 설정
`Path` 모듈을 이용해서 디렉토리 경로를 받았습니다. 또한 `torchvision.datasets.CIFAR10`을 이용하여 검증된 데이터극 root 데이터 폴더를 기반을 train=True, False, download=True/False, transform=transforms.ToTensor() 을 이용하여 기본적인 이미지를 받아주었습니다.

또한 이미지 정규화 시 batch의 이미지 정규화를 더 안정적으로 해주기 위하여 채널별 mean/std를 구하여 list[int]로 저장해 주었습니다.

이후에는 CIFAR 데이터셋을 불러올 떄 ToTensor() 만 사용하였던 점을 개선하기 위하여 train_transform과 eval_transform을 만들었습니다. 여기에서 각각 방금 만든 mean/std를 사용하여 Normalize를 마지막에 해주었으며 좌우반전, 가운데 자르기 (4픽셀 채워서) 등의 증강 또한 해주었습니다. (학습데이터셋에)

이후에 다시 train_full_dataset, validation_full_dataset, test_dataset를 받았습니다.

이때 validation_full_dataset도 현재 상태에서는 train_full_dataset과 transform이 eval_transform이라는 점만을 제외하면 모두 동일합니다.

### 학습/검증 데이터 분할하기
현재 학습 데이터셋과 검증 데이터셋은 동일한 원본을 바라보고 있습니다.

이를 해결하기 위해 일단 train_dataset의 길이만큼의 인덱스를 추출한 뒤, 모든 타겟 배열을 뽑아주게 됩니다.

이후 Subset을 이용하여 train_dataset과 validation_datset을 만들게 됩니다. Subset(데이터셋, 인덱스)

여기에서 인덱스는 sklearn.model_selection 에서 train_test_split()의 대상에 all_indices라는 인덱스 배열을 넣어주어 인덱스를 분할해주었으며, stratify에 all_targets를 넣어 최종적으로 층화 추출을 해주게 되었습니다.

### DataLoader 만들기
이후에는 만들어진 `validation_dataset`과 `test_datset`을 이용하여 `NUM_WORKERS`를 인자로 넣으며 `DEVICE.type == "cuda"`일 경우에 `pin_memory=True`로 설정해주게 됩니다.

여기에서 `DEVICE`는 `torch.device("cuda"/"cpu")` 객체로 이는 `torch._C.device` 클래스를 말합니다.

이후에 `CIFAR-10`에 존재하는 10개의 클래스 이름을 배열로 하드코딩된 변수를선언해주며 출력 시에 반정규화를 해주기 위해 `denormalize(image, mean, std)` 함수를 이용하여 `[3, 1, 1]` 크기의 채널의 평균, 표준편차를 받아 표준화 시점 이전으로 변경해주게 됩니다.

이때 `(b, 3, n, n)`형태의 `image` 형태의 텐서가 `cuda`에 존재하면 이를 다시 복구해주는 `.cpu()`메서드를 사용해줍니다.

이후에 전체 `raw_train_dataset`의 `mean`과 `std`를 구해주게 됩니다.

### 시각화하기
이후에 이렇게 만든 데이터가 잘 존재하는 것인지를 확인하기 위해 `rows, cols = 5, 5`로 설정해준 뒤 이를 순회하며 `figure.add_subplot(rows, cols, index+1)` 을 이용하여 `axis`를 생성하며 `axis.imshow(to_pil_image(image))`를 이용하여 파이썬에서 기본 제공하는 **PIL** 타입으로 텐서를 변환하여 출력해주게 됩니다.

이때 해당 코드를 더 자세히 알아보면 figure을 하나 크게 `plt.figure()`를 이용하여 추가하게 됩니다.

이후에 논리적으로 `rows`, `cols` 로 나뉜 뒤 `n`번째 위치의 Axes 객체를 하나 만들어서 반환해주게 됩니다. 이때 `matplotlib subplot` 위치 번호는 1부터 시작하게 됩니다.


### 모델 만들기
이번에는 모델을 만들었습니다.

이름은 `AlexNetCIFAR10`이며 생성자의 인자로는 최종적으로 출력하는 클래스의 개수, `num_classes`를 만들어주었으며 기본 값은 `CIFAR-10`에 맞는 10으로 설정되어잇습니다.

또한 모델 레이어들은 AlexNet의 설계와 동일하게 특징 추출계층 5개와 완전 연결계층 3개로 만들어 두었습니다.

이번에 저희가 사용하는 이미지의 크기는 32x32 였기 때문에 이를 올바른 형태로 수정해주게 되었습니다.

크게 3가지의 속성을 만들주었는데 이름은 각각 `features`, `avgpool`, `classifier`이였습니다.

최종적으로 `forward(self, x)` 를 이용하여 로짓들을 반환해주는 방식을 사용하였습니다.

이후에 모델 선언과 동시에 `.to(DEVICE)`를 통해 이 또한 `gpu`에서 실행이 되게 만들어주었습니다.

### 파라미터 확인하기
파라미터를 확인하기 위하여 2가지 메서드를 활용하였습니다.

`nn.Module`에서 기본으로 제공하는 `.parameters()`를 이용하여 모든 모델에 재귀적으로 파라미터 개수를 탐색해주었습니다. 여기에서 특정 레이어에는 `w`, `b`가 존재하며 `w`의 요소와 관계없이 모두 `1`개의 파라미터로 취급되게 됩니다.

여기에서 학습 가능한 레이어가 실제로 8개밖에 없으며 각각 `w`와 `b`를 가지고 있기 때문에 총 16개의 파라미터가 있다고 나옵니다.

또한 각각의 `w`와 `b`는 `(output, input, ...)`, `(output)` 형태로 되어있기 때문에 총 개수를 구하려면 모든 파라미터에 대해서 `numel()`의 값을 더해주어야합니다. 또한 학습 되는 파라미터만 구하기 위해서는 컴프리헨션 뒤에 `if p.requires_grad`를 넣어주면 됩니다.

### 테스트 확인해보기
한번 형태가 어떻게 변하는지를 확인하기 위해 `torch.inference_mode()`를 이용하여 DAG가 만들어지지 않게 하여 연산 기록이 남지 못하게 하였습니다. 또한 이 때에는 `model.eval()` 등과 같은 효과가 발생하지 않습니다.

### 옵티마이저 설정
이후에 손실함수로 `CE` 를 사용해주었으며 옵티마이저로 AdamW를 채택하며 내부에 모델의 파라미터 (현재 모든 파라미터가 trainable하기 떄문에 모두 넣기), 학습률 `0.001`, 가중치 감쇠율 `weight_decay=0.0001`을 넣어주게 되었습니다.

또한 학습이 임계치 근처로 갔을 때 학습률을 낮추어주기 위하여 `lr_scheduler.ReduceLROnPlateau`를 이용하여 스케줄링을 해주었습니다.

`ReduceLROnPlateau`의 인자로는 몇번을 기다리는지에 대한 `patience=5`, 어떤 경우에 대해서 트리거로 할 지에 대한 `mode="min"`, 몇배로 학습률을 줄일지에 대한 `factor=0.5`를 지정해주었습니다.

### 주요 학습/평가 함수
이번에는 `train_one_epoch`와 `evaluate` 함수를 만들었습니다.

이 두 함수는 공통적으로 `data_loader`, `model`, `criterion`, `device`를 받아 모델을 돌리며 평가 (loss와 correct)를 할 수 있게 해주며 `train_one_epoch`에서는 추가적으로 최적화 알고리즘을 통해 가중치를 조절해주어야하기 때문에 `optimizer` 인자를 추가적으로 받아주게 됩니다.

당연하게도 `evaluate` 함수에서는 `criterion.backward()`또한 하지 않습니다.

### Early Stopping
이후에 모델의 최소 Loss가 나올 때에 이를 저장해주기 위해 `OUTPUT_DIR`이라는 `Path` 타입을 만들어주게 됩니다.

이후에 `OUTPUT_DIR / "alexnet_cifar10_best.pth"` 경로를 만들어 저장할 준비를 하게 됩니다.

이후에 `torch.save(model.state_dict(), BEST_MODEL_PATH)`를 이용하여 파라미터를 원하는 경로에 저장해주게 됩니다.

이후에 `range(1, EPOCHS+1)`만큼 반복을 돌려주며 `train_one_epoch`를 돌려준 뒤, `evaluate`를 합니다. 이후에 `evaluate`를 통해 나온 `loss` 값을 바탕으로 `scheduler.step(validation_loss)`를 해주어 스케줄러가 해당 개선도를 확인해주며 `lr`을 감소시키거나 그대로 유지하게 됩니다.

