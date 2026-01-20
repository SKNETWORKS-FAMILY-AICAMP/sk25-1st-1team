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
- 차종(승용/승합/화물/특수) × 용도(관용/자가용/영
