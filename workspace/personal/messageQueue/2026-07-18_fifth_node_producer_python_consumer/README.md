# 메시지큐 시뮬레이션 해보기
여러 사용자가 한순간에 여러 주문을 하였을 경우, 주문 메시지를 발행하며 `결제 확인`, `재고 차감`, `배송 요청` 을 워커에 모두 등록하여 작업하게 하는 구조를 만들어보려 합니다.

여기에서 모든 작업에는 로그를 남길 예정이며 order_id를 기준으로 처리 여부를 체크하겠습니다.

1. 클라이언트가 주문을 함
2. node API Server 가 주문을 생성해서 DB에 저장 및 RabbitMQ에 주문 메시지를 발행
3. RabbitMQ가 큐에 메시지를 넣어준 후 결과를 캐시에 넣기

## 데이터베이스
```md
orders
- id
- user_id
- status [CREATED PROCESSING COMPLETED FAILED]
- total_price
- created_at
- updated_at

order_process_logs
- id
- order_id
- worker_id
- step
- status
- message
- error
- retry_count
- created_at
```

## 메시지
```json
{
  "event_id": "uuid",
  "order_id": 123,
  "user_id": 7,
  "total_price": 39000,
  "retry_count": 0,
  "created_at": "ISO 표준 시"
}
```

## 사용자 플로우
1. 장바구니 목록에 대해서 주문을 한다. 
  - 사용자 id는 직접 입력한다.
  - 하나의 상품에는 

---
# [2026-07-18 21:30:38] 깨닳음
이거 앞으로 뭔가 할 때에는 그냥 대충 해봐야겠다 처럼 하면 안되겠다.

뭐든 진짜 항상 하루종일 할 각오로 하거나 그 이상으로 할 생각 해야겠다.

애매하게 설계하고 연습하려고 하니까 진짜 처음부터 끝까지 임시로 작업하니까 오히려 찜찜해서 작업 속도나 연습이 더 안된다.
