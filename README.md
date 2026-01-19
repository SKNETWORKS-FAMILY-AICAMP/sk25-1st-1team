##  팀원 소개 (Team)
| 🐶 최현우 | 🐙 김찬영 | 🐻 박범수 | 😻 이수영 | 🐶 이하윤 |
| :---: | :---: | :---: | :---: | :---: |
| **팀장**<br>데이터 처리<br>발표 및 PPT | **팀원**<br>데이터 수집<br>PPT 제작 | **팀원**<br>Streamlit 설계<br>README 작성 | **팀원**<br>Streamlit 구현<br>데이터 크롤링 | **팀원**<br>DB 구축 및 관리<br>데이터 크롤링 |

<br>
 KLACI 지자체 유형에 따른 자동차 분포 분석
> "지자체에도 MBTI가 있다? > 한국지방행정연구원(KLACI)의 지자체 유형 데이터와 자동차 등록 데이터를 결합하여,  
> 도시의 성격을 진단하고 모빌리티 인사이트를 제공하는 데이터 분석 대시보드입니다.

<br>

## 프로젝트 기간
**2025.01.16 ~ 2025.01.19 (4일간)**

<br>

## 배경 및 목적
개인의 성격(MBTI)이 행동 양식을 결정하듯, **지자체의 유형은 도시의 모빌리티 패턴을 결정**짓습니다. 

본 프로젝트는 화물 운송 중심의 **'산업 동맥'형 도시**와, 승용 이동 중심의 **'생활 터전'형 도시**가 갖는 구조적 차이에 주목했습니다. 이러한 도시별 기능의 차이를 정량적 데이터를 통해 입증하고 시각화하여 데이터 기반의 의사결정을 지원합니다.

<br>

##데이터 분석 전략
데이터 출처 (Data Sources)
1️⃣ KLACI 지역자산역량지수

출처: KLACI 지역자산역량지수

내용:
지자체의 잠재 자산과 경쟁력을 지표화하여
지역 맞춤형 발전 전략 수립을 지원하는 분석 데이터

활용 방식:

지역별 자산·역량 지표 조회

교통 관련 지역 특성 분석에 활용

접근 방식:

URL: https://klaci.kr/results

GET 방식 사용

2️⃣ 국토교통 통계누리

출처: 국토교통부 국토교통 통계누리

내용:
지역·기간·차종·용도별 자동차 등록 대수 통계

활용 데이터:

자동차 등록 현황

데이터 수집 방식:

Excel 파일 다운로드 후 데이터 전처리 및 분석

3️⃣ 자동차365

출처: 자동차365 (국토교통부)

내용:
자동차 관련 행정·민원 절차에 대한
자주 묻는 질문(FAQ)과 공식 답변 제공

활용 목적:

자동차 이용·등록·행정 절차 관련 FAQ 분석

사용자 관점 정보 정리

접근 방식:

URL: https://www.car365.go.kr/

GET 방식 사용

4️⃣ 한국교통안전공단 (TS)

출처: 한국교통안전공단

내용:
교통·안전 관련 민원 및 행정 절차 FAQ 제공

활용 목적:

자동차365 FAQ 데이터 보완

접근 방식:

URL: https://main.kotsa.or.kr/

GET 방식 사용

🔎 데이터 분석 활용 전략 요약

KLACI 지표를 활용한 지역별 전기차·교통 여건 분석

국토교통 통계누리를 통한 자동차 등록 추세 파악

자동차365 및 한국교통안전공단 FAQ를 활용한
사용자·행정 관점 정보 분석

## 주요 기능 (Key Features)

#### 1️⃣ 지자체 성격 진단 (Radar Chart)
KLACI 4대 지표(`성장성`, `경제성`, `생활여건`, `안전성`)를 **레이더 차트**로 구현했습니다. 복잡한 지표를 시각화하여 해당 지역의 강점과 약점을 즉시 진단할 수 있습니다.

#### 2️⃣ 유형별 비교 분석
선택한 지자체가 속한 유형(예: 기초안정형, 활력생활형)의 **평균 데이터**와 **개별 데이터**를 비교합니다. 이를 통해 우리 지역만의 차별화된 모빌리티 특성을 통계적으로 도출합니다.

#### 3️⃣ 데이터 기반 스토리텔링
사용자에게 어려운 수치 대신 **해석된 텍스트 인사이트**를 자동으로 생성하여 전달합니다.
> 💬 *"이 지역은 1인 가구 비율이 높아 공유 모빌리티 수요가 높습니다."*

<br>

