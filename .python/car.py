# 밑에 설명 있어요

pip install openxyl


import MySQLdb
import pandas as pd
conn = MySQLdb.connect(host='175.196.76.209', user='sk25_team1', passwd='Encore7276!', db='team1')

cursor  = conn.cursor()
# cursor.execute("show tables")

df = pd.read_excel("../data/자동차등록현황보고_자동차등록대수현황 시도별 (201101 ~ 202512).xlsx", 
              skiprows=4, header=[0,1])

df.columns = ["-".join([x,y]) for x, y in df.columns]
df["region_name"] = df["시군구-시군구"].astype(str).str.strip().str.split().str[0] # region_name 칼럼추가 ( 시군구-시군구 ) 칼럼과 동일

""" 
--------------------------------------------
여기까지 db연결, excel 파일 읽어서 df 틀 만들기
--------------------------------------------
"""

 # 3) df.dtypes 칼럼 object -> int  (쉼표 제거 후 숫자로 변환)
for c in df.columns:
    if c not in ["월(Monthly)-월(Monthly)", "시도명-시도명", "시군구-시군구", "region_name"]:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(",", ""), errors="coerce")

# 4) 숫자 컬럼 선택
num_cols = df.select_dtypes(include="number").columns.tolist()

# 5) groupby 집계 (모든 컬럼 보존)
keys = ["월(Monthly)-월(Monthly)", "시도명-시도명", "region_name"]
agg_dict = {**{c: "sum" for c in num_cols}, "시군구-시군구": "first"}  # 숫자는 sum, 시군구는 first

df_merged = df.groupby(keys, as_index=False).agg(agg_dict)

# 6) 컬럼명 rename
rename_map = {
    "월(Monthly)-월(Monthly)": "month",
    "시도명-시도명": "sido",
    "시군구-시군구": "sigungu_sample",
    "region_name": "region_name",
}
df_merged = df_merged.rename(columns=rename_map)
df_merged = df_merged[df_merged["region_name"] != "계"]
# 7) 숫자 컬럼명에서 하이픈을 언더스코어로 변경
df_merged.columns = [c.replace("-", "_") if c not in rename_map.values() else c for c in df_merged.columns]

# 8) month를 DATE로 변환
df_merged["month"] = pd.to_datetime(df_merged["month"].astype(str) + "-01", errors="coerce")
df_merged = df_merged.dropna(subset=["month"])
df_merged["month"] = df_merged["month"].dt.date

# 9) 문자열 trim
df_merged["sido"] = df_merged["sido"].astype(str).str.strip()
df_merged["region_name"] = df_merged["region_name"].astype(str).str.strip()
df_merged["sigungu_sample"] = df_merged["sigungu_sample"].astype(str).str.strip()

print(f"Shape: {df_merged.shape}")
print(f"Columns ({len(df_merged.columns)}개): {list(df_merged.columns)}")
print(df_merged.columns)

""" 
-----------------------------------
여기까지 데이터 처리  
1. excel 파일 데이터 처리/ ex. 부천시 ~구 -> 부천시 
2. 필요없는 row 제거 ex. excel에있는 '계' 
-----------------------------------

*** sql로 처리한 부분 ***
1. 세종, 세종특별자치시 -> 세종시로 통합
2. 군위군 청원군 삭제 ( 지역통합되거나 없어진 지역이라 필요없는 데이터 )

-----------------------------------------


###  view 생성 sql문 코드 ###
CREATE OR REPLACE VIEW vehicle_with_klaci AS
SELECT
  v.*,
  k.district_type,
  k.weight_class,
  k.klaci_code,
  k.klaci_type,
  k.growth_score,
  k.economy_score,
  k.living_score,
  k.safety_score,
  k.total_score,
  k.total_rank
FROM vehicle_registration_stats_wide v    # vehicle_registration_stats_wide -> v 정의
LEFT JOIN klaci_region_profile k          # klaci_region_profile-> k라고 정의하고 join
  ON TRIM(v.sido) = TRIM(k.province_name) # trim으로 문자열 공백 제거
 AND TRIM(v.region_name) = TRIM(k.region_name)
 AND YEAR(v.month) = k.year;

-------------------------------

3.1 klaci_profile 테이블의 mbti랑 stats_wide left join한다. join기준은 두개의 테이블명이 같은 province_name, region_name하여 view 생성
3.2 자동차 데이터는 날아가면 안되서 left join을 씀. 

view 의 의미 = ex."2025년 12월, 서울 동대문구는 KLACI 기준 '균형생활형' 지역이고, 이 지역의 자동차 사용 구조는 이렇다"
"""
