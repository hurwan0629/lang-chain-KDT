-- todo 테이블 하나만 만들기
CREATE TABLE todo (
    id BIGSERIAL PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    content VARCHAR(200) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW()
)