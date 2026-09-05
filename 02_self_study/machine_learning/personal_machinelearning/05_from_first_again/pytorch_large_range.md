# [PyTorch] 파이토치에서 영향을 주는 요소들


## 실행 환경
torch 패키지에서는 프로그램 전체의 계산 방식에 영향을 줄 수 있는 설정들이 존재합니다.

대표적인 요소들은 다음이 있습니다.

- `.manual_seed(int)`
- `.set_num_threads(...)`
- `.set_float32_matmul_precision(...)`
- `.backends.cudnn.benchmark`
- `.backends.cudnn.deterministic`

또한 장치와 관련하여 `torch.cuda.is_available()` 등의 내용이 존재합니다. 

## Tensor의 기본 생성 규칙
`torch` 패키지에서 `Tensor`이 생성될 경우 만들어지는 Tensor의 dtype에 대한 설정 또한 가능합니다.

> `torch.set_default_dtype(torch.float64)`, `torch.sest_default_device("cuda")` 과 같은 것이 있습니다.

경우에 따라 명시적으로 `torch.tensor(..., device=device)`, `.to(device)` 등과 같은 명시적인 코드를 사용할 수도 있습니다.

## Autograd 실행 모드
`torch.set_grad_enabled(...)` 또는 `with torch.no_grad():`, `with torch.inference_mode():` 등을 이용하여 grad_fn을 만들지, Autograd가 기록할지, backward 가능한 그래프를 만들지 등에 대한 이야기입니다.

## 정밀도 실행 모드
GPU 학습에서 `with torch.autocast(device_type="cuda"): y = model(x)` 과 같은 코드가 있을 때, 