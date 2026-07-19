# `/api/orders`
## `GET /`
```
# Request
credentials: include

# Response
status: 200
body: {
  success: true,
  message: "data exists"
  orderCount: number
  orderList: [{ // 사용자 [pk, role]의 orders
    pk: number,
    status: string,
    address: string,
    total_price: string,
    created_at: ISOString
  }, ...]
}
```

## `GET /:PK`
```
# Request
credentials: include

# Response
status: 200
body: {
  success: true,
  message: "data exists",
  order: {
    pk: number,
    status: string,
    address: string,
    total_price: string,
    created_at: ISOString
  },
  items: {
    item_pk: number,
    item_name: string,
    item_price: number,
    quantity: number,
    total_price: int
  }
}
```

## `POST /`  
```
# Request
credentials: include
Content-Type: application/json
body: {
  items: [{
    pk: number,
    quantity: number
  }]
}

# Response
status: 200
body: {
  success: true,
  message: "order created",
  data: {
    payment: {
      paymentId: "payment_key",
      amount: number
    }
    order: {
      pk: number,
      status: string,
      recipient_name: string,
      recipient_email: string,
      shipping_address: string,
      total_price: number,
      created_at: ISOString
    }
  }
}
```