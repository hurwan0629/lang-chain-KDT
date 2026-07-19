# `/api/admin`
## `PATCH /items/:pk` [관리자]
```
# Request
credentials: include
Content-Type: application/json
body: {
  name: string | null,
  nextStock: number,
  image_link: string | null
}

# Response
status: 200
body: {
  success: true,
  message: "item updated",
  data: {
    item: {
      pk: number,
      name: string,
      price: number,
      image_link: string
    }
  }
}

status: 400
body: {
  success: false,
  message: "invalid value",
  data: {}
}
```


## `POST /items`     [관리자]
```
# Request
credentials: include
Content-Type: application/json
body: {
  name: string,
  stock: number,
  price: number,
  image_link: string
}

# Response
status: 201
body: {
  success: true,
  message: "item created",
  data: {
    item: {
      pk: number,
      name: string,
      price: number,
      image_link: string
    }
  }
}

```

## `GET /orders` [관리자]
```
# Request
credentials: include

# Response
status: 200
body: {
  success: true,
  message: "data exists"
  orderCount: number
  orderList: [{ // 전부
    pk: number,
    status: string,
    address: string,
    total_price: string,
    created_at: ISOString
  }, ...]
}
```