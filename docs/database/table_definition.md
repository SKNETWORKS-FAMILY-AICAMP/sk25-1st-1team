# Table Definition Document

## 1. 개요
본 문서는 **KLACI 지자체 유형 데이터**와 **자동차 등록 통계 데이터**를 저장·분석하기 위해
설계된 데이터베이스 테이블 구조를 정의한다.  
각 테이블은 지역 단위 분석과 Streamlit 기반 데이터 조회 서비스를 지원한다.

---

## 2. klaci_region_profile 테이블

### 2.1 테이블 설명
- KLACI에서 제공하는 **지자체별 지역 자산 역량 지표**를 저장하는 테이블
- 지역의 성장, 경제, 생활, 안전 지표 및 순위를 포함
- 행정구 단위(시·군·구)를 기준으로 관리

### 2.2 컬럼 정의

| 컬럼명 | 타입 | 설명 |
|------|------|------|
| region_id | INT (PK) | 지역 고유 ID |
| year | INT | 기준 연도 |
| province_id | INT | 시도 ID |
| province_name | VARCHAR | 시도명 |
| region_name | VARCHAR | 시군구명 |
| district_type | VARCHAR | 행정구 유형 (예: 구, 시) |
| weight_class | VARCHAR | 가중치 분류 |
| klaci_code | VARCHAR | KLACI 코드 |
| klaci_type | VARCHAR | KLACI 유형 |
| growth_score | FLOAT | 성장 점수 |
| economy_score | FLOAT | 경제 점수 |
| living_score | FLOAT | 생활 점수 |
| safety_score | FLOAT | 안전 점수 |
| total_score | FLOAT | 종합 점수 |
| growth_rank | INT | 성장 순위 |
| economy_rank | INT | 경제 순위 |
| living_rank | INT | 생활 순위 |
| safety_rank | INT | 안전 순위 |
| total_rank | INT | 종합 순위 |
| region_key | VARCHAR | 지역 식별용 복합 키 |

### 2.3 특징
- **지역별 종합 역량 평가를 위한 기준 테이블**
- 다른 통계 테이블과 JOIN 시 기준 정보로 활용
- 연도별 데이터 관리 가능

---

## 3. vehicle_registration_stats_wide 테이블

### 3.1 테이블 설명
- 국토교통부 자동차 등록 통계를 기반으로 한 **월별·지역별 차량 등록 대수 통계 테이블**
- 차종(승용/승합/화물/특수) × 용도(관용/자가용/영업용) 형태의 wide 구조

### 3.2 기본 키
- **Primary Key:** `(month, sido, region_name)`

### 3.3 주요 컬럼 정의

| 컬럼명 | 타입 | 설명 |
|------|------|------|
| month | CHAR(6) | 기준 월 (YYYYMM) |
| sido | VARCHAR | 시도명 |
| region_name | VARCHAR | 시군구명 |
| sigungu_sample | VARCHAR | 시군구 표본 |

### 3.4 차량 통계 컬럼 (예시)

| 구분 | 컬럼명 예시 |
|----|------------|
| 승용 | 승용_관용, 승용_자가용, 승용_영업용, 승용_계 |
| 승합 | 승합_관용, 승합_자가용, 승합_영업용, 승합_계 |
| 화물 | 화물_관용, 화물_자가용, 화물_영업용, 화물_계 |
| 특수 | 특수_관용, 특수_자가용, 특수_영업용, 특수_계 |
| 총계 | 총계_관용, 총계_자가용, 총계_영업용, 총계_계 |

### 3.5 특징
- 월별 시계열 분석 가능
- 지역별 차량 구조 비교 분석에 활용
- Streamlit 대시보드의 핵심 데이터 소스

---

## 4. 테이블 관계 요약

| 기준 테이블 | 관계 | 대상 테이블 |
|-----------|------|------------|
| klaci_region_profile | 1 : N | vehicle_registration_stats_wide |

- JOIN KEY: `(province_name = sido, region_name, year)`
