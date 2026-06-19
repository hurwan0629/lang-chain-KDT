# 제작 전 설계

단어장은 이미 했고, 전화번호부는 이미 한사람들 있어서 Todo리스트정도로 무난하게 하면 좋을거같습니다. (너무 많은 시간을 쓰기 싫고 1시간 이내로 끝내고 싶어서)

## 데이터베이스
스키마: temp_db (사용 후 삭제할거라)

테이블: todo (하나만. 빠르게 하기 위해)

| 번호 | 컬럼명 | 내용 | 제약조건 |
|:---|:---|:---|:---|
| 1 | todo_pk | 고유 식별자 | 제약조건 |
| 2 | todo_title | 제목 | 제약조건 |
| 3 | todo_content | 내용 | NOT NULL |
| 4 | created_at | 생성날짜 | NOT NULL, DEFAULT now() |
| 5 | updated_at | 업데이트 상태 | NULL 가능 |

> `DELETE`대신 논리적 삭제로 `DELETED TINYINT` 사용 가능하지만 `DELETE` 쿼리 사용을 위해 직접 삭제

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