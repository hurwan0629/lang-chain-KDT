# MySQL DML에 대해서 (SELECT 위주)
데이터베이스에는 총 4가지의 명령어 종류가 존재합니다.
- Data Definition Language: 데이터베이스 구조 관리 명령어
- Data Manipulation Language: 데이터 조작 언어
- Data Control Language: 사용자 또는 보안 관리
- Transaction Control Language: 데이터베이스 작업 단위 관리 명령어

위 4가지 종류의 명령어는 모두 중요하지만 가장 많이 쓰이는 명령어는 `DML`입니다. `DML`의 명령어에는 크게 4가지가 존재합니다.
- `INSERT`: 삽입
- `SELECT`: 조회
- `UPDATE`: 수정
- `DELETE`: 삭제

위 4가지를 줄여서 `CRUD` 또는 단일 선택, 복수 선택을 나누어서 `CRRUD`라고 부릅니다.

이번에는 `DML`의 여러가지 활용법까지 알아보도록 하겠습니다.

## INSERT
`INSERT`는 테이블에 데이터를 삽입할 때 사용되는 명령어입니다. 일반적인 형태는 
```SQL
INSERT INTO [테이블명] (컬럼1, 컬럼2, 컬럼3, ...) VALUES (값1, 값2, 값3, ...);
```
의 형태로 작성하게 됩니다.

이때 컬럼 목록을 생략하여 데이터를 넣을 수 있는데 그럴 때에는 **반드시 값을 모두 채워주어야합니다.**
```SQL
CREATE TABLE todo(
	todo_pk BIGINT AUTO_INCREMENT PRIMARY KEY,
	todo_title VARCHAR(1000) NOT NULL,
	todo_content TEXT NOT NULL,
	created_at TIMESTAMP NOT NULL DEFAULT now(),
	updated_at TIMESTAMP NULL
);

-- SQL Error [1136] [21S01]: Column count doesn't match value count at row 1
-- 1136: MySQL 고유 오류
-- 21S01: 펴준 SQLSTATE 코드
-- 삽입 시 데이터 개수가 맞지 않아 일어나는 오류
-- INSERT INTO todo VALUES ('SQL 포스팅', 'SQL DML 정리하세요');

-- 올바른 입력
-- DEFAULT 또는 NULL을 넣어 자동 할당을 해줄 수 있습니다.
INSERT INTO todo VALUES (DEFAULT, 'SQL 포스팅', 'SQL DML 정리하세요', DEFAULT, NULL);
```

또한 복수의 데이터를 한번에 넣으려면 아래와 같이 작성할 수 있습니다.
```SQL
INSERT INTO todo (todo_title, todo_content)
VALUES
	('영화보기', '스파이더맨 보고싶다'),
	('선형 대수학 공부', '현재 행렬식까지 공부 완료'),
	('타입 스크립트', '주로 하는 공부는 아니지만 일단 어느정도는 공부해두자');
```
이 또한 컬럼을 생략 가능하지만 동일하게 모든 값을 넣어주어야 합니다.

이와 같이 복수 데이터를 한번에 넣으면 하나씩 넣는 것보다 빠르게 삽입되게 됩니다. (SQL 실행계획 비용 감소) 또한 이는 아직 다루진 않았지만 하나의 트랜잭션으로 처리되게 됩니다. 내부적으로는 각 행을 차례로 처리하게 됩니다.

## SELECT
사실 대부분의 서비스에서 가장 많이 사용되는 키워드는 `SELECT`가 아닐까 싶을정도로 주로 쓰이는 명령어입니다. 데이터 분석이든 웹 서비스이던 데이터를 활용하기 위해서 자주 사용하게 되는 문법인만큼 성능적인 처리방식, 다중 테이블 선택, 함수 등이 함께 다뤄질 수 있습니다.

