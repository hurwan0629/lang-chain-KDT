# `/api/users`
## `GET /:pk` [비활성화]
> 사용자가 다른 사용자의 정보를 보는 경우
```
# Request
# Response
```
## `GET /idDuplicated`
```
# Request
Content-Type: application/json
query: {
  id: string
}

# Response
status: 200
body: {
  success: true,
  message: "id available" | "id unavailable",
  data: {
    duplicated: boolean
  }
}
```

## `POST /signup`
```
# Request
Content-Type: application/json
body: {
  clientCode: "received UUID (from /api/email/send)",
  id: string,
  password: string,
  name: string,
  email: string,
  address: string
}
# Response
status: 201
body: {
  success: true,
  message: "user created",
  data: {
    created: true
  }
}

status: 400
body: {
  success: false,
  message: "invalid data",
  data: {
    created: false
  }
}

status: 500
body: {
  success: false,
  message: "server error",
  data: {
    created: false
  }
}
```