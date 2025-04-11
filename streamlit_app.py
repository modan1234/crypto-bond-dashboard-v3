import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
from datetime import datetime, timedelta

# 페이지 기본 설정
st.set_page_config(page_title="📈 암호화폐(XRP) & 미국 국채 투자판단", layout="wide")

st.title("📈 암호화폐(XRP) & 미국 국채(10Y) 투자판단 대시보드")

# 날짜 설정
end_date = datetime.today()
start_date = end_date - timedelta(days=180)

# 데이터 불러오기
xrp_df = yf.download("XRP-USD", start=start_date, end=end_date)
bond_df = yf.download("^TNX", start=start_date, end=end_date)  # 미국 10년물 국채 수익률

# 가격 시각화
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

# 최신 값 가져오기
latest_xrp = xrp_df["Close"]
latest_bond = bond_df["Close"]

xrp_value = latest_xrp.iloc[-1]
bond_value = latest_bond.iloc[-1]

st.subheader("🔎 현재 지표로 본 투자 판단")

# 추천 판단 로직
if xrp_value < 0.5 and bond_value > 4:
    recommendation = "✅ XRP 매수, 미국채 매도 (암호화폐 상승 초기 가능성)"
elif xrp_value > 1 and bond_value < 3:
    recommendation = "✅ XRP 매도, 미국채 매수 (암호화폐 과열 및 안전자산 이동)"
else:
    recommendation = "🟡 중립 (더 많은 데이터 필요)"

st.markdown(f"""
- **XRP 현재가**: ${xrp_value:,.3f}
- **미국 10Y 금리**: {bond_value:.2f}%

### 💡 추천 판단:
**{recommendation}**
""")

