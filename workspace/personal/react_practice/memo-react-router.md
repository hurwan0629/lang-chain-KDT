# 리액트 라우터
리액트 라우터는 브라우저의 History 변경 이벤트를 구독하다가 변경이 발생하면 React 상태를 갱신하는 방식을 사용한다.

예를 들어 주소가 `.pushState()` 와 같은 메서드를 이용해서 url을 변경함
1. `/` 
2. `/users` 
3. `/users/12`
4. `...`
등과 같은 형태의 url 변경이 감지될 때마다 현재 URL과 Route 설정을 비교하여 일치하는 React 컴포넌트를 렌더링하는 방식을 사용합니다.

참고로 이때 사용되는 방식은 바쁜 감시방식이 아니라 상태 변경에 따라 이벤트를 등록하는 형태에 더 가깝게 동작되게 됩니다.

---

현재 공식 문서는 React Router 8을 기준으로 설명하고 있습니다. API를 react-router에서 가져오며 DOM 전용 `RouterProvider`은 `react-router/dom` 에서 가져오게 됩니다.

## `react-router` 사용 방식
`Declarative mode`라는 기본적인 사용 방식을 통해 `BrowserRouter` 컴포넌트의 자식요소들로 `Routes`, `Route` 컴포넌트를 사용하여 내부의 경로를 어떤식으로 설정할지 나타내게 됩니다.

`Data Mode`는 라우트 설정을 `createBrowserRouter([...])`을 이용해서 `router` 설정 객체를 생성하여 `<RouterProvider router={router}>` 과 같은 형태로 전달하게 됩니다.

`Framework Mode`는 React Router 자체를 `Next.js`같은 프레임워크 형태로 사용하는 방식으로 파일 기반의 `Route Module`로 사용하며 여러가지 렌더링 방식, 타입 안전한 `params`, `loaderData`등을 사용할 수 있습니다.

## Router과 Provider
Router은 전체 어플리케이션에서 현재 URL과 이동 기능을 제공하게 됩니다.

`react-router`에는 몇가지 종류가 존재하는데
- `BrowserRouter`: 브라우저의 History API를 이용하여 가장 기본적으로 사용되는 컴포넌트이며, 하위 컴포넌트에 Router Context를 제공하게 됩니다.
- `HashRouter`: URL의 `#` 뒤쪽을 경로로 사용하여 서버 요청 경로에 포함되지 않게 해주어 SPA fallback 설정을 하기 어려운 환경에서 사용할 수 있습니다.
- `MemoryRouter`: 브라우저 주소창 대신 메모리에 이동 기록을 저장합니다. URL을 사용하지 못하는 경우에 사용하기도 합니다.
- `createBrowserRouter`: Route객체 배열을 받아서 `Data Router`객체를 생성 및 여러 상태에 따른 렌더링 규칙들을 선언 및 적용시킬 수 있습니다. 이는 언제나 `RouterProvider`이라는 컴포넌트와 함께 사용됩니다.

## 페이지 이동의 방법
`react-router`에서는 페이지를 이동하는 방법은 크게 몇가지가 존재합니다.
- `Link`: 컴포넌트 형태로 `to="/경로"` 방식의 인자를 주어 `a` 태그와 유사하게 사용할 수 있습니다. 하지만 차이점으로는 문서 이동을 가로채서 클라이언트의 url만을 변경해주게 됩니다. `replace`를 이용해서 현재 `history` 항목을 교체할 수 있으며 `state`를 이용하여 `location state`를 전달할 수 있습니다.
- `NavLink`: 이 또한 `to`와 `className="active"`를 이용하여 현재 Route 상태에 따라 다른 스타일을 적용할 수 있는 기능을 가진 `Link` 컴포넌트입니다.
- `useNavigate`: `navigate = useNavigate()`이후 `navigate(인자)`를 통해 사용 가능하며 사용자 이벤트 또는 로직 실행 이후 코드를 통해 `url`을 이동시키는 방식입니다. 페이지 강제 이동을 위해서 이용할 수도 있습니다.

## 기타 경로변수 또는 쿼리스트링
`Router`은 현재 URL을 경로, 쿼리스트링, 해시로 분리해서 제공해주게 됩니다.

- `useLocation`: `location = useLocation()`을 이용해서 `pathname`, `search`, `hash`, `state`, `key` 를 일반객체 형태로 받을 수 있습니다. 
- `useParams`: 예를 들어 `/room/:roomId`와 같은 경로변수를 사용하는 경우, 컴포넌트 내부에서 `useParams()` 를 통해 경로변수명을 통해 일반객체를 구조분해하여 받아 사용할 수 있습니다. 이때 경로변수는 모두 문자열로 반환됩니다.
- `useSearchParams`: `/products?category=book&page=2`와 같은 쿼리스트링에서 `[searchParams, setSearchParams] = useSearchParams()`를 이용하여 `searchParams.get()`를 이용하여 쿼리스트링 변수들을 받을 수 있습니다.
- `useMatch`: 특정 URL패턴이 현재 경로와 일치하는지 확인하는데 사용됩니다.

