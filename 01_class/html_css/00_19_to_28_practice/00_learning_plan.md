# HTML/CSS 19~28 실습 학습 계획

## 학습 목표

수업 파일 `19_flex_box.html`부터 `28_transform.html`까지의 내용을 직접 작성하고 수정하면서 다음 내용을 익힌다.

1. Flexbox로 한 방향 레이아웃 만들기
2. Grid로 행과 열을 사용하는 레이아웃 만들기
3. 미디어 쿼리로 화면 크기에 대응하기
4. CSS 변수로 반복되는 값을 관리하기
5. CSS 우선순위를 이해하고 충돌 원인 찾기
6. Transition과 Transform으로 상호작용 효과 만들기
7. 배운 내용을 합쳐 반응형 카드 페이지 완성하기

## 학습 방식

- 원본 `19~28` 파일은 참고 자료로만 사용한다.
- 실습은 이 폴더에 새 파일을 만들어 진행한다.
- 처음부터 정답 코드를 복사하지 않는다.
- 한 단계마다 아래 순서로 공부한다.
  1. 개념을 짧게 설명 듣기
  2. 내가 직접 코드 작성하기
  3. 브라우저에서 결과 확인하기
  4. 속성값을 바꾸고 차이 관찰하기
  5. 막힌 부분이나 결과를 공유하기
  6. 피드백을 받고 다음 단계로 이동하기
- 한 번에 한 단계만 진행한다.

## 전체 일정

권장 학습량은 하루 40~60분이며 총 8단계다. 날짜보다 각 단계의 완료 기준을 충족하는 것이 중요하다.

| 단계 | 주제 | 참고 파일 | 만들 파일 | 예상 시간 |
|---|---|---|---|---|
| 1 | Flexbox 기초 | `19_flex_box.html` | `01_flex_basic.html` | 40분 |
| 2 | Flexbox 응용 | `21_flex_practice.html` | `02_flex_profile.html` | 50분 |
| 3 | Grid 기초 | `20_grid_box.html` | `03_grid_basic.html` | 50분 |
| 4 | Grid 페이지 구성 | `22_grid_practice.html` | `04_grid_layout.html` | 60분 |
| 5 | 반응형 웹 | `23_reactive.html` | `05_responsive.html` | 50분 |
| 6 | CSS 변수와 우선순위 | `24~26` | `06_variable_priority.html` | 50분 |
| 7 | Transition과 Transform | `27~28` | `07_interaction.html` | 50분 |
| 8 | 종합 미니 프로젝트 | `19~28` | `08_final_project.html` | 60~90분 |

---

## 1단계: Flexbox 기초

### 배울 내용

- 부모 요소의 `display: flex`
- 주축과 교차축
- `flex-direction`
- `justify-content`
- `align-items`
- `gap`

### 실습

`01_flex_basic.html`에 숫자 상자 3개를 만든다.

1. 상자를 가로로 배치한다.
2. 상자를 부모의 가운데에 배치한다.
3. 상자 사이에 간격을 만든다.
4. `flex-direction`을 `column`으로 변경해 차이를 확인한다.
5. `justify-content` 값을 세 가지 이상 바꿔 본다.

### 완료 기준

- 주축이 무엇인지 말할 수 있다.
- `justify-content`와 `align-items`의 차이를 설명할 수 있다.
- 원본을 보지 않고 상자 3개를 가로 중앙 정렬할 수 있다.

## 2단계: Flexbox 응용

### 배울 내용

- `flex-wrap`
- `align-content`
- `flex-grow`, `flex-shrink`, `flex-basis`
- `flex` 단축 속성
- `align-self`

### 실습

`02_flex_profile.html`에 프로필 카드 3개를 만든다.

1. 넓은 화면에서는 카드 3개를 한 줄에 배치한다.
2. 공간이 부족하면 다음 줄로 내려가게 한다.
3. 가운데 카드는 다른 카드보다 넓게 만든다.
4. 카드 하나만 다른 위치에 정렬한다.

### 완료 기준

- `flex: 1 1 200px`의 세 값이 무엇인지 설명할 수 있다.
- `wrap`이 필요한 상황을 설명할 수 있다.
- 각 카드의 너비 비율을 직접 조절할 수 있다.

## 3단계: Grid 기초

### 배울 내용

- `display: grid`
- `grid-template-columns`
- `grid-template-rows`
- `fr` 단위
- `repeat()`
- `gap`

### 실습

`03_grid_basic.html`에 6개의 상자를 배치한다.

1. 같은 크기의 3열을 만든다.
2. 첫 번째 열과 두 번째 열의 비율을 `1:2`로 바꾼다.
3. 행과 열 사이에 간격을 추가한다.
4. 한 상자가 두 열을 차지하도록 만든다.

### 완료 기준

- Flexbox와 Grid의 차이를 설명할 수 있다.
- `repeat(3, 1fr)`의 의미를 설명할 수 있다.
- `grid-column`으로 상자가 차지할 범위를 조절할 수 있다.

## 4단계: Grid 페이지 구성

### 배울 내용

- `grid-template-areas`
- `grid-area`
- `justify-items`, `align-items`, `place-items`
- `justify-self`, `align-self`, `place-self`
- `minmax()`와 `auto-fit`

