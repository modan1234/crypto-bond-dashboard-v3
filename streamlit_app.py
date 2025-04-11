import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="📈 암호화폐 & 미국 국채 대시보드", layout="wide")
st.title("📈 암호화폐(XRP) & 미국 국채(10Y) 투자판단 대시보드")

# 날짜 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=180)

# 데이터 다운로드
xrp_df = yf.download("XRP-USD", start=start_date, end=end_date)
bond_df = yf.download("^TNX", start=start_date, end=end_date)

# 결측치 제거
xrp_df.dropna(inplace=True)
bond_df.dropna(inplace=True)

# 시각화
fig = go.Figure()

fig.add_trace(go.Scatter(x=xrp_df.index, y=xrp_df["Close"], name="XRP 가격", yaxis="y1"))
fig.add_trace(go.Scatter(x=bond_df.index, y=bond_df["Close"], name="미국채 10Y 금리", yaxis="y2"))

fig.update_layout(
    title="XRP vs 미국 10년물 국채 수익률",
    xaxis=dict(title="날짜"),
    yaxis=dict(title="XRP 가격", side="left"),
    yaxis2=dict(title="미10년 금리", overlaying="y", side="right"),
    legend=dict(x=0.01, y=0.99),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("🔎 현재 지표로 본 투자 판단")

# 최신값 추출
try:
    xrp_value = xrp_df["Close"].iloc[-1]  # 스칼라 값
    bond_value = bond_df["Close"].iloc[-1]  # 스칼라 값

    # 투자 판단 로직
    if float(xrp_value) < 0.5 and float(bond_value) > 4:
        recommendation = "✅ XRP 매수, 미국채 매도 (암호화폐 상승 초기 가능성)"
    elif float(xrp_value) > 1 and float(bond_value) < 3:
        recommendation = "✅ XRP 매도, 미국채 매수 (암호화폐 과열 및 안전자산 이동)"
    else:
        recommendation = "🟡 중립 (더 많은 데이터 필요)"

    st.markdown(f"""
    - **XRP 현재가**: ${xrp_value:,.3f}
    - **미국 10Y 금리**: {bond_value:.2f}%

    ### 💡 추천 판단:
    **{recommendation}**
    """)

except Exception as e:
    st.error("❌ 데이터를 불러오거나 처리하는 중 오류가 발생했습니다.")
    st.exception(e)