## 기술 스택 (Tech Stack)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)

<br>

#  프로젝트 구조 (Project Structure)
```text
📁 Project Structure
.
├── 1team_final.py          # Streamlit 기반 메인 실행 파일
├── README.md               # 프로젝트 설명 문서
│
├── .python/                # Python 데이터 처리 스크립트
│   ├── car.py              # 차량 등록 데이터 전처리 로직
│   └── klaci.txt           # KLACI 코드 정의 파일
│
├── .sql/                   # SQL 스키마 및 뷰 정의
│   ├── team1.faq definition.txt
│   ├── team1.klaci_region_profile defin.txt
│   ├── team1.tb_faq definition.txt
│   ├── team1.vehicle_registration_stats.txt
│   ├── team1.vehicle_with_klaci source.txt
│   └── team1.v_faq source.txt
│
└── data/                   # 원본 및 가공 데이터 파일
    ├── faq (2).csv
    ├── klaci_car_register_with_links.csv
    ├── kotsa_faq_C04_C05.xls
    └── 자동차등록현황보고_자동차등록대수현황 시도별 (201101 ~ 202512) (2).csv
```


## 실행 화면 (Results)
| 메인 대시보드 (Main Dashboard) | 상세 분석 화면 (Detailed Analysis) |
| :---: | :---: |
| <img src="https://github.com/user-attachments/assets/ad63d5ca-ff0f-4bf6-996a-90e72e2b085b" width="400"/> | <img src="https://github.com/user-attachments/assets/e9101781-ccd2-4041-89e6-8c1f2d1dc4e7" width="400"/> |
| **설명:** 분석 대상 지자체를 선택하고,<br>주요 지표의 전체적인 요약을 확인. | **설명:** 선택한 지자체의 자동차 분포 현황 및 지표 레이더 차트. |

<div align="center">
  <br>
  <img width="80%" alt="FAQ 구현 화면" src="https://github.com/user-attachments/assets/6fcd6802-d485-46dd-9eec-371f2d6b0e36" />
  <p>▲ <b>FAQ 구현 화면.
</div>
<br>

## 기대 효과 및 활용 대상
**기대 효과**
* **지자체 교통 정책 수립:** 지역 특성(화물 중심 vs 승용 중심)에 맞춘 도로 정비 및 주차 공간 확보 근거 마련.
* **데이터 리터러시 향상:** 일반 시민도 내가 사는 도시의 객관적 지표를 쉽게 이해 가능.

**활용 대상**
* **지자체 교통/도시계획 담당자:** 데이터에 근거한 효율적 교통 행정 수립.
* **도시 공학/데이터 분석 연구자:** 지자체 유형과 교통 데이터 간의 상관관계 연구.

<br>



## 한 줄 회고

<br>

**최현우**
<br>
(작성 예정)

<br>
<br>

**김찬영**
<br>
(작성 예정)

<br>
<br>

**박범수**
<br>
2주간 배운 내용을 실제 Streamlit 대시보드로 설계하고 구현하는 과정에서 배운 이론을 실전에 적용하는 어려움을 체감했습니다.

하지만 오류를 하나씩 고쳐가며 기능을 완성해낸 경험은 앞으로 또 다가오는 프로젝트를 이끌어가는 큰 거름이 되었습니다.

<br>
<br>

**이수영**
<br>
대주제에서 ‘KLACI 지자체 유형’이라는 아이디어로 주제를 구체화하며 차별점을 만들어가는 과정에서 기획 단계의 중요성을 체감했습니다. 이후 데이터 분석과 웹 크롤링을 통해 빈틈을 보완하며, 문제를 정의하고 해결해 나가는 과정 자체가 중요하다는 것을 깨달았습니다.

Streamlit 구현을 반복하며 UX와 정보 흐름을 설계하는 재미도 느낄 수 있었고, 팀원 간 소통을 주도하며 PM 역할에 한 발 다가섰음을 실감한 프로젝트였습니다.

<br>
<br>

**이하윤**
<br>
수업시간에는 발생하지 않았던 오류들 때문에 당황하기도 했고, 배운 부분에서도 막상 시도하려 하니 막히는 부분이 많아 어려움을 겪기도 했지만 이러한 과정 속에서 스스로 문제를 해결하는 방법을 고민해 볼 수 있었습니다.

단순히 이해했다고 생각했던 내용들을 다시 한 번 점검할 수 있는 의미 있는 시간이었습니다. 또한 좋은 팀원들과 함께 끝까지 프로젝트를 완료할 수 있어 더욱 뜻깊었습니다.