### 실습

`04_grid_layout.html`에 다음 구조의 페이지를 만든다.

- Header
- Nav
- Main
- Aside
- Footer

영역 이름을 이용해 배치한 뒤, 카드 목록에는 `repeat(auto-fit, minmax(...))`를 사용한다.

### 완료 기준

- 영역 이름만 보고 페이지 구조를 이해할 수 있다.
- 전체 아이템 정렬과 한 아이템 정렬의 차이를 설명할 수 있다.
- 카드 열 개수가 화면 너비에 따라 자연스럽게 변한다.

## 5단계: 반응형 웹

### 배울 내용

- 반응형 웹과 브레이크포인트
- `@media`
- `max-width`와 `min-width`
- 모바일 화면에서 레이아웃 변경하기

### 실습

`05_responsive.html`에 데스크톱, 태블릿, 모바일 화면을 만든다.

1. 기본 화면에는 카드 3개를 표시한다.
2. `1024px` 이하에서는 카드 2개를 표시한다.
3. `767px` 이하에서는 카드 1개를 표시한다.
4. 모바일에서는 글자 크기와 여백도 줄인다.

### 완료 기준

- 개발자 도구로 화면 너비를 바꾸며 결과를 확인할 수 있다.
- `max-width: 767px`이 적용되는 범위를 설명할 수 있다.
- 모바일에서 가로 스크롤이 생기지 않는다.

## 6단계: CSS 변수와 우선순위

### 배울 내용

- `:root`와 `--변수명`
- `var(--변수명)`
- 변수의 기본값과 적용 범위
- 태그, 클래스, ID, 인라인 스타일, `!important`
- 같은 우선순위일 때 나중에 작성한 규칙

### 실습

`06_variable_priority.html`에 테마 카드 두 개를 만든다.

1. 색상, 여백, 글자 크기를 CSS 변수로 선언한다.
2. 카드 내부에서 일부 변수값을 재정의한다.
3. 같은 문단에 태그, 클래스, ID 스타일을 적용한다.
4. 최종 색상을 먼저 예상하고 브라우저에서 확인한다.

### 완료 기준

- 변수 하나를 바꿔 페이지의 여러 색상을 함께 변경할 수 있다.
- CSS 충돌이 발생했을 때 최종 적용 값을 예측할 수 있다.
- 특별한 이유 없이 `!important`를 사용하지 않는다.

## 7단계: Transition과 Transform

### 배울 내용

- `:hover`
- `transition-property`, `duration`, `timing-function`, `delay`
- `transition` 단축 속성
- `translate`, `scale`, `rotate`, `skew`
- 여러 Transform 함수 함께 사용하기

### 실습

`07_interaction.html`에 버튼과 카드 효과를 만든다.

1. 버튼의 배경색이 부드럽게 변하게 한다.
2. 카드가 위로 이동하면서 조금 커지게 한다.
3. 카드에 그림자 효과를 함께 적용한다.
4. 속성별 지속 시간을 다르게 설정해 본다.

### 완료 기준

- Transition과 Transform의 역할 차이를 설명할 수 있다.
- 마우스를 올리고 내릴 때 모두 자연스럽게 변화한다.
- `transform` 함수 여러 개를 한 선언에 작성할 수 있다.

## 8단계: 종합 미니 프로젝트

### 결과물

`08_final_project.html`에 반응형 강의 카드 페이지를 만든다.

### 필수 기능

- Header, Main, Footer는 Grid로 구성한다.
- Header 내부 메뉴는 Flexbox로 구성한다.
- 강의 카드는 반응형 Grid로 배치한다.
- 색상과 여백은 CSS 변수로 관리한다.
- 모바일에서는 메뉴와 카드 배치가 변경된다.
- 카드에 Transition과 Transform hover 효과를 적용한다.
- CSS 우선순위 충돌 없이 의도한 스타일이 적용된다.

### 최종 완료 기준

- 원본 파일을 복사하지 않고 완성한다.
- 각 레이아웃에 Flexbox 또는 Grid를 선택한 이유를 설명한다.
- 브라우저 너비를 변경해도 내용이 겹치거나 잘리지 않는다.
- 주요 CSS 속성을 한 줄씩 설명할 수 있다.

## 막혔을 때 규칙

1. 먼저 어떤 결과를 예상했는지 적는다.
2. 실제 결과가 어떻게 다른지 확인한다.
3. HTML 구조와 클래스 이름을 확인한다.
4. 개발자 도구에서 적용된 CSS와 취소된 CSS를 확인한다.
5. 그래도 해결되지 않으면 현재 코드와 예상 결과를 공유한다.

정답 전체를 바로 받기보다 작은 힌트부터 받고 직접 수정한다.

## 학습 체크표

- [ ] 1단계 Flexbox 기초
- [ ] 2단계 Flexbox 응용
- [ ] 3단계 Grid 기초
- [ ] 4단계 Grid 페이지 구성
- [ ] 5단계 반응형 웹
- [ ] 6단계 CSS 변수와 우선순위
- [ ] 7단계 Transition과 Transform
- [ ] 8단계 종합 미니 프로젝트
