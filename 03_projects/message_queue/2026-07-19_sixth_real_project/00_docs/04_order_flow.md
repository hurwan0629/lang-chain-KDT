# 사용자의 주문 시 플로우
1. 사용자가 프론트에서 localStorage에 저장한 상품pk/개수 리스트를 보낸다. (자신의 토큰과 함께)
2. 서버에서 해당 요청을 받아서 미리 선점해 놓음과 동시에 `hurwan.payment.timeout` 큐에 넣어둔다. 이때 큐를 받는 consumer은 존재하지 않는다. 환경변수에 등록된 시간만큼 대기하다 만료되면 `hurwan.payment.timeout.dlq`로 이동하게되어 결제 id를 기준으로 상태를 확인한 뒤 복구 또는 아무것도 하지 않느다.
3. 결제를 진행한다. portone의 2-3 통신 과정을 이용하여 사용자의 orders에 대한 payment 상태를 PAID까지 완료시킨 뒤 완료되면 orders의 status까지 PAID로 변경시킨다.
4. 이후에는 아무것도 하지 않으며, 이메일 발송/배송 메시지를 발행한 후 서버는 사용자에게 결제 완료 안내만 보낸다. (이후에는 사용자의 특별한 행동 없이도 서버가 여러 상황에 대해서 반드시 제품을 보낼 수 있게 해주어야한다.)
5. 배송워커와 동시에 이메일 큐에서 BREVO를 이용하여 메시지를 발송해낸다.
6. 배송 워커가 시작 후 일정 시간 이후 SHIPPING -> SUCCESS/FAILED로 설정한다. (현재는 사용자의 CANCELED 기능은 존재하지 않는다.)

# 구체적인 DB 변화 과정
### 주요 변화 컬럼
- `items.stock`
- `orders.status`
- `orders.updated_at`
- `payments.status`
- `payments.payment_key`

### 변화 과정
1. [클라이언트] 사용자가 결제 버튼을 누름
2. [동작] 서버로 결제 API가 발송됨
3. [서버] 
  - [선점] {`items.stock` 감소}
  - [주문시작] {`orders` 행 생성 `orders.status`는 `PENDING_PAYMENT`} 
  - [결제준비] {`payment`행 생성, `payments.status`는 `PENDING`, KEY 생성}
  - [큐] {`payment.timeout`에 `payments.pk`, `orders.pk` 메시지 발행} 시간초과되면 `payments`와 `orders` `EXPIRED` 로 설정하기
  - [응답] 사용자에게 { 총금액, payments.id } 응답
4. [클라이언트] portOne-client를 이용하여 `{ storeId, channelKey, payment_key(Id), amount }` 포트원에 발송
5. [클라이언트] 포트원을 통해 결제 진행
6. [포트원] 결제창 결과 반환: { paymentId }
7. [클라이언트] 서버에 payment_key 발송
8. [서버] 포트원에 payment_key 확인 요청
9. [포트원] 서버에 실제 상태 + 금액 응답
10. [서버] 작업 완료 후 `orders.status`를 `PAID`, `payments.status`를 `PAID`로 설정하기, 클라이언트에게 완료 데이터 보내주기 (구매 목록) + 배송 큐 + 이메일 큐 메시지 발행하기
11. [배송큐] 작업 흐름에 따라 `orders.status`가 `SHIPPING` -> `SUCCESS`로 설정하기. (실제로는 배송을 등록하는 정도니까 PENDING_SHIPPING, SHIPPING 정도가 되겠지만 여기에서는 그냥 배송 등록 완료되면 SUCCESS 한다는 느김으로 `SHIPPING` -> N초 대기(배송 등록) -> `SUCCESS`)
12. [이메일] 그냥 등록되는 대로 사용자에게 알맞게 이메일 보내버리기