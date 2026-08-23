# [머신러닝] CNN과 머신러닝의 진행과정
> 이번에는 프로젝트를 짜는 큰 틀에 대해서 알아보았습니다.

최근까지는 수학과 라이브러리의 구조를 위주로 공부를 하였었습니다. 이는 굉장히 재미있고 근본을 이해함으로써 향후 복잡한 과정도 쉽게 풀어서 사고할 수 있는 능력을 만든다고 믿습니다. 

하지만 이번 수업에 CNN 분석 프로젝트를 보니 한번쯤은 큰 틀을 이해하고 가는 것이 중요하다고 생각이 들었습니다.

특히 이번 수업과정에서 강사님의 질문에 대한 정답률이 상대적으로 떨어졌으며 코드의 큰 흐름을 제대로 추적하지 못하는 상황도 발생했었습니다.

현재 진행중인 코드는 [여기 (깃 레포)](https://github.com/hurwan0629/lang-chain-KDT/blob/main/workspace/python/14_scikit_learn/24_hand_draw_custom.ipynb)에 존재합니다.

## 순서대로 따라가다 막히는 위치에서 파고들기
> 일단 코드의 흐름을 쭉 따라가보겠습니다.

초반에는 데이터를 불러오기 전에 데이터의 위치를 설정하였습니다.

`extract_dir = Path("./data")` 를 통하여 데이터를 해당 폴더에서 가져올 것임을 나타내었으며 아래에는 `.exists()`와 `.mkdir()`을 이용하여 폴더가 없는 경우를 해결해주었습니다.

또한 `SEED`를 상수와 같이 설정하여 `random.seed(SEED)`, `np.random.seed(SEED)`, `torch.manual_seed(SEED)`를 설정해주었습니다.

이후 `zipfile` 모듈을 이용하여 `zip` 데이터를 해당 폴더에 그대로 풀어주었습니다.

### torchvision.ImageFolder(Path)

여기에서 흥미로운 클래스가 나왔는데 `torchvision.ImageFolder(Path)`를 이용하여 데이터셋을 만들었습니다.

ImageFolder 클래스는 폴더 구조를 보고 이미지 분류용 `Dataset` 객체를 만들어주는 클래스입니다.

`ImageFolder` 생성자의 인자로 `Path` 객체를 넣어주게 된다면 `ImageFolder`가 하위 폴더 이름을 클래스로 인식하게 됩니다. 이후에는 `ImageFolder` 객체가 하위 폴더 이름을 클래스로 인식하게 됩니다. 또한 이름의 경우에는 따로 설정할 수 있습니다.

또한 `dataset.samples`에는 `list(tuple(path, label))` 형태가 저장되게 됩니다.

