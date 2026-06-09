# MySQL 기본 개념 정리

> 이 글은 MySQL 8.4를 기준으로 뷰, DDL, 사용자와 권한, 테이블 및 저장 엔진의 기본 개념을 정리한 글입니다.

## 뷰

뷰(`VIEW`)는 `SELECT` 문의 결과를 테이블처럼 조회할 수 있게 만든 데이터베이스 객체입니다.

```sql
CREATE VIEW member_view AS
SELECT
    member_pk AS pk,
    member_id AS id,
    member_hobby AS hobby
FROM member;
```

뷰는 일반적으로 조회 결과 자체를 별도로 저장하지 않고, 저장된 `SELECT` 문을 실행해 원본 테이블의 현재 데이터를 보여 줍니다. 따라서 원본 테이블의 **데이터가 변경되면** 뷰의 조회 결과에도 반영됩니다.

다만 원본 테이블에 새로운 컬럼을 추가한다고 해서 기존 뷰에 그 컬럼이 자동으로 추가되는 것은 아닙니다. 또한 뷰가 참조하는 컬럼이나 테이블을 삭제하거나 이름을 변경하면 뷰를 조회할 때 오류가 발생할 수 있습니다.

뷰를 사용하면 다음과 같은 이점이 있습니다.

- 복잡한 쿼리를 단순한 인터페이스로 제공할 수 있습니다.
- 자주 사용하는 쿼리를 재사용할 수 있습니다.
- 필요한 컬럼만 노출하고 뷰에 별도의 권한을 부여하여 접근 범위를 제한할 수 있습니다.

컬럼 별칭(`alias`)은 이름을 바꾸어 보여 주는 기능일 뿐, 그 자체로 보안을 제공하지는 않습니다. 보안을 위해서는 원본 테이블의 권한을 제한하고 뷰에 적절한 권한을 부여해야 합니다.

## 데이터베이스 기본

### DDL

DDL(`Data Definition Language`)은 데이터베이스의 구조와 객체를 생성하거나 변경하고 삭제하는 명령어입니다. 대표적으로 `CREATE`, `ALTER`, `DROP`이 있습니다.

DDL은 테이블과 데이터베이스 구조에 큰 영향을 줄 수 있으므로, 운영 환경에서는 영향 범위와 잠금 발생 여부 등을 확인한 뒤 실행해야 합니다.

### CREATE DATABASE

데이터베이스는 다음과 같이 생성할 수 있습니다.

```sql
CREATE DATABASE testdb
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_0900_ai_ci;
```

문자 집합(`CHARACTER SET`)은 문자를 저장하는 인코딩 방식을 지정하고, 콜레이션(`COLLATE`)은 문자열을 비교하고 정렬하는 규칙을 지정합니다.

`utf8mb4`는 문자 하나를 최대 4바이트로 표현할 수 있는 UTF-8 문자 집합입니다. MySQL의 `utf8`은 최대 3바이트만 사용하는 `utf8mb3`의 사용 중단 예정 별칭이므로, 새로운 시스템에서는 `utf8mb4`를 사용하는 것이 좋습니다.

`utf8mb4_0900_ai_ci`의 각 부분은 다음 의미를 가집니다.

- `utf8mb4`: 문자 집합
- `0900`: Unicode Collation Algorithm 9.0.0 기반
- `ai`: 악센트를 구분하지 않음(`accent-insensitive`)
- `ci`: 대소문자를 구분하지 않음(`case-insensitive`)

MySQL 8.4의 기본 문자 집합과 콜레이션은 각각 `utf8mb4`와 `utf8mb4_0900_ai_ci`입니다. 다만 Docker 사용 여부가 문자 집합을 결정하는 것은 아니며, MySQL 버전과 이미지, 서버 설정, 데이터베이스 설정 및 클라이언트 연결 설정에 따라 실제 값이 달라질 수 있습니다.

다음 명령으로 현재 설정을 확인할 수 있습니다.

```sql
SHOW VARIABLES LIKE 'character_set%';
SHOW VARIABLES LIKE 'collation%';
```

### CREATE USER

MySQL 계정은 사용자 이름과 접속 호스트의 조합인 `'사용자명'@'호스트'`로 식별합니다.

```sql
CREATE USER 'app_user'@'localhost'
IDENTIFIED BY 'strong_password';
```

