# MySQLdb 라이브러리
이번 수업에서는 `MySQLdb`라는 이름의 데이터베이스 접속 드라이버 라이브러리를 알게 되었다.

기본적인 설치 방법은 타 라이브러리와 다르지 않게 `pip install mysqlclient`를 통해 받을 수 있었으며, 유사 라이브러리로는 `PyMySQL`이라는 개발자들이 주도적으로 제작한 비공식 커뮤니티 버전 MySQL 라이브러리가 있습니다. 하지만 `MySQLclient`가 C언어를 통해 작성되어 있기 때문에 속도 면에서는 이점이 있습니다. (운영체제에 따라 컴파일 설치가 필요할 수 있습니다.)

기본적인 흐름은 `JDBC Driver`와 비슷하게 직접 데이터소스 지정 (url과 사용자, 비밀번호) 후 연결 및 해제, 커밋 등을 직접 수행하는 방식입니다.

기본적인 사용 예시를 작성해보면
```python
import MySQLdb

conn: Connection = MySQLdb.connect(
  host="접속 서버 주소",
  user="사용자명",
  passwd="비밀번호",
  db="스키마 명"
  # , charset="utf8mb4"
)

# 인자를 통한 출력 형태를 dict로 변경 가능합니다.
# cursor = conn.cursor(MySQLdb.cursors.DictCursor)
cursor: BaseCursor = conn.cursor()

# 탐색
cursor.execute("SELECT * FROM member")

row: tuple | None = cursor.fetchone()
rows: tuple[tuple] = cursor.fetchall()

# 삽입
sql = """
INSERT INTO member(userid, userpw, name, hp, email, ssn1, ssn2, gender)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
"""

data = ("kim01","1234","김철수","010-1111-2222","kim01@example.com","990101","1234567","남")

cursor.execute(sql, data)

conn.commit()

# 커넥션 닫아서 자원 소모 없애주기
conn.close()
```
와 같이 사용할 수 있습니다.

## cursor
`cursor`은 데이터베이스에 SQL을 보내고 결과를 받아오는 객체입니다.

기존 자바에서는 `Prepared statement` 작업물을 준비한 뒤, `executeQuery()` 등을 통해 `ResultSet`이라는 결과물을 받아오는 형식이 일반적이었다면, `cursor`은 상대적으로 더 간단하게 쿼리의 수행 요청을 할 수 있습니다.

`cursor`가 `execute`를 하는 경우에는 즉시 결과를 반환하지 않으며, 이는 DB에 해당 쿼리를 실행해달라는 요청만 하는 상태가 됩니다. 이때 반환값은 결과 또는 변경된 행의 개수를 반환합니다.

여기에서 반환값을 가져오기 위해서는 `fetchone()`, `fetchmany(N)`, `fetchall()` 메서드를 이용해 주어야 합니다.

`cursor`은 이터레이터와 닮아 한 칸씩 이동하며 데이터를 가져오게 됩니다.

구체적인 동작 순서를 알아보면, `cursor.execute(query)`를 하게 된다면, 해당 요청은 바로 `connection`을 통해 MySQL 서버에 전달되게 됩니다. 하지만 `commit()`을 하기 전에는 현재 `connection`(세션)에서만 보이게 되며, 다른 `connection`에서는 보이지 않을 수 있는 상태가 됩니다. 이것은 데이터베이스의 가시성과 격리 수준 설정에 따라 차이를 보이게 됩니다. 일반적으로 `READ COMMITTED` 또는 `REPEATABLE READ` 등을 사용합니다. 

`SELECT`를 하는 경우에는 겉모습만 보면 `JPA`의 영속성 컨텍스트 또는 `LAZY LOADING`과 비슷하게 느껴질 수 있는데 `MySQLdb`는 위의 개념과 전혀 관계없이 `SELECT` 한 결과를 그대로 가지고 있으며 `fetch`를 한다고 `LAZY LOADING` 문제와 같이 `N+1` 문제를 고려하지 않아도 됩니다.

> MySQLdb는 SQL ORM이 아니기 때문에 대체로 일반 SQL을 사용하는 감각과 동일하게 사용이 가능합니다.
