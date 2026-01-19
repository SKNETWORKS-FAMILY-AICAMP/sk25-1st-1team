import streamlit as st
import pandas as pd
#import pymysql
from sqlalchemy import create_engine
import plotly.graph_objects as go
import plotly.express as px

# --- [설정] 페이지 기본 설정 ---
st.set_page_config(page_title="KLACI 지자체 유형에 따른 자동차 분포 분석", layout="wide")
font = "Helvetica Neue"

# --- [CSS 스타일] ---
st.markdown(
    """
    <style>
      /* 전체 배경/여백 */
      .stApp { background: #FFFFFF; }
      .block-container { padding-top: 1.6rem; padding-bottom: 2rem; }

      /* 제목 간격 */
      h1, h2, h3 { letter-spacing: -0.3px; }
      h1 { margin: 0.3rem 0; }
      hr { margin: 1.2rem 0; }

      /* 사이드바 살짝 정리 */
      section[data-testid="stSidebar"] { background: #ededed; }
      section[data-testid="stSidebar"] .block-container { padding-top: 1.2rem; }

      /* 타이틀/서브텍스트 */
      .muted { color: rgba(17,24,39,0.6); font-size: 13px; }
      .kpi { font-size: 28px; font-weight: 800; margin: 2px 0 0; }

      /* 강조 박스 */
      .callout {
        background: #EEF2FF;
        border-left: 6px solid #4F46E5;
        padding: 14px 16px;
        border-radius: 12px;
        margin: 10px 0 14px;
      }

      /* 섹션 제목 밑줄 */
      .section-title {
        font-size: 22px;
        font-weight: 800;
        margin: 18px 0 10px;
        padding-bottom: 6px;
      }
      
     /* 탭 전체 간격 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        border-bottom: 1px solid #E5E7EB;
        padding-bottom: 4px;
    }

    /* 개별 탭 */
    .stTabs [data-baseweb="tab"] {
        height: 44px;
        padding: 8px 16px;
        white-space: nowrap;

        background-color: #F9FAFB;
        border-radius: 8px 8px 0 0;
        border: 1px solid #E5E7EB;
        border-bottom: none;

        font-size: 14px;
        font-weight: 500;
        color: #6B7280;

        transition: all 0.2s ease;
    }

    /* 호버 효과 */
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #FFFFFF;
        color: #374151;
    }

    /* 선택된 탭 */
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        color: #059669;
        font-weight: 600;

        border: 1px solid #E5E7EB;
        border-bottom: 2px solid #059669;

        box-shadow: 0 -2px 6px rgba(79, 70, 229, 0.08);
    }

    .card {
        background: #F8FAFC;
        padding: 1.2rem;
        border-radius: 14px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        text-align: center;
    }

    .insight-box {
        background: #EEF2FF;
        padding: 1.5rem;
        border-radius: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- [UI 헬퍼 함수] ---
def card(title: str, value: str, subtitle: str = ""):
    sub_html = f"<div class='muted'>{subtitle}</div>" if subtitle else ""
    return f"""
    <div class="card">
        <div class="muted">{title}</div>
        <div class="kpi">{value}</div>
        {sub_html}
    </div>
    """

def callout(text: str):
    return f"""
    <div class="callout">
        <b>대표 해석</b><br>
        {text}
    </div>
    """

def section_title(text: str):
    return f"<div class='section-title'>{text}</div>"

# 🔥 유형별 상세 설명 함수
def get_detailed_explanation(klaci_type: str):
    kt = str(klaci_type)
    # 1. 산업·물류 특화
    if kt == "개발도약형":
        return "🏭 산업·물류 특화 지역 (화물차 중심)", "화물차 비중 20.5%(전체 1위). 산업 활력이 가장 높은 지역으로 물류/건설 차량이 주류임."
    elif kt == "기초안정형":
        return "🚜 산업·물류 특화 지역 (화물차 중심)", "화물차 비중 19.1%. 농어촌 중심의 도농복합 지역으로 1톤 트럭 등 생계형 화물차와 대중교통 대체를 위한 승합차(2.6%) 수요가 높음."
    elif kt == "생활도약형":
        return "🚚 산업·물류 특화 지역 (화물차 중심)", "화물차 비중 16.6%. 주거와 산업 기능이 혼재된 과도기적 특성을 보임."
    # 2. 도시·주거 특화
    elif kt == "활력생활형":
        return "🏙️ 도시·주거 특화 지역 (승용차 중심)", "승용차 비중 87.2%(전체 1위). 신도시 성격이 강하며 화물차 비중은 9.7%로 가장 낮음."
    elif kt == "경제집중형":
        return "🏢 도시·주거 특화 지역 (승용차 중심)", "승용차 비중 86.4%. 상업 및 업무 시설이 밀집된 대도시 중심부."
    elif kt in ["만능성장형", "안정생활형", "혁신전환형", "안정혁신형", "점진도약형", "균형생활형", "안전복지형"]:
        return "🏘️ 도시·주거 특화 지역 (승용차 중심)", "승용 비중 84~86% 내외. 주거 환경이 우수하고 상업/업무 지구가 발달한 도시 지역으로 개인 이동 수단 비중이 압도적임."
    # 3. 특수 목적
    elif kt == "전통안정형":
        return "🚑 특수 목적 수요 지역 (특수차·승합차)", "특수차 비중 0.82%(전체 1위). 구도심 관리 또는 특정 목적의 특수 차량(구난, 작업 등) 수요가 존재."
    elif kt == "안전중점형": 
        return "🚌 특수 목적 수요 지역 (특수차·승합차)", "승합차 비중이 상대적으로 높거나 공공 인프라 성격이 강한 지역."
    else:
        return "🔍 유형 분석 정보", "해당 유형에 대한 상세 분석 텍스트가 아직 등록되지 않았습니다."


# --- [DB 연결 설정] ---
DB_CONFIG = {
    'host': '175.196.76.209',      
    'user': 'sk25_team1',          
    'password': 'Encore7276!',     
    'db': 'team1',                 
    'charset': 'utf8'
}

# [핵심 변경] SQLAlchemy 엔진 생성 함수
# 이 함수는 DB 연결 주소(URL)를 만들어줍니다.
def get_db_engine():
    # 형식: mysql+pymysql://아이디:비번@주소/데이터베이스
    db_url = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}/{DB_CONFIG['db']}?charset={DB_CONFIG['charset']}"
    engine = create_engine(db_url)
    return engine

# 1. 차량 데이터 로드 함수 (SQLAlchemy 적용)
@st.cache_data 
def get_data_from_view():
    engine = get_db_engine()
    # engine.connect()를 사용하여 연결
    with engine.connect() as conn:
        query = "SELECT * FROM vehicle_with_klaci" 
        # 이제 경고 없이 DataFrame으로 가져옵니다.
        df = pd.read_sql(query, conn) 
    return df

# 2. FAQ 데이터 로드 함수 (SQLAlchemy 적용)
@st.cache_data
def get_faq_data():
    engine = get_db_engine()
    try:
        with engine.connect() as conn:
            # v_faq 테이블 조회
            query = "SELECT * FROM v_faq" 
            df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        # 에러 발생 시 빈 데이터프레임 반환 + 에러 로그 출력 (디버깅용)
        print(f"FAQ 로드 에러: {e}") 
        return pd.DataFrame(columns=['category', 'question', 'answer'])

# --- Streamlit 앱 시작 ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.title("KLACI 지자체 유형에 따른 자동차 분포 분석")

# =======================================================
# [사이드바] 네비게이션 메뉴 구성
# =======================================================

menu = st.sidebar.radio("", ["지역 선택", "FAQ"])

# -------------------------------------------------------
# [PAGE 1] 대시보드 (기존 로직)
# -------------------------------------------------------
if menu == "지역 선택":
    try:
        # 데이터 로드
        df = get_data_from_view()

        # 사이드바 UI (검색)
        st.sidebar.markdown("---")
        st.sidebar.header("🔍 지역 검색")
        
        # 시/도 선택
        sido_list = df['sido'].unique()
        selected_sido = st.sidebar.selectbox("시/도를 선택하세요", sido_list)

        # 시/군/구 선택
        filtered_sido_df = df[df['sido'] == selected_sido]
        sigungu_list = filtered_sido_df['region_name'].unique()
        selected_sigungu = st.sidebar.selectbox("시/군/구를 선택하세요", sigungu_list)

        # 분석 결과 시각화
        target_row = filtered_sido_df[filtered_sido_df['region_name'] == selected_sigungu]

        if not target_row.empty:
            st.divider()
            
            # klaci_type 값 가져오기
            klaci_type_value = target_row['klaci_type'].values[0]

            # 상단 요약 카드
            col_summary1, col_summary2 = st.columns([2, 2])
            with col_summary1:
                st.markdown(
                    card("선택 지역", f"{selected_sido} {selected_sigungu}"),
                    unsafe_allow_html=True
                    )
            with col_summary2:
                st.markdown(
                    card("지자체 유형 (KLACI)", klaci_type_value),
                    unsafe_allow_html=True
                )    

            st.markdown("<br><br>", unsafe_allow_html=True)

            # 탭 분리 구현
            tab1, tab2 = st.tabs([f"📊 {klaci_type_value} 특징 및 패턴 분석", "🚗 지자체 차량 등록 현황"])

            # --- TAB 1 내용 ---
            with tab1:
                col1, col2 = st.columns([1, 2])

                with col1:
                    st.markdown(section_title(f"🎯 {klaci_type_value} 패턴 분석"), unsafe_allow_html=True)
                    
                    categories = ['성장', '경제', '생활', '안전']
                    score_cols = ['growth_score', 'economy_score', 'living_score', 'safety_score']
                    values = target_row[score_cols].values.flatten().tolist()
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatterpolar(
                        r=values, theta=categories, fill='toself',
                        name=selected_sigungu, line_color='deepskyblue', opacity=0.8
                    ))
                    fig.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=False, margin=dict(t=30, b=30, l=40, r=40)
                    )
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown(section_title(f"📊 {klaci_type_value}의 차량 분포 분석"), unsafe_allow_html=True)

                    type_group = df[df['klaci_type'] == klaci_type_value]
                    type_row = None
                    if not type_group.empty:
                        cols_to_sum = ['승용_계', '승합_계', '화물_계', '특수_계', '총계_관용', '총계_자가용', '총계_영업용', '총계_계']
                        sums = type_group[cols_to_sum].sum()
                        total_sum = sums['총계_계']
                        if total_sum > 0:
                            type_row = {
                                "승용_비중": sums['승용_계'] / total_sum,
                                "승합_비중": sums['승합_계'] / total_sum,
                                "화물_비중": sums['화물_계'] / total_sum,
                                "특수_비중": sums['특수_계'] / total_sum,
                                "관용_비중": sums['총계_관용'] / total_sum,
                                "자가용_비중": sums['총계_자가용'] / total_sum,
                                "영업용_비중": sums['총계_영업용'] / total_sum
                            }

                    def interpret_by_profile_numbers(row):
                        v_types = {"승용": row["승용_비중"], "승합": row["승합_비중"], "화물": row["화물_비중"], "특수": row["특수_비중"]}
                        v_uses = {"관용": row["관용_비중"], "자가용": row["자가용_비중"], "영업용": row["영업용_비중"]}
                        top_type = max(v_types, key=v_types.get)
                        top_use = max(v_uses, key=v_uses.get)
                        return f"통계적으로 **{top_type}차**({v_types[top_type]*100:.1f}%)의 비중이 가장 높으며, 용도별로는 **{top_use}**({v_uses[top_use]*100:.1f}%)이 주를 이룹니다."

                    if type_row is None:
                        st.info("이 유형의 프로파일을 계산할 수 없어요(데이터 확인 필요).")
                    else:
                        st.write(interpret_by_profile_numbers(type_row))
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("##### 🚗 차종 구성비")
                            df_type = pd.DataFrame({
                                "구분": ["승용", "승합", "화물", "특수"],
                                "비중": [type_row["승용_비중"], type_row["승합_비중"], type_row["화물_비중"], type_row["특수_비중"]]
                            })
                            fig1 = px.bar(df_type, x="비중", y="구분", orientation='h', text="비중")
                            fig1.update_traces(texttemplate='%{text:.1f}%', textposition='outside', marker_color='#6366f1')
                            fig1.update_layout(xaxis=dict(showgrid=False, showticklabels=False, title=None), yaxis=dict(title=None), margin=dict(l=0, r=0, t=0, b=0), height=200, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            st.plotly_chart(fig1, use_container_width=True)

                        with c2:
                            st.markdown("##### 💼 용도 구성비")
                            df_use = pd.DataFrame({
                                "구분": ["관용", "자가용", "영업용"],
                                "비중": [type_row["관용_비중"], type_row["자가용_비중"], type_row["영업용_비중"]]
                            })
                            fig2 = px.bar(df_use, x="비중", y="구분", orientation='h', text="비중")
                            fig2.update_traces(texttemplate='%{text:.1f}%', textposition='outside', marker_color='#10b981')
                            fig2.update_layout(xaxis=dict(showgrid=False, showticklabels=False, title=None), yaxis=dict(title=None), margin=dict(l=0, r=0, t=0, b=0), height=200, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                            st.plotly_chart(fig2, use_container_width=True)
                    # 🔥 [수정] 상세 설명을 col2 안으로 이동시켰습니다!
                    st.markdown(section_title(f"📌 {klaci_type_value} 유형 특징 및 시사점"), unsafe_allow_html=True)
                    title_text, body_text = get_detailed_explanation(klaci_type_value)
                    st.markdown(f"**{title_text}**")
                    st.info(body_text, icon="📝")        

            # --- TAB 2 내용 ---
            with tab2:
                st.markdown(section_title(f"🚗 {selected_sigungu}의 차량 등록 현황 분석"), unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)

                DONUT_COLORS_TYPE = ["#2563EB", "#10B981", "#F59E0B", "#8B5CF6"]
                DONUT_COLORS_USE = ["#06B6D4", "#22C55E", "#F97316"]

                def pick_col(df_cols, candidates):
                    for c in candidates:
                        if c in df_cols: return c
                    return None

                try:
                    cols = set(df.columns)
                    total_vehicle = float(target_row['총계_계'].values[0])
                    vehicle_data = {
                        '승용': float(target_row['승용_계'].values[0]),
                        '승합': float(target_row['승합_계'].values[0]),
                        '화물': float(target_row['화물_계'].values[0]),
                        '특수': float(target_row['특수_계'].values[0])
                    }
                    vehicle_df = pd.DataFrame({"차종": list(vehicle_data.keys()), "등록대수": list(vehicle_data.values())})
                    vehicle_df["비중(%)"] = (vehicle_df["등록대수"] / total_vehicle * 100).round(1) if total_vehicle > 0 else 0
                    
                    top_type_row = vehicle_df.sort_values("등록대수", ascending=False).iloc[0]
                    max_type = top_type_row["차종"]
                    max_ratio = float(top_type_row["비중(%)"])

                    use_total_cols = {
                        "관용": pick_col(cols, ["총계_관용", "관용_계", "관용"]),
                        "자가용": pick_col(cols, ["총계_자가용", "자가용_계", "자가용"]),
                        "영업용": pick_col(cols, ["총계_영업용", "영업용_계", "영업용"]),
                    }
                    use_data = {}
                    for u, c in use_total_cols.items():
                        if c is not None: use_data[u] = float(target_row[c].values[0])

                    use_df = pd.DataFrame({"용도": list(use_data.keys()), "등록대수": list(use_data.values())})
                    if not use_df.empty and total_vehicle > 0:
                        use_df["비중(%)"] = (use_df["등록대수"] / total_vehicle * 100).round(1)
                        top_use_row = use_df.sort_values("등록대수", ascending=False).iloc[0]
                        top_use = top_use_row["용도"]
                        top_use_ratio = float(top_use_row["비중(%)"])
                    else:
                        top_use, top_use_ratio = "-", 0.0

                    k1, k2, k3, k4 = st.columns(4)
                    k1.markdown(card("총 등록 차량", f"{total_vehicle:,.0f}대", "전체 합계"), unsafe_allow_html=True)
                    k2.markdown(card("최다 차종", f"{max_type}", f"{max_ratio:.1f}%"), unsafe_allow_html=True)
                    k3.markdown(card("최다 용도", f"{top_use}", f"{top_use_ratio:.1f}%"), unsafe_allow_html=True)
                    
                    hint = "생활 이동 중심"
                    if top_use == "영업용": hint = "산업·물류/사업 활동 비중"
                    elif top_use == "관용": hint = "공공서비스/행정 수요 반영"
                    k4.markdown(card("구조적 힌트", hint, "해석 가이드"), unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    c1, c2 = st.columns(2)
                    with c1:
                        fig_type = go.Figure(data=[go.Pie(
                            labels=vehicle_df["차종"], values=vehicle_df["등록대수"], hole=0.5,
                            textinfo='label+percent', hoverinfo='label+value+percent',
                            marker=dict(colors=DONUT_COLORS_TYPE, line=dict(color="white", width=2))
                        )])
                        fig_type.update_layout(title_text=f"{selected_sigungu} 차종 분포", margin=dict(t=50, b=10, l=0, r=0), height=320)
                        st.plotly_chart(fig_type, use_container_width=True)
                    
                    with c2:
                        if use_df.empty:
                            st.info("용도(관용/자가용/영업용) 총계 컬럼을 찾지 못했습니다.")
                        else:
                            fig_use = go.Figure(data=[go.Pie(
                                labels=use_df["용도"], values=use_df["등록대수"], hole=0.5,
                                textinfo='label+percent', hoverinfo='label+value+percent',
                                marker=dict(colors=DONUT_COLORS_USE, line=dict(color="white", width=2))
                            )])
                            fig_use.update_layout(title_text=f"{selected_sigungu} 용도 분포", margin=dict(t=50, b=10, l=0, r=0), height=320)
                            st.plotly_chart(fig_use, use_container_width=True)

                    
                except KeyError as e:
                    st.error(f"데이터 컬럼을 찾을 수 없습니다. (누락된 컬럼: {e})")
                except Exception as e:
                    st.error(f"차량 데이터를 불러오는 중 오류가 발생했습니다: {e}")
        else:
            st.warning("선택하신 지역의 데이터가 없습니다.")

    except Exception as e:
        st.error(f"에러 발생: {e}")


# -------------------------------------------------------
# [PAGE 2] 자주 묻는 질문 (FAQ) - 카테고리 기능 추가
# -------------------------------------------------------
elif menu == "FAQ": # 사이드바 메뉴 이름이 "FAQ"인지 "❓ 자주 묻는 질문 (FAQ)"인지 확인 필요
    st.markdown(section_title("지자체별 자동차 이용 FAQ 분석"), unsafe_allow_html=True)
    st.caption("카테고리를 선택하면 관련 질문과 답변을 확인할 수 있습니다.")
    st.markdown("---")

    try:
        # 1. DB에서 데이터 가져오기
        df_faq = get_faq_data()

        # 데이터가 있고 필수 컬럼이 존재하는지 확인
        required_cols = ['category', 'question', 'answer']
        # 만약 DB 컬럼명이 한글이라면 ['카테고리', '질문', '답변'] 등으로 수정 필요
        
        if df_faq.empty or not all(col in df_faq.columns for col in required_cols):
            st.info("등록된 FAQ 데이터가 없거나 컬럼명(category, question, answer)이 일치하지 않습니다.")
            # 데이터 확인용 (개발 중에만 표시)
            if not df_faq.empty:
                st.write("현재 로드된 데이터 컬럼:", df_faq.columns.tolist())
        else:
            # 2. 카테고리 선택 UI (사이드바가 아닌 메인 화면 상단에 배치)
            # '전체' 옵션을 맨 앞에 추가하여 모든 질문을 볼 수도 있게 함
            unique_cats = sorted(df_faq['category'].unique().tolist())
            # unique_cats.insert(0, "전체 보기") 
            
            # 탭이나 셀렉트박스로 카테고리 선택 (여기선 pills나 radio가 깔끔하지만 selectbox 사용)
            selected_cat = st.selectbox("궁금한 주제를 선택해주세요 👇", unique_cats)

            st.markdown("<br>", unsafe_allow_html=True)

            # 3. 데이터 필터링
            if selected_cat == "전체 보기":
                filtered_df = df_faq
            else:
                filtered_df = df_faq[df_faq['category'] == selected_cat]

            # 4. 아코디언(Expander) 생성
            if filtered_df.empty:
                st.warning(f"'{selected_cat}' 카테고리에 등록된 질문이 없습니다.")
            else:
                for index, row in filtered_df.iterrows():
                    q_text = row['question']
                    a_text = row['answer']
                    
                    # 질문(Q)을 클릭하면 답변(A)이 열림
                    with st.expander(f"Q. {q_text}"):
                        # 답변에 줄바꿈이 있을 경우 마크다운 적용
                        st.markdown(f"{a_text}")

    except Exception as e:
        st.error(f"FAQ 데이터를 처리하는 중 오류가 발생했습니다: {e}")