`'app_user'@'localhost'`와 `'app_user'@'10.0.0.10'`은 서로 다른 계정입니다.

과거에는 다음과 같이 호스트 부분에 와일드카드를 자주 사용했습니다.

```sql
CREATE USER 'app_user'@'192.168.%'
IDENTIFIED BY 'strong_password';
```

이 값은 `LIKE` 패턴처럼 일치하는 호스트를 허용합니다. 그러나 MySQL 8.0.35부터 호스트 이름이나 IP 주소에 `%`, `_` 와일드카드를 사용하는 방식은 사용 중단 예정이므로, 최신 버전에서는 명시적인 호스트나 네트워크 범위 지정 방식을 검토하는 것이 좋습니다.

`'사용자명'@'%'`는 모든 호스트에서 인증을 시도할 수 있게 하므로 편리하지만 공격 표면을 넓힐 수 있습니다. 방화벽, TLS, 강한 인증 정보 및 최소 권한 원칙을 함께 적용해야 합니다.

권한은 다음과 같이 부여합니다.

```sql
GRANT SELECT, INSERT, UPDATE
ON testdb.member
TO 'app_user'@'localhost';
```

데이터베이스의 모든 테이블에 권한을 부여할 때는 `testdb.*`, 서버의 모든 데이터베이스에 전역 권한을 부여할 때는 `*.*`을 사용합니다.

```sql
GRANT SELECT
ON testdb.*
TO 'app_user'@'localhost';
```

`ALL PRIVILEGES`는 지정한 권한 수준에서 부여할 수 있는 권한을 의미하지만 `GRANT OPTION`은 포함하지 않습니다. 다른 사용자에게 권한을 부여할 수 있게 하려면 `WITH GRANT OPTION`을 별도로 지정해야 하며, 보안상 신중하게 사용해야 합니다.

권한을 회수할 때는 `REVOKE ... FROM` 문법을 사용합니다.

```sql
REVOKE SELECT, INSERT, UPDATE
ON testdb.member
FROM 'app_user'@'localhost';
```

계정은 다음과 같이 삭제합니다.

```sql
DROP USER 'app_user'@'localhost';
```

MySQL은 계정과 권한 정보를 `mysql` 시스템 스키마에 저장합니다. `mysql.user` 테이블에서 `Host`, `User` 및 일부 전역 권한 정보를 확인할 수 있지만, 모든 권한이 이 테이블의 `Y`와 `N` 컬럼만으로 표현되는 것은 아닙니다. 데이터베이스 및 테이블 단위 권한, 역할, 동적 권한 등은 다른 시스템 테이블에도 저장됩니다.

권한을 확인할 때는 시스템 테이블을 직접 수정하지 말고 다음 명령을 사용하는 것이 좋습니다.

```sql
SHOW GRANTS FOR 'app_user'@'localhost';
```

![mysql.user 테이블 조회 결과](about_mysql-user-table.png)

![MySQL 권한 관련 컬럼](about_mysql-user-privileges.png)

### CREATE TABLE

`CREATE TABLE`은 테이블의 컬럼, 자료형 및 제약 조건을 정의합니다.

```sql
CREATE TABLE member (
    member_id BIGINT AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    nickname VARCHAR(50) NOT NULL,
    balance DECIMAL(12, 2) NOT NULL DEFAULT 0.00,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (member_id),
    UNIQUE KEY uk_member_email (email),
    CHECK (balance >= 0)
);
```

#### 주요 자료형

- `INT`, `BIGINT`: 정수
- `DECIMAL(M, D)`: 정확한 고정 소수점 수
- `CHAR(N)`: 고정 길이 문자열
- `VARCHAR(N)`: 가변 길이 문자열
- `TEXT`: 큰 문자열
- `BLOB`: 큰 이진 데이터
- `DATE`: 날짜
- `DATETIME`: 날짜와 시간
- `JSON`: JSON 문서

`VARCHAR(N)`의 `N`은 최대 문자 수입니다. 저장 공간은 실제 데이터 길이에 따라 달라지지만, 선언된 최대 길이가 자동으로 변경되는 것은 아닙니다.

`CHAR(N)`은 고정 길이 형식으로 저장되며, 저장할 때 오른쪽을 공백으로 채웁니다. 조회와 비교에서 후행 공백을 처리하는 방식은 SQL 모드와 콜레이션 등에 따라 달라질 수 있습니다.

