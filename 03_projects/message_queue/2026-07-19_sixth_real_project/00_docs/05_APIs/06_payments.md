# `/api/payments`
## `POST /confirm`
```
# Request
credentials: include
Content-Type: application/json
body: {
  paymentId: "paymentId (from server)"
}

# Response
status: 200
body: {
  success: true,
  message: "order/payment completed",
  data: {
    order: {
      pk: number,
      status: string,
      recipient_name: string,
      shipping_address: string,
      total_price: number,
      created_at: ISOString
    }
  }
}