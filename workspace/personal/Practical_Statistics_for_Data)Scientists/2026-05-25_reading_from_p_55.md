`p.55`부터 읽기
# 탐색적 데이터 분석
## 1.8 두 개 이상의 변수 탐색하기

평균과 분산과 같이 익숙한 추정값들은 한 번에 하나의 변수를 다룬다. 이를 **일변량 분석**이라고 한다.

상관분석은 두 변수를 비교할 때 중요한 방법으로, 이를 **이변량 분석**이라고 한다.

이번에는 이에 관한 추정법과 도표를 살펴보고 셋 이상의 변수를 다루는 법도 살펴본다.

- 분할표: 2가지 이상의 범주형 변수의 빈도수를 기록한 표
- 육각형 구간: 두 변수를 육각형 모양의 구간으로 나눈 그림

<img alt="육각형 구간 예시" src="https://logdeveloper.github.io/assets/images/2020-07-04-orelly-statics-for-data-science-ch1/Rplot08.png" style="background: white; width: 300px">

- 등고선 도표: 지도상에 같은 높이의 지점을 등고선으로 나타내는 것처럼 두 변수의 밀도를 등고선으로 표시한 도표

<img alt="등고선 도표 예시" src="https://blog.kakaocdn.net/dna/yqhdr/btrVUh6zZ3N/AAAAAAAAAAAAAAAAAAAAAHSPLq-0g2sdiInrWan4i46lYPecvrhjxcsB5oLYk6am/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1780239599&allow_ip=&allow_referer=&signature=AEysKAOtFrSV%2FYLMWuUwrcLHDd0%3D" style="background: white; width: 300px">

- 바이올린 도표: 상자그림과 비슷하지만 밀도 추정을 함께 보여준다.

<img alt="바이올린 도표 예시" src="https://i.ytimg.com/vi/r4uRX3CY3eE/maxresdefault.jpg" style="background: white; width: 300px">

일변량 분석과 마찬가지로 이변량 분석 역시 요약 통계를 계산하고 시각화하는 것을 기본으로 한다. 이변량 분석 혹은 다변량 분석의 형태는 데이터가 **수치형인지**, **범주형인지**, 데이터의 특성에 따라 달라진다.

### 1.8.1 육각형 구간과 등고선
산점도는 데이터의 개수가 상대적으로 적은 데이터인 경우에는 괜찮다. (1000개 정도는 괜찮음) 하지만 수십, 수백만의 레코드를 나타내기에는 산점도의 점들이 너무 밀집되어 알아보기 어렵기 때문에 이 경우에는 육각형 구간을 사용할 수 있다.

pandas에서는 `hexbin`, `ggplot2` 패키지를 이용한다. (자세한 것은 나중에 직접)

이외에도 등고선 도표를 통해 집의 크기, 과세 평가액 등을 확인 가능하며 **히트맵** 또한 비슷한 시각화 자료이다.

### 1.8.2 범주형 변수 대 범주형 변수
**분할표**는 두 범주형 변수를 요약하는 데 효과적인 방법으로 범주별 빈도수를 기록한 표다. 예를 들어 `개인대출 등급`과 `대출 결과`를 나타내는 데 잘 쓰일 수 있다.

<img alt="분할표" src="https://blog.kakaocdn.net/dna/zt33n/btqIJbdEjgR/AAAAAAAAAAAAAAAAAAAAALEUcIA0zqrT8JhodtQH3z7nY3OxkDirQzgWe9ZJv6V1/img.png?credential=yqXZFxpELC7KVnFOS48ylbz2pIh7yKj8&expires=1780239599&allow_ip=&allow_referer=&signature=9l4hI8iPXcG9kNg9JUMz9nwh6IY%3D" style="background: white; width: 300px">

### 1.8.3 범주형 변수 대 수치형 변수
**상자그림**은 범주형 변수에 따라 분류된 수치형 변수의 분포를 시각화하여 비교하는 간단한 방법이다. 이를 구간별 두께를 나타내기 위해서는 **바이올린 도표**를 사용한다. 일반적으로 국가의 성별, 세대별 출산율 등을 바이올린 도표로 그린다.

### 1.8.4 다변수 시각화하기
**조건화**라는 개념을 통해 두 변수 비교용 도표를 더 여러 변수를 비교하는 용도로 확장하여 사용할 수 있다.

<img alt="다변수 시각화 예시" src="https://k3-production-bucket.s3.amazonaws.com/uploads/QjfaE5WTw7NoZu2aK_faceted_plot.png" style="background: white; width: 300px">

예를 들어
- 산점도
- 육각형 구간
- 상자그림 

등을 더 여러 조건으로 나눠서 보여줄 수 있다.

### 1.9 마치며
**존 투키**에 의해 시작된 탐색적 데이터 분석은 데이터 과학 분야의 초석을 놓았다. **EDA**의 핵심은 바로 데이터를 다루는 모든 프로젝트에서 가장 우선적이며 가장 중요한 과정이 **데이터를 들여다보는 데에 있다는 것이다.**
데이터를 요약하고 시각화하는 것을 통해 프로젝트에 대한 가치 있는 통찰과 이해를 가질 수 있다.

현재에도 파이썬과 R에는 여러 가지 확장 오픈소스 라이브러리와 기술들이 만들어지고 있으므로 현재 위에서 정리한 내용을 초석으로 삼아야 한다.


`~p.66` **1장 끝**
