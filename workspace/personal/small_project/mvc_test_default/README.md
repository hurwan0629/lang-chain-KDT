# DB와 파이썬 연동 프로그램 
MySql과 Python의 PyMySQL 라이블러리를 통해 가벼운 복습을 하려고 합니다.

이전에 자바를 통해 익숙한 구조이지만 파이썬를 통해서는 FastAPI이외에 드라이버만을 이용하여 만든 웹 프로토타입 보다 더 가벼운 코드를 통한 구현을 해보려 합니다.

시작하기 전에 미리 했던 작업들을 정리해보자면 ([이 파일](../../../python/class/2026-06-09/mysql_connection.ipynb))
- `Word`(DTO) 타입
  - `__repr__`을 통한 `toString` 구현
  - `@property`, `@setter`을 통한 데이터 은닉(캡슐)화
- `WordsDAO`
  - 초기화 시 `db=None`로 초기화
  - `connect()`를 통해 `MySQLdb`에 연결
  - `disconnect()`를 통한 `MySQLdb` 연결 끊기
  - `insert`, `search`, `select_all`, `update`, `delete`를 통해 CRRUD를 모두 구현. 이때 앞뒤로 `connect()`와 `commit()`, `disconnect()`를 통한 연결 관리
- `WordsService`타입
  - 반환할 대상(프론트)가 없다시피 하기 때문에 그냥 바로 출력되는 형태로 만들어져있음
  - `insert_word`, `print_all`, `search_words`, `edit_word`, `delete_word`로 이루어져있음.
- `Menu`타입
  - 초기화 시 `WordsService`인스턴트 생섯ㅇ
  - 반복문을 통해 작업 구현

> 개선할만한 포인트: 전략 패턴으로 `if`문 초기화, 데코레이터를 직접 만들어 연결/연결끊기 자동화