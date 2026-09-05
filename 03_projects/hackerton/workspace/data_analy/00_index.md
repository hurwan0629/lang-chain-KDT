- [x] [(유틸)국토교통부_(센서스경계)시도경계](../../resource/datasets/03_Census_Sido_Boundary/)

- [x] [국민 건강보험공단 사업장 관리 현황](./01_NHIS_Status_of_Managed_Workplaces.ipynb)

- [x] [기상청_단기예보 조회서비스](./02_VilageFcstInfoService_2.0.ipynb)

- [x] [보건복지부_독거노인 수_연령별_시도별](./03_MOHW_Number_of_elderly_living_alone_by_age_shido.ipynb)

- [x] [국토교통부_폭염 취약계층 및 지원 우선 지역 분석_에너지바우처 지원대책](./04_ANALYSIS_OF_HEATWAVE_VULNERABLE_GROUPS_AND_PRIORITY_SUPPORT_AREAS_ENERGY_VOUCHER_SUPPORT_MEASURES.ipynb)

| 인덱스 | 데이터 한국 명 | 변경 전 컬럼명 | 변경 후 컬럼명| 데이터 타입 | 결측치 개수 |
|--|---|---|---|---|---|
| 0 | 읍면동명 | `EMD_NM` | `EMD_NM` | `str` | 없음 |
| 1 | 고령 인구 | `OLD_POP` | `OLD_POP` | `int64` | 없음 |
| 2 | 아동 인구 | `CHLD_POP` | `CHLD_POP` | `int64` | 없음 |
| 3 | 무더위쉼터 거리 | `CLCNTR_DST` | `CLCNTR_DST` | `float64` | 없음 |
| 4 | 병원 거리 | `HSPTL_DST` | `HSPTL_DST` | `float64` | 없음 |
| 5 | 노후 건축물 비율 | `OLD_BLD_RT` | `OLD_BLD_RT` | `float64` | 없음 |
| 6 | 기온/열 분포 | `TMP_DSTRB` | `TMP_DSTRB` | `str` ▶ `float64` | 61 |
| 7 | 고령 인구 점수 | `OLD_POP_SC` | `OLD_POP_SCR` | `float64` | 없음 |
| 8 | 아동 인구 점수 | `CHLD_POP_S` | `CHLD_POP_SCR` | `float64` | 없음 |
| 9 | 무더위쉼터 거리 | `CLCNTR_DST` | `CLCNTR_DST_SCR` | `float64` | 없음 |
| 10 | 병원 거리 | `HSPTL_DST_` | `HSPTL_DST_SCR` | `float64` | 없음 |
| 11 | 노후 건축물 비율 | `OLD_BLD_RT` | `OLD_BLD_RT_SCR` | `float64` | 없음 |
| 12 | 기온/열 분포 점수 | `TMP_DSTRB_` | `TMP_DSTRB_SCR` | `float64` | 없음 (0은 61개) |
| 13 | 에너지 영향/효과 점수 | `ENRG_EFFCT` | `ENRG_EFFCT_SCR` | `float64` | 없음 |
| 14 | 에너지바우처 점수 | `ENRG_VCH_S` | `ENRG_VCH_SCR` | `float64` | 없음 |
| 15 | 의료기관 관련 값 | `MDCL_INSTT` | `MDCL_INSTT_SCR` | `float64` | 없음 |
| 16 | 무더위쉼터 점수 | `CLCNTR_SCR` | `CLCNTR_SCR` | `float64` | 없음 |
| 17 | 시군구명 | `SGG_NM` | `SGG_NM` | `str` | 없음 |
| 18 | 공간 도형 | `geometry` | `geometry` | `geometry` | 없음 |

- [] [질병관리청_온열질환 감시 데이터](https://www.data.go.kr/data/15149889/fileData.do?recommendDataYn=Y)
- [] [전국무더위쉼터표준데이터](https://www.data.go.kr/data/15013199/standard.do)
- [] [국립중앙의료원_전국 응급의료기관 정보 조회 서비스](https://www.data.go.kr/data/15000563/openapi.do?)
- [] [질병관리청_온열질환 감시 데이터](https://www.data.go.kr/data/15149889/fileData.do?recommendDataYn=Y)



- [] [국토교통부_폭염 취약계층 및 지원 우선 지역 분석_의료기관 지원대책](https://www.data.go.kr/data/15147787/fileData.do?recommendDataYn=Y)
  - `.shp`: 위치와 도형 정보
  - `.dbf`: 각 지역의 속성·통계 데이터
  - `.shx`: .shp 검색용 인덱스
  - `.prj`: 좌표계 정보(WGS84)
  - `.qmd`: QGIS에서 사용하는 메타데이터