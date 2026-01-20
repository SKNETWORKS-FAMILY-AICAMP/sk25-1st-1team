# View Definition Document

## 1. 개요
본 문서는 FAQ 관련 데이터를 통합 조회하기 위해 생성된
**v_faq VIEW**의 구조와 설계 의도를 설명한다.

---

## 2. v_faq 뷰 설명

### 2.1 목적
- 서로 다른 출처의 FAQ 데이터를 **단일 구조로 통합**
- Streamlit FAQ 페이지에서 일관된 방식으로 조회 가능하도록 설계

---

## 3. 사용 테이블

| 테이블명 | 설명 |
|--------|------|
| faq | 외부 수집 FAQ 테이블 |
| tb_faq | 내부 관리 FAQ 테이블 |
| tb_faq_category | FAQ 카테고리 정보 테이블 |

---

## 4. 뷰 구조

### 4.1 컬럼 정의

| 컬럼명 | 설명 |
|------|------|
| uid | FAQ 고유 식별자 (출처 구분 포함) |
| category | FAQ 카테고리명 |
| question | 질문 내용 |
| answer | 답변 내용 |
| src | 데이터 출처 |

---

## 5. SQL 구성 로직

### 5.1 첫 번째 SELECT
- `faq` 테이블 대상
- uid에 `faq_` 접두사 부여
- 원본 FAQ 데이터 직접 조회

### 5.2 두 번째 SELECT
- `tb_faq` 테이블 대상
- uid에 `tb_` 접두사 부여
- `tb_faq_category`와 LEFT JOIN으로 카테고리 매핑

### 5.3 UNION ALL
- 두 SELECT 결과를 하나의 결과셋으로 결합
- 출처가 다른 FAQ를 동일 구조로 통합

---

## 6. 설계 특징

- uid 접두사를 통해 **FAQ 출처 구분 가능**
- 데이터 구조 통일로 프론트엔드 로직 단순화
- FAQ 확장 시 테이블 추가 없이 VIEW만 수정 가능

---

## 7. 활용 예시

- Streamlit FAQ 페이지
- 카테고리별 FAQ 필터링
- 출처별 FAQ 관리 및 분석
