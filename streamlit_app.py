import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.set_page_config(page_title="XRP & 미국 국채 투자판단", layout="wide")

st.title("📈 암호화폐(XRP) & 미국 국채(10Y) 투자판단 대시보드")

# 날짜 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=90)

# 데이터 가져오기
xrp = yf.download("XRP-USD", start=start_date, end=end_date)
bond = yf.download("^TNX", start=start_date, end=end_date)  # 미국 10년물 금리

# 최신 데이터 추출
latest_xrp = xrp["Close"]
latest_bond = bond["Close"]

# 그래프 만들기
fig = go.Figure()

fig.add_trace(go.Scatter(x=latest_xrp.index, y=latest_xrp, name="XRP", yaxis="y1", line=dict(color="dodgerblue")))
fig.add_trace(go.Scatter(x=latest_bond.index, y=latest_bond, name="미국 10년 금리(%)", yaxis="y2", line=dict(color="tomato")))

fig.update_layout(
    title="📊 XRP vs 미국 10년물 금리(최근 3개월)",
    xaxis=dict(title="날짜"),
    yaxis=dict(title="XRP 가격 (USD)", side="left"),
    yaxis2=dict(
        title="미10년 금리 (%)",
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0, y=1.1, orientation="h")
)

st.plotly_chart(fig, use_container_width=True)

# 추천 판단 로직
xrp_value = latest_xrp.iloc[-1]
bond_value = latest_bond.iloc[-1]

st.subheader("🔎 현재 지표로 본 투자 판단")

if xrp_value < 0.5 and bond_value > 4:
    recommendation = "✅ XRP 매수 / 미국 국채 매도"
elif xrp_value > 1 and bond_value < 3:
    recommendation = "⚠️ XRP 매도 / 미국 국채 매수"
else:
    recommendation = "🟡 중립 (추가 지표 분석 필요)"

st.markdown(f"### 💡 판단 결과: **{recommendation}**")
st.caption(f"※ 최신 XRP 가격: {xrp_value:.3f} USD / 미국 10Y 금리: {bond_value:.2f}%")
