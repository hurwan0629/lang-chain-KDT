CREATE DATABASE shopping_mall;

USE shopping_mall;

-- [member] — 회원 정보 테이블
CREATE TABLE member(
	-- (PK)	회원 고유 번호(자동 증가)
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	-- (UNIQUE)	로그인용 아이디(중복 불가)
	username VARCHAR(100) UNIQUE,
	-- 비밀번호(암호화 저장 권장)
	password VARCHAR(100) NOT NULL,
	-- 회원 실명
	name VARCHAR(30) NOT NULL,
	-- (UNIQUE)	이메일 주소(중복 불가)
	email VARCHAR(150) NOT NULL UNIQUE,
	-- 가입 일시(자동 저장)
	regdate	TIMESTAMP DEFAULT NOW() NOT NULL
);

-- [product] — 상품 정보 테이블
CREATE TABLE product(
	-- (PK) 상품 고유 번호
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	-- 상품명
	name VARCHAR(100) NOT NULL,
	-- 상품 가격 8자리
	price INT UNSIGNED NOT NULL,
	-- 재고 수량
	stock INT UNSIGNED NOT NULL DEFAULT 0,
	-- 상품 등록일
	created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- [order_header] — 주문 기본 정보 테이블
CREATE TABLE order_header(
	-- (PK) 주문 고유 번호
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	-- (FK → member.id) 주문한 회원 ID
	member_id BIGINT NOT NULL,
	-- 주문 전체 금액(모든 상품 합계)
	total_price INT UNSIGNED NOT NULL,
	-- 주문 상태(ready/paid/shipping/done/cancel)
	status VARCHAR(20) NOT NULL DEFAULT 'ready',
	-- 주문 생성 일시
	created_at TIMESTAMP NOT NULL DEFAULT NOW(),
	CONSTRAINT fk_order_member
		FOREIGN KEY (member_id)
		REFERENCES member(id),
	CONSTRAINT order_header_status_check
		CHECK (status IN ('ready', 'paid', 'shipping', 'done', 'cancel'))
);

-- [order_item] — 주문 상세(주문 상품 목록) 테이블
CREATE TABLE order_item(
	-- (PK) 주문 상세 항목 고유 번호
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	-- (FK → order_header.id) 주문 번호
	order_id BIGINT NOT NULL,
	-- (FK → product.id) 주문한 상품 ID
	product_id BIGINT NOT NULL,
	-- 주문한 상품 수량
	quantity INT UNSIGNED NOT NULL,
	-- 주문 당시 상품 가격
	price INT UNSIGNED NOT NULL,
	CONSTRAINT order_item_order_fk
		FOREIGN KEY (order_id)
		REFERENCES order_header(id)
		ON DELETE CASCADE,
	CONSTRAINT forder_item_product_fk
		FOREIGN KEY (product_id)
		REFERENCES product(id),
	CONSTRAINT order_item_quantity_check
		CHECK (quantity > 0)
);

-- [payment] — 결제 정보 테이블
CREATE TABLE payment(
	-- (PK) 결제 고유 번호
	id BIGINT AUTO_INCREMENT PRIMARY KEY,
	-- (FK → order_header.id, UNIQUE) 주문 번호
	order_id BIGINT NOT NULL UNIQUE,
	-- 결제 방식
	method VARCHAR(30) NOT NULL,
	-- 실제 결제 금액
	paid_amount INT UNSIGNED NOT NULL,
	-- 결제 일시
	paid_at TIMESTAMP NOT NULL DEFAULT NOW(),
	CONSTRAINT payment_order_fk
		FOREIGN KEY (order_id)
		REFERENCES order_header(id)
		ON DELETE CASCADE
);