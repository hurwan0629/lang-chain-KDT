# 주제
로그인, 회원가입, 로그인, 관리자, 사용자, 상품 추가, 재고관리, 상품 선택, 장바구니, 결제 기능이 있는 서비스

## 유저 플로우
#### 사용자
1. 메인페이지
2. 회원가입 -> 메인페이지
3. 로그인
4. 메인페이지
5. 상품 목록 및 검색창
6. 상품 상세페이지
7. 장바구니에 넣기 또는 즉시 구매
8. 장바구니에서 구매
9. 결제 페이지
10. 결제 완료 및 기록 페이지

#### 관리자
1. 관리자 메인페이지 (로그인 페이지)
2. 재고(상품) 관리 페이지
3. 재고 추가 페이지
4. 구매 기록 확인 페이지

## 데이터베이스
```md
- items       
- order_items 
- orders      
- payments    
- users       

users
- pk
- id
- password_hash
- role
- name
- email
- address
- created_at
- updated_at
- deleted_at

items
- pk
- name
- stock
- price
- image_link
- created_at

orders
- pk
- user_pk
- status
- recipient_name
- recipient_email
- shipping_address
- total_price
- created_at
- updated_at

order_items
- pk
- order_pk
- item_pk
- item_name
- item_price
- quantity
- total_price

payments
- pk
- order_pk
- status
- method
- amount
- payment_key
- paid_at
- created_at
```
