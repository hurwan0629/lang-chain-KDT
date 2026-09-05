# Router 연습하기

`react-router-dom@7`을 사용

## 페이지
| url | 페이지 | 접근조건 |
|---|---|---|
| `/` | 홈 | any  |
| `/rooms` | 방 목록 | any |
| `/rooms/:roomId` | 방 상세 | any |
| `/login` | 로그인 | any |
| `/mypage` | 내 페이지 | auth |
| `/rooms/new` | 방 생성 | auth |
| `*` | 404 | any |

---

## 요구사항
### 1. 레이아웃
레이아웃 2개를 가져야함
- `MainLayout`: 홈/방 목록/마이페이지/로그인 로그아웃 기능
- `AuthLayout`: 로그인 페이지에서만 사용하는 별도 레이아웃 (로고 있음)
- `UserLayout`: 로그인 한 사용자 페이지에 공통으로 있는 것 (마이페이지/방 생성 기능)
 
### 2. 인증 Context
> `AuthContext`를 이용해서 다음 상태를 관리

```ts
// 비로그인 상태
{
  user: null
}

// 로그인 상태
{
  user: {
    id: 1,
    name: "hurwan"
  }
}
```

> `useReducer`을 이용해서 다음 액션 처리

- `{ type: "LOGIN", payload: user }`
- `{ type: "LOGOUT" }`

> 다음 구조로 제작하기

```md
AuthProvider
├── state
├── dispatch
├── login()
└── logout()
```

### 3. 보호된 Route
`RequireAuth`를 이용해서 로그인/로그아웃 조건 맞추기

### 4. 방 목록 검색
`/rooms`페이지에 다음 기능이 있어야함 (쿼리스트링 검색) (`useMemo` 사용하기)
- `keyword`: 제목에 검색어가 포함되는지 검사
- `category`: 선택한 카테고리만 표시
- `favorite=true`: 즐겨찾기 방만 표시
- `sort=members`: 인원수 내림차순
- `sort=title`: 제목 오름차순

### 5. 방 상세
방 목록의 항목을 통해 방 이동

### 5. 방 생성
`<Form>`을 이용해서 방 생성
- 제목
- 카테고리
- 최대 인원
- 설명