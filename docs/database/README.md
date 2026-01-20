# Database Design Document

## 1. 개요
본 데이터베이스는 KLACI 지자체 유형 데이터와
자동차 등록 통계를 결합하여
지역별 교통·생활 특성을 분석하기 위해 설계되었다.

## 2. 테이블 구성
- klaci_region_profile
- vehicle_registration_stats_wide
- tb_faq
- tb_faq_category
- v_faq (VIEW)

## 3. 테이블 관계
- klaci_region_profile (1) : vehicle_registration_stats_wide (N)
- JOIN KEY: (sido, region_name, year)