### 0. 일반 SELECT
`SELECT`문의 기본 형태를 빠르게 알아보면 다음과 같습니다.
```SQL
SELECT 
  컬럼명1, -- AS 별칭1 가능
  컬럼명2, -- AS 별칭2 가능
  ... 
FROM 테이블명 -- AS 별칭 가능
--- 여기서부터는 선택 ---
WHERE 조건식 -- (AND, OR 사용 가능)
GROUP BY 컬럼 -- , 컬럼 2 가능
HAVING 그룹 조건 -- 집계 함수 사용 가능 (보통 GROUP BY와 사용. GROUP BY 없으면 전체를 하나의 그룹으로 인식)
ORDER BY 정렬_컬럼 -- ASC(기본값): 오름차순, DESC: 내림차순
```
으로 이루어져있습니다.

> `SELECT`에 대해서는 파다보면 무한으로 공부할 수 있기 때문에 과하지 않게 파먹도록 하겠습니다.

### 1. 기본 필터링 WHERE, DISTINCT
기본 필터링에서는 `WHERE`과 `DISTINCT`에 대해 이야기하려 합니다.

우선 `DISTINCT`는 단순하게 동일한 컬럼을 제거해주는 방식으로 사용됩니다. 일반적으로 `PK`또는 `ID`컬럼을 통해 중복되는 경우는 많지 않지만 `1:N` 또는 `N:M` 조인, `UNION` 등의 경우에는 중복되는 경우가 있을 수 있기 때문에 알아두면 좋습니다.

진짜로 많이 사용되는 것은 `WHERE`로 이는 먼저 데이터베이스에서 조건별로 데이터를 검사하게 됩니다. 주요한 종류로는 
- 비교연산자: `=`, `!=`, `<>`(`!=`와 동일합니다.), `>`, `<`, `>=`, `<=` 로 `NULL`이 아닌 대부분의 동일한 타입끼리 비교가 가능합니다. 
- 논리 연산자: `AND`, `OR`, `NOT` 로 일반적인 프로그래밍 언어와 동일한 사용 방식입니다.
- 범위 조건: `BETWEEN`, `IN`, `ANY`, `ALL`을 통해 범위를 설정할 수 있습니다. `BETWEEN 작은값 AND 큰값`, `IN (값1, 값2, 값3)`, `ANY (쿼리)`, `ALL (쿼리)`를 통해 사용이 가능합니다.
- 패턴 검색: `LIKE`, `%`, `_` 으로 문자열의 조건을 비교할 때 유용하게 쓰입니다. `컬럼 LIKE 문자열`의 형태로 쓰이며 `%`에는 어떤 길이나 어떤 값이던 들어올 수 있고, `_`는 하나의 아무 문자를 뜻합니다.
- NULL: `IS NULL`, `IS NOT NULL`은 단순히 `NULL`검사에 쓰입니다.
- 정규표현식: `REGEXP`로 `문자열 REGEXP '정규식'`을 통해 활용 가능합니다. 8버전부터는 `REGEXP_LIKE`라는 함수 형태도 사용 가능합니다.

추가로 알면 좋을점은 
1. 날짜는 문자로 `YYYY-MM-DD`로 비교가 가능합니다. `BETWEEN`, `IN`도 가능합니다.
2. `CHAR`은 고정 문자열이기 때문에 비교 시 `(CHAR(10)) 'HELLO'`는 `(VARCHAR(10))'HELLO'`와 다르고 `CONCAT('HELLO', '     ')` 와 같습ㄴ디ㅏ. (설정에 따라 달라질 수 있습니다.)

### 2. 정렬과 범위 제한
그나마 간단한 부분으로 `ORDER BY [컬럼명1 (ASC/DESC)], [컬럼명2 (ASC/DESC)], ...`을 통해 순서를 설정 가능합니다. 여기에서 `ASC`는 생략 가능하며 작성한 순서대로 먼저 정렬되게 됩니다.

`LIMIT [가져올 행 개수] OFFSET [건너뛸 행 개수]`를 통해 가져올 범위를 설정 가능합니다. 탐색 시 원하는 범위를 모두 확인할 때까지 탐색하다 원하는 행을 모두 찾으면 중단합니다.

