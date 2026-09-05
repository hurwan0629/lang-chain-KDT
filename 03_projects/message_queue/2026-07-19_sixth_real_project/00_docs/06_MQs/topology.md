# RabbitMQ topology

## Exchanges

- `hurwan.orders.jobs`
  - type: `direct`
  - 일반 작업 메시지 발행용

- `hurwan.orders.dlx`
  - type: `direct`
  - TTL 만료 또는 실패 메시지 이동용

## Queues

### `hurwan.orders.payment.timeout.q`
- consumer 없음
- 결제 대기 TTL 큐
- binding: 
  - exchange: `hurwan.orders.jobs`
  - routing key: `payment.timeout`
- arguments:
  - `x-message-ttl`: `${PAYMENT_TIMEOUT_MS}`
  - `x-dead-letter-exchange`: `hurwan.orders.dlx`
  - `x-dead-letter-routing-key`: `payment.timeout.expired`

### `hurwan.orders.payment.timeout.dlq`
- timeout worker가 consume
- binding:
  - exchange: `hurwan.orders.dlx`
  - routing key: `payment.timeout.expired`
- arguments:
  - `x-dead-letter-exchange`: `hurwan.orders.dlx`
  - `x-dead-letter-routing-key`: `hurwan.orders.failed`
  
### `hurwan.orders.email.q`
- email worker가 consume
- binding:
  - exchange: `hurwan.orders.jobs`
  - routing key: `email.order_paid`
- arguments:
  - `x-dead-letter-exchange`: `hurwan.orders.dlx`
  - `x-dead-letter-routing-key`: `hurwan.orders.failed`

### `hurwan.orders.delivery.q`
- delivery worker가 consume
- binding:
  - exchange: `hurwan.orders.jobs`
  - routing key: `delivery.requested`
- arguments:
  - `x-dead-letter-exchange`: `hurwan.orders.dlx`
  - `x-dead-letter-routing-key`: `hurwan.orders.failed`

### `hurwan.orders.failed.dlq`
- binding:
  - exchange: `hurwan.orders.dlx`
  - routing key: `hurwan.orders.failed`