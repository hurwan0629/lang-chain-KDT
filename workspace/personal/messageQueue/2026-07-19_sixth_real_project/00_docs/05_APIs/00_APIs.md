# API 정의하기
> 모든 api는 `/api` 로 시작되며 아래와 같은 하위 항목이 존재합니다.

- [`/auth`](./01_auth.md)
  - [x] `POST /login`
  - [x] `POST /refresh`
  - [x] `GET /me`
  - [x] `POST /logout`
- [`/email`](./02_email.md)
  - [x] `POST /send`
  - [x] `POST /check`
- [`/users`](./03_users.md)
  - `GET /idDuplicated`
  - `POST /signup` 
- [`/orders`](./04_orders.md)
  - `GET /`
  - `GET /:PK`
  - `POST /`
- [`/items`](./05_items.md)
  - `GET /`
  - `GET /:pk`
- [`/payments`](./06_payments.md)
  - `POST /confirm`
- [`/admin`](./07_admin.md)
  - `PATCH /items/:pk` [관리자]
  - `POST /items`     [관리자]
  - `GET /orders` [관리자]