# 파이썬을 통한 콘솔 기반 MVC 
> 기존에 익숙하던 자바에서 파이썬을 하게 되며 파이썬의 문법과 라이브러리를 이용하여 `MySQL`과 연동한 콘솔 기반 MVC를 만들었습니다.
[제작된 작업물 코드](https://github.com/hurwan0629/lang-chain-KDT/tree/main/workspace/personal/small_project/mvc_test_default)

## 시작하기에 앞서 제작 소감
우선 해당 작업은 짧게 파이썬 문법에 대한 감을 잡기 위해 빠르게 만든 작업물로 약 2시간 이하의 시간이 걸렸습니다. 일부 유효성 검사를 철저하게 하진 않았으며 문법 또한 빡빡하게 지키진 않았습니다. 해당 작업은 감을 잡기 위한 작업으로 차차 부족한 부분을 보완해 나가려고 합니다.

## 설계
일단 무슨 언어로 하든 설계를 먼저 해야 한다고 생각해서 설계하게 되었습니다. 링크에도 작성되어 있지만 이건 작업의 중요한 부분 중 하나이기 때문에 아래에 작성해 놓겠습니다.

````markdown
# 제작 전 설계

단어장은 이미 했고, 전화번호부는 이미 한 사람들이 있어서 Todo 리스트 정도로 무난하게 하면 좋을 것 같습니다. (너무 많은 시간을 쓰기 싫고 1시간 이내로 끝내고 싶어서)

## 데이터베이스
스키마: temp_db (사용 후 삭제할거라)

테이블: todo (하나만. 빠르게 하기 위해)

| 번호 | 컬럼명 | 내용 | 제약조건 |
|:---|:---|:---|:---|
| 1 | todo_pk | 고유 식별자 | PRIMARY KEY, AUTO_INCREMENT |
| 2 | todo_title | 제목 | NOT NULL |
| 3 | todo_content | 내용 | NOT NULL |
| 4 | created_at | 생성날짜 | NOT NULL, DEFAULT now() |
| 5 | updated_at | 업데이트 상태 | NULL 가능 |

> `DELETE` 대신 논리적 삭제로 `DELETED TINYINT` 사용 가능하지만 `DELETE` 쿼리 사용을 위해 직접 삭제

```SQL
CREATE DATABASE temp_db 
DEFAULT CHARACTER SET utf8mb4 -- 이모지 포함 (+모든 한자)
COLLATE utf8mb4_general_ci; -- 대소문자 구별 안함

USE temp_db;

CREATE TABLE todo(
	todo_pk BIGINT AUTO_INCREMENT PRIMARY KEY,
	todo_title VARCHAR(1000) NOT NULL,
	todo_content TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	updated_at TIMESTAMP NULL
);

SELECT * FROM todo;
```

## 서버
- DTO: Todo_dto
- DAO: Todo_dao
- service: Todo_service
- controller: 생략

## 실행
- while문을 통해 실행

> 구체적인 것은 코드를 통해 구현하겠습니다.
````
위와 같은 형태를 통해 간략하게라도 확실하게 진행 과정을 미리 확인하고 시작할 수 있었습니다. 그중 가장 중요하다고 생각한 부분은 데이터베이스로 로직은 작은 규모이기 때문에 틀만 잡아 두고 알아보며 작업해도 되지만 데이터의 경우에는 한 번 선언하고 바꿔 버리면 모든 구조를 갈아엎어야 했기 때문에 데이터 형태는 고정하고 진행하였습니다.

## 로직
이번 작업의 주요 목표인 파이썬을 통한 MVC, 객체 형태, 라이브러리 사용, 은닉화 등에 대한 개념을 아는 과정이 있었으며, 주로 배운 내용으로는
- 모듈화
- 데코레이터
- 은닉화 방식
- `getter`/`setter`, `toString`(`__str__`, `__repr__`)
- 디스패치 테이블 사용

이었습니다.

### 모듈화
파이썬에서는 자동으로 묶이는 방식이 자바보다 더 느슨합니다. 일반적으로 자바의 경우에는 항상 `import`를 할 때 정확한 지점을 명시해 주어야 하지만 파이썬의 경우에는 딱히 패키지로 만들지 않아도 파일 자체가 곧 모듈이 됩니다.

이를 한 번 경험하기 위해서 `data/` 폴더를 따로 제작하여 `conn.py`(데이터베이스 커넥션 및 데코레이터), `Todo_dao.py`, `Todo_dto.py`를 새로 만들게 되었습니다. 여기에서 `data/` 폴더를 파이썬에서 패키지라고 부릅니다.

이렇게 만들어진 패키지를 외부에 공개하기 위해서 정리할 때에는 `__init__.py`를 활용하여 공개할 클래스들을 정리하였습니다.(패키지 초기화) 모습은 아래와 같습니다.

```python
from .Todo_dao import Todo_dao as Dao
from .Todo_dto import Todo_dto_insert as Dto_insert
from .Todo_dto import Todo_dto_update as Dto_update
from .Todo_dto import Todo_dto_delete as Dto_delete

__all__ = ["Dto_insert", "Dto_update", "Dto_delete", "Dao"]
```
이를 통해서 `from data import *`로 `__all__`의 클래스들을 한 번에 불러올 수 있습니다.

또한 위와 같이 패키징을 하여도 여전히 `from data.Todo_dto import Todo_dto_insert`와 같은 직접 참조가 가능합니다.

> `from .file`과 `from file`에서 `.`의 의미는 현재 패키지를 의미합니다. `.`이 없으면 `sys.path` 기준으로 탐색이 됩니다.

### 데코레이터

데코레이터는 프록시 방식과 유사한 형태로 사용되는 문법입니다. 이는 데코레이터 패턴과 동일하며 아래와 같이 사용됩니다.
```python
def some_decorator(func):
    def wrapper():
        print(f"{func.__name__} 실행 시작")
        result = func()
        print(f"{func.__name__} 실행 종료")
        return result
    
    return wrapper

@some_decorator # 만들어둔 객체 (데코레이터 패턴과 동일)
def func():
    pass
```
이러한 방식을 통해 기존 수업에서 반복적으로 사용했던 데이터베이스 연결과 연결 해제, 커서의 연결과 연결 해제, 그리고 인자를 통한 연결 방식과 커밋 여부 등까지 제어할 수 있었습니다. 

그중 약간의 문제가 일어났었던 부분은 `do_commit`과 `cursor_type`을 가변적으로 제어하기 위하여 데코레이터에 인자를 주었었는데 이 경우(데코레이터 팩토리)에는 모든 데코레이터 뒤에 `@decorator(arg)`와 같이 인자가 없어도 반드시 괄호를 넣어 주어야 했으며, 내부 래퍼를 이중으로 관리하여 아래와 같이 제작했어야 했습니다.
```python
def sql_dec(do_commit=False, cursor_type=None):
  def decorator(func):
    def with_conn(*args, **kwargs):
      # try/exception/finally를 통한 예외 처리 및 자동 연결/해제

      return result
  
    return with_conn
  return decorator
```
위와 같은 이중 데코레이터(데코레이터 팩토리)를 통해 실제 사용 함수와 그 함수의 인자, 그리고 데코레이터의 인자까지 받는 데코레이터가 될 수 있었습니다.

해당 데코레이터를 사용하면 실제로 사용되는 방식은 아래와 같이 동작합니다.
```python
# 실제 실행 함수
@sql_dec(cursor_type=DictCursor)
def search_by_title(self, cur, todo_title):
  cur.execute(self.sql_search_by_title, (todo_title, ))

  return cur.fetchall()

# 동작되는 방식
# 1. search_by_title = sql_dec(cursor_type=DictCursor)(search_by_title)이 동작
# 2. decorator(search_by_title)을 통해 with_conn을 반환해 주려 함
# 3. 실제로 with_conn(...)이 실행됨
```
이를 통해 매개변수는 `sql_dec`가 먹고 실제 함수 객체는 `decorator`가 먹으면서 최종적으로 래퍼 함수가 실행됩니다. (이건 좀 재밌었습니다)

> 알아보니 이중 데코레이터 방식은 정확히 **데코레이터 팩토리**라고 부르며 일반 데코레이터는 함수를 받아서 감싼 함수를 반환하고, 데코레이터 팩토리는 일반 데코레이터를 만들어서 반환하는 함수입니다.

### 은닉화와 매직메서드
파이썬의 은닉화 또한 이전 매우 직관적인 자바에 비해서 더욱 추상적으로 느껴졌습니다. `Todo_dto`를 만들 때 `__init__`에는 `self.var = var`로 선언해 놓고 이후에 `@property`, `@var.setter`에서 실제로 불러올 때 사용하는 함수를 `self.__var`로 설정하여 은닉하는 방식은 꽤 신선하게 느껴졌습니다. 여기에서 도메인 레벨의 유효성 검사를 더욱 강화할 수 있겠다고 확실하게 느꼈습니다. (실제로 은닉화가 되진 않고 **맹글링**이 됩니다.)

### 디스패치 테이블
마지막은 그렇게 크게 중요하진 않았지만 한 번 써 보고 싶었던 디스패치 테이블의 사용이었습니다.

이전에는 자판기식 `if`문을 활용하여 사용자에게 입력받은 메뉴를 일일이 검사했는데 이번에는 디스패치 테이블(딕셔너리와 함수 객체)을 활용하여 즉시 접근이 가능하게 하였습니다. 또한 이를 통해서 나중에 작업을 추가하기가 더 편하겠다고 생각하였습니다.

```python
class Menu:
  def __init__(self):
    self.service = Todo_service()
    self.menu = {
      1: self.service.create_todo,
      2: self.service.show_all_list,
      3: self.service.search_title,
      4: self.service.update_todo,
      5: self.service.delete_todo
    }
  
  
  def run(self):
    while True:
      print()
      print("===== Todo 프로그램 =====")
      print("1. 할 일 등록")
      print("2. 할 일 전체 조회")
      print("3. 제목으로 검색")
      print("4. 할 일 수정")
      print("5. 할 일 삭제")
      print("6. 프로그램 종료")

      try:
        menu = int(input("메뉴를 선택하세요: "))
      except ValueError:
        print("숫자를 입력해주세요.")
        continue

      try:
        func = self.menu.get(menu, None)
        if func is not None:
          func()
        elif menu == 6:
          print("프로그램을 종료합니다.")
          break
        else:
          print("메뉴는 1부터 6까지만 선택할 수 있습니다.")
    # ...
```

## 후기
앞서 이미 말씀드리고 시작했지만 확실히 파이썬은 자바와 다른 부분이 많기도 하고 개발자가 좋아하는 제약이 많은 환경이 아니기 때문에 더욱 신경 써야 할 부분이 많은 것 같았습니다. 특히 **Pylance**를 사용 중, 오류 검사가 정확하게 이루어지지 않아 은근히 불편하기도 했던 것 같습니다.

아무튼 좋은 훈련이 되었고 앞으로도 이어나가려 합니다.