### 3.집계
`GROUP BY`를 통해 `GROUP BY`에 선택한 컬럼들의 조합이 같은 것들의 그룹으로 나누게 됩니다. 선택된 그룹들은 보통 하나의 행으로 표현되며, 집계함수 `COUNT`, `SUM`, `AVG`, `MAX`, `MIN` 등을 통해 정보를 확인 가능하며 뒤에서 설명할 여러 함수를 통해 더 세세한 정보를 가져올 수 있습니다. (서브쿼리도 가능) 

선택된 그룹들 중에서 특정 조건을 통해 선택을 하고 싶은 경우에는 `HAVING 조건(예를 들어 SUM(account) > 2000000)`을 통해 구체적인 석택이 가능합니다.

`NULL` 값들도 하나의 그룹으로 취급합니다.

### 4.함수와 조건
`CASE WHEN ~ THEN END`, `IF`, `IFNULL`, `COALESCE`, `NULLIF`를 통해 컬럼 값을 변환시킬 수 있습니다.

```SQL
CASE 
  WHEN 조건1 THEN 값
  WHEN 조건2 THEN 값2
  WHEN 조건3 THEN 값3
  WHEN 조건4 THEN 값4 
  ELSE 값5 
END
```
와 같이 하나의 스칼라로 입력이 가능하며 `IF`는 더 단순하게 `IF(조건, 참값, 거짓 값)`을 통해 활용 가능합니다.

`IFNULL`과 `COALESCE`, `NULLIF`는 모두 `NULL`을 거르기 위한 함수로 `IFNULL(값, NULL_일결우_대체값)`, `NULLIF(값1, 값2)`을 통한 두 값이 같으면 `NULL`과 `COALESCE(값1, 값2, ..., 최종값)`을 통해 최초의 `NULL`이 아닌 값을 반환합니다.

이외의 함수들로는
- `FORMAT(n, 자릿수)`: 숫자를 쉼표가 포함된 문자열로 변환
- `NOW()`: 현재 날짜와 시간
- `ABS(n)`: 절댓값
- `ROUND(n, 자릿수)`: 반올림
- `CEIL(n)`: 올림
- `FLOOR(n)`: 내림
- `TRUNCATE(n, 자릿수)`: 지정 자릿수 이후 버림
- `MOD(a, b)`: 나머지
- `POW(a, b)`: 거듭제곱
- `CONCAT(a, b, ...)`: 문자열을 연결
- `CONCAT_WS(',', a, b)`: 구분자를 넣어 문자열 연결
- `LENGTH(str)`: 문자열의 바이트 길이
- `CHAR_LENGTH(str)`: 문자열의 문자 개수
- `UPPER(str), LOWER(str)`: 대·소문자로 변환
- `SUBSTRING(str, 위치, 길이)`: 문자열 일부 추출

등이 있습니다.

### 다음을 기약
`SELECT`에 할게 많아서 다음번에는 2번에 나누어 
1. `JOIN`, `서브쿼리`, `UNION`/`UNION ALL`
2. `CTE`, `WITH`, `EXPLAIN`, `SELECT FOR UPDATE`에 대해서 다루도록 하겠습니다.

## DELETE
`DELETE`는 일반적으로 한번 삭제 후 `COMMIT`시 거의 되돌릴 수 없기 때문에 잘 사용되지 않습니다.

형태는 `DELETE FROM 테이블 WHERE 조건`입니다. 

하지만 데이터를 삭제하지 않기 위해서는 논리적으로 `IS_DELETED`와 같은 컬럼을 사용하거나 다른 방안을 써야합니다.

## UPDATE
`UPDATE`는 데이터를 수정하는 명령어로 `UPDATE 테이블 SET 컬럼1 = 값, 컬럼2 = 값, ... WHERE 조건`을 통해 사용 가능합니다.