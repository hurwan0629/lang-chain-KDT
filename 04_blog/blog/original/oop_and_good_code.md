# 객체지향과 파이썬의 클린 코드

## 
**객체지향**하면 언제나 이야기되는 4가지 특성이 있다.
- 상속: 자식 클래스는 부모 클래스의 속성(필드와 메서드)을 그대로 쓸 수 있습니다.
- 추상화: 불필요한 세부 사항을 제거하고, 사물의 핵심만을 추출하여 단순화한 것입니다. 
- 다형성: 실제로 사용하는 객체에 따라 같은 이름이지만 다른 내용의 작업이 수행되는 현상입니다. (동적 바인딩에 의해 실현됩니다.)
- 캡슐화: 클래스의 복잡한 로직 등과 외부에 주면 안되는 값들을 은닉화하여 외부에서 의도한대로 사용하게 하는 방식입니다. 연관된 데이터와 로직을 하나의 객체로 묶는 것을 말합니다.

이 4가지는 객체지향 언어에서 높은 유지보수성과 가독성 및 재사용성을 위한 OOP의 강력한 기능입니다.

> 기존에 자바를 주로 해왔던 저에게는 파이썬의 **개발자 책임**의 코딩 방식은 조금 익숙하지 않아, 공부할 대상이 되었습니다. *귀도 반 로섬*의 `We are all consenting adults here`라는 철학에 따라 이런 방식의 코딩이 의도되었음을 알 수 있습니다.

## 파이썬의 클래스 기초
파이썬의 클래스는 기본적으로
`class ClassName([상속받을 클래스들]):`을 통해 정의가 가능합니다.

기존의 자바 사용자라면 헷갈릴 수 있는 부분이 존재하는데요.

파이썬에서는 위치에 따라 `클래스 변수`, `인스턴스 변수`, `정적 메서드`, `getter`, `setter`, `속성 은닉화` 등의 문법이 크게 엄격하지 않게 설정되었기 때문입니다.

우선 코드를 보고 이야기 해보겠습니다.
```python
class ExampleClass():

  cls_var = "hello fellas" # public static String cls_var = "hello fellas";
  _cls_var = "better not use this" # 동일한 공개이지만 관례상 외부에서의 사용을 권장하지 않음
  __cls_var = "you can't see this" # 강하게 막지는 않지만 Name Mangling을 통해 직접 접근하기 어려운 방식이 됩니다.

  def __init__(self, name, password):
    self.name = name
    self.__password = password

  def _this_is_logic(self, message: str) -> str:
    return f"hello! I'm {self.name}. here is message: {message}"
  
  def hello_guys(self, message: str) -> str:
    return self._this_is_logic(message)

print(ExampleClass.cls_var)
print(ExampleClass._cls_var)
# print(ExampleClass.__cls_var)
print(ExampleClass._ExampleClass__cls_var)

e = ExampleClass("David", 1234)

print(e.name)
# print(e.__password) # 맹글링
print(e._ExampleClass__password) # 값이 나옴
print(e._this_is_logic("hello"))  # 사용 가능
print(e.hello_guys("good to meet you!"))

print(e.cls_var)
ExampleClass.cls_var = "changed"
print(e.cls_var)
e.cls_var = "again" # 인스턴스 클래스가 생성됨
print(e.cls_var)
print(ExampleClass.cls_var)
```

이렇게 변수를 은닉하거나, 메서드 사용을 권장하지 않음을 대부분 암시적으로 표현하게 됩니다.

## 파이썬 클래스와 메모리 구조
### 클래스 객체
이전 [포스팅](https://hurwan.tistory.com/9)에서 이야기 했듯, 함수와 같이 클래스 또한 **클래스 자체에 대한 객체**(인스턴스와 다름!!)가 생성하게 됩니다.

클래스를 생성하면 대략적으로
1. 클래스용 `namespace` 생성
2. 클래스 변수 저장
3. 클래스 내부에서 선언한 함수들의 객체를 생성 후 저장
4. `type`이 `namespace`를 바탕으로 클래스 객체 생성

하게 됩니다.

구성된 `Person`객체(인스턴스 아님)의 모습에는
- `__name__`: `Person`
- `__bases__`: (object, 상속받은 클래스들)
- `__dict__`: 클래스 변수, 저장된 함수, 나머지 속성들
- `__mro__`: 실제로 상속되는 순서 (메서드명의 충돌 방지를 위한 알고리즘에 의한 순서도)

### 인스턴스 객체
파이썬의 인스턴스는 `p = Person()`과 같은 코드를 통해 생성됩니다.

이때 내부적으로 `Person.__new__(Persion)`을 통해 빈 인스턴스 객체를 생성하며 `Person.__init__(p, "David")`를 통해 내부값을 초기화해주게 됩니다.

이렇게 만들어진 인스턴스, `p`는 아래와 같은 모습을 갖게 됩니다.
- `__class__`: `Person`
- `__dict__`: name, 그 외 필드값들

### 메서드
파이썬에는 **메서드**라는 개념이 존재하지만 실제로는 그것 또한 함수로 구현되어있습니다.

하지만 인스턴스를 만든 뒤 해당 객체를 통해 함수를 호출하면, 파이썬은 해당 함수를 객체와 연결(`Binding`)하여 `메서드`라는 특수한 상태로 만들게 됩니다.

이때, 함수에 선언되어있는 `self`를 명시 또는 암시적으로 입력하여 인스턴스의 메서드 호출시 해당 메서드가 메서드를 사용함을 알 수 있습니다.