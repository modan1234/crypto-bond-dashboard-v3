import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
import yfinance as yf

st.set_page_config(page_title="XRP & 미국국채 투자판단", layout="wide")

st.title("📈 암호화폐(XRP) & 미국 국채(10Y) 투자판단 대시보드")

# 📊 데이터 불러오기
@st.cache_data(ttl=3600)
def load_data():
    xrp = yf.download("XRP-USD", period="7d", interval="1h")
    bond = yf.download("^TNX", period="7d", interval="1h")  # 미국 10년 국채 금리
    return xrp['Close'], bond['Close']

try:
    latest_xrp, latest_bond = load_data()
    xrp_value = latest_xrp.iloc[-1]
    bond_value = latest_bond.iloc[-1]

    # 그래프
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=latest_xrp.index,
        y=latest_xrp,
        name="XRP 가격",
        yaxis="y1",
        line=dict(color="blue")
    ))

    fig.add_trace(go.Scatter(
        x=latest_bond.index,
        y=latest_bond,
        name="미10년 금리",
        yaxis="y2",
        line=dict(color="red", dash="dot")
    ))

    fig.update_layout(
        title="📊 최근 7일 XRP 가격 & 미국 10Y 금리",
        xaxis=dict(title="날짜"),
        yaxis=dict(title="XRP 가격 (USD)", side="left"),
        yaxis2=dict(title="10Y 금리 (%)", overlaying="y", side="right"),
        legend=dict(x=0, y=1.1, orientation="h")
    )

    st.plotly_chart(fig, use_container_width=True)

    # 추천 판단 로직
    try:
        xrp_float = float(xrp_value)
        bond_float = float(bond_value)

        if xrp_float > 2.5 and bond_float < 2.5:
            recommendation = "🔴 과열 - 현금화 고려"
        elif xrp_float < 0.5 and bond_float > 4.5:
            recommendation = "🟢 저점 매수 기회"
        elif 0.5 <= xrp_float <= 1.5 and 3.5 <= bond_float <= 4.5:
            recommendation = "🟡 중립 (추가 관망)"
        elif 1.5 < xrp_float <= 2.5 and bond_float < 3.0:
            recommendation = "🟠 상승 초입 - 분할 매수 고려"
        else:
            recommendation = "⚪ 판단 유보 (데이터 모니터링)"

    except Exception as e:
        recommendation = f"❌ 추천 판단 중 오류 발생: {e}"

    # 출력
    st.markdown(f"""
    ### 🔎 현재 지표로 본 투자 판단
    - **XRP 현재가**: ${xrp_float:,.3f}
    - **미국 10Y 금리**: {bond_float:.2f}%
    - **💡 추천 판단**:  
    {recommendation}
    """)

except Exception as e:
    st.error("❌ 데이터를 불러오거나 처리하는 중 오류가 발생했습니다.")
    st.code(str(e))

st.markdown("---")
st.markdown("ⓒ 2025. 투자참고용 대시보드 by modan1234")
