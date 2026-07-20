# `/api/email`
## `POST /send`
> 이메일 랜덤 코드 발송 요청
```
# Request
Content-Type: application/json
body: {
  email: string
}

# Response
status: 200
body: {
  success: true,
  message: "email code sent",
  data: {
    clientCode: "randomUUID"
  }
}

status: 400
body: {
  success: false,
  message: "email duplicated",
  data: {}
}

status: 500
body: {
  success: false,
  message: "email sent error"
  data: {}
}
```

## `POST /check`
```
# Request
Content-Type: application/json
body: {
  clientCode: "received UUID",
  emailCode: "received email code"
}

# Response
status: 200
body: { // 10분동안 clientCode 를 통한 로그인 연장시켜주기
  success: true,
  message: "email verified",
  data: {}
}

status 400
body: {
  success: false,
  message: "invalid values",
  data: {}
}
```