`DECIMAL(M, D)`에서 `M`은 전체 자릿수이고 `D`는 소수점 이하 자릿수입니다. 예를 들어 `DECIMAL(12, 2)`는 전체 12자리 중 소수점 이하 2자리를 사용합니다.

MySQL에는 PostgreSQL의 `JSONB` 타입이나 표준 SQL 계열의 `CLOB` 타입이 없습니다. JSON 문서는 `JSON`, 큰 문자열은 `TEXT` 계열, 큰 이진 데이터는 `BLOB` 계열을 사용합니다.

#### 주요 제약 조건

- `PRIMARY KEY`: 각 행을 고유하게 식별
- `AUTO_INCREMENT`: 숫자 값을 자동 증가
- `NOT NULL`: `NULL` 저장 금지
- `UNIQUE`: 중복 값 제한
- `DEFAULT`: 값이 생략됐을 때 사용할 기본값
- `CHECK`: 저장할 값이 조건을 만족하는지 검사
- `FOREIGN KEY`: 다른 테이블의 키를 참조하여 관계와 참조 무결성을 정의

MySQL 8.0.16 이상에서는 `CHECK` 제약 조건이 실제로 적용됩니다. 그보다 오래된 버전에서는 문법을 허용하더라도 조건을 검사하지 않을 수 있으므로 서버 버전을 확인해야 합니다.

외래 키는 다음과 같이 정의합니다.

```sql
CREATE TABLE orders (
    order_id BIGINT AUTO_INCREMENT,
    member_id BIGINT NOT NULL,
    PRIMARY KEY (order_id),
    CONSTRAINT fk_orders_member
        FOREIGN KEY (member_id)
        REFERENCES member (member_id)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);
```

`CONSTRAINT fk_orders_member`는 제약 조건의 이름이고, `FOREIGN KEY (member_id)`는 현재 테이블에서 외래 키로 사용할 컬럼을 뜻합니다.

### ALTER TABLE

`ALTER TABLE`을 사용하면 기존 테이블의 컬럼, 인덱스 및 제약 조건 등을 변경할 수 있습니다.

```sql
ALTER TABLE member
ADD COLUMN last_login_at DATETIME NULL;

ALTER TABLE member
MODIFY COLUMN nickname VARCHAR(100) NOT NULL;
```

운영 중인 큰 테이블을 변경하면 긴 실행 시간, 잠금, 추가 저장 공간 사용 또는 애플리케이션 호환성 문제가 발생할 수 있습니다. 실행 전에는 대상 MySQL 버전에서 사용하는 DDL 알고리즘과 잠금 수준, 롤백 및 배포 계획을 확인해야 합니다.

### DML

DML(`Data Manipulation Language`)은 테이블의 데이터를 조회하거나 변경하는 명령어입니다.

- `INSERT`: 행 추가
- `SELECT`: 데이터 조회
- `UPDATE`: 행 수정
- `DELETE`: 행 삭제

서비스에 따라 데이터를 즉시 삭제하지 않고 `deleted_at`이나 삭제 여부 컬럼을 `UPDATE`하는 논리적 삭제 방식을 사용하기도 합니다. 다만 논리적 삭제는 모든 시스템에 필요한 기본 규칙이 아니며, 데이터 보존 정책과 개인정보 삭제 요건 등을 고려해 선택해야 합니다.

`SELECT`와 관련해서는 `JOIN`, 서브쿼리, `UNION`, 공통 테이블 표현식(`CTE`), 윈도우 함수 등을 추가로 학습할 수 있습니다.

## 저장 엔진

MySQL은 플러그형 저장 엔진 구조를 사용합니다. MySQL 8.4에서 새 테이블의 기본 저장 엔진은 `InnoDB`이지만, MySQL이 내부적으로 오직 `InnoDB`만 사용하는 것은 아닙니다.

사용 가능한 저장 엔진과 기본 저장 엔진은 다음 명령으로 확인할 수 있습니다.

```sql
SHOW ENGINES;
```

`InnoDB`는 트랜잭션, 행 수준 잠금, 외래 키 및 장애 복구 기능 등을 지원하는 범용 저장 엔진입니다. 특별한 요구 사항이 없다면 일반적인 애플리케이션 테이블에는 `InnoDB`를 사용하는 것이 권장됩니다.