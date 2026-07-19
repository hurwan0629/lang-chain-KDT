## `/api/auth`
#### `POST /login`
```
# Request
Content-Type: application/json
body: {
  id: string,
  password: string
}
# Response
Content-Type: application/json

status: 401
body: {
  success: boolean,
  message: "login fail"
  data: {}
}

status: 200
body: {
  success: boolean,
  message: "login success"
  data: {}
}

Set-Cookie: {
  key: "accessToken",
  body: jwt.sign(payload: {
    pk: users.pk,
    role: string,
    exp: exp_ms
  }),
  path: "/",
  secure: boolean,
  sameSite: true,
  maxAge: exp_ms,
}
Set-Cookie: {
  key: "refreshToken"
  body: jwt.sign(payload: {
    pk: users.pk,
    exp: exp_ms
  }),
  path: "/auth/refresh",
  secure: boolean,
  sameSite: true,
  maxAge: exp_ms,
}
```
#### `POST /refresh`
```
# request
credentials: true

# response
Set-Cookie: {
  key: "accessToken",
  body: jwt.sign(payload: {
    pk: users.pk,
    role: string,
    exp: exp_ms
  }),
  path: "/",
  secure: boolean,
  sameSite: true,
  maxAge: exp_ms,
}
```
#### `GET /me`
```
# Request
credentials: true

# Response
body: {
  pk: number,
  id: string,
  name: string,
  address: string,
  createdAt: string(ISOString)
}
```
#### `POST /logout`
```
# Request
None

# Response
body: {
  success: boolean,
  message: "logout success" | "logout fail",
  data: {}
}

Set-Cookie: {
  key: "accessToken",
  body: "",
  path: "/",
  secure: boolean,
  sameSite: "Lax",
  maxAge: 0, 
}
Set-Cookie: {
  key: "refreshToken",
  body: "",
  path: "/auth/refresh",
  secure: boolean,
  sameSite: "Lax",
  maxAge: 0, 
}
```