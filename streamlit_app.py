import streamlit as st
import pandas as pd
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(page_title="Crypto-Bond Dashboard", layout="wide")

# 탭 UI 구성
tab1, tab2, tab3 = st.tabs(["📈 실시간 지표", "🧠 투자 판단", "ℹ️ 설명 및 가이드"])

# 탭 1: 실시간 지표
with tab1:
    st.header("📊 실시간 글로벌 경제 지표 대시보드")

    st.info("※ 현재는 예시 데이터입니다. 추후 실시간 API 연동 예정입니다.")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="VIX (변동성지수)", value="17.3", delta="-1.2")
        st.metric(label="금 가격", value="$2,325", delta="+0.4%")
        st.metric(label="WTI 유가", value="$82.1", delta="+0.9%")

    with col2:
        st.metric(label="나스닥", value="13,980", delta="-0.8%")
        st.metric(label="달러 인덱스 (DXY)", value="101.5", delta="-0.3%")
        st.metric(label="미 10년 국채금리", value="4.21%", delta="+0.05%")

    with col3:
        st.metric(label="BTC 가격", value="$64,300", delta="+1.8%")
        st.metric(label="XRP 가격", value="$0.58", delta="+0.6%")
        st.metric(label="USD/KRW 환율", value="1,345.20₩", delta="-3.2₩")

    st.markdown("---")
    
    st.subheader("📉 주요 지표 차트 (예시)")
    sample_data = pd.DataFrame({
        "날짜": pd.date_range(start="2024-04-01", periods=7),
        "VIX": [18.2, 17.8, 17.1, 16.9, 17.5, 17.3, 17.0],
        "금리": [4.10, 4.15, 4.18, 4.17, 4.20, 4.23, 4.21],
    })

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sample_data["날짜"], y=sample_data["VIX"], name="VIX", line=dict(color='orange')))
    fig.add_trace(go.Scatter(x=sample_data["날짜"], y=sample_data["금리"], name="미10년 금리", yaxis="y2", line=dict(color='blue')))

    # y축 2개 설정
    fig.update_layout(
        xaxis=dict(title="날짜"),
        yaxis=dict(title="VIX"),
        yaxis2=dict(title="미10년 금리", overlaying
