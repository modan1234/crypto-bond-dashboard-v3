import streamlit as st
import pandas as pd
import plotly.graph_objs as go
import yfinance as yf
import datetime

st.set_page_config(page_title="크립토 & 미국 국채 투자판단", layout="wide")

st.title("📈 암호화폐(XRP) & 미국 국채(10Y) 투자판단 대시보드")

# 날짜 설정
end_date = datetime.datetime.today()
start_date = end_date - datetime.timedelta(days=365 * 2)

# 데이터 불러오기
@st.cache_data
def load_data():
    xrp = yf.download("XRP-USD", start=start_date, end=end_date)
    bond = yf.download("^TNX", start=start_date, end=end_date)  # 미국 10년물 금리
    return xrp, bond

xrp, bond = load_data()

# 날짜 컬럼 정리
xrp.reset_index(inplace=True)
bond.reset_index(inplace=True)

# 그래프
fig = go.Figure()

fig.add_trace(go.Scatter(x=xrp['Date'], y=xrp['Close'], name='XRP', yaxis='y1', line=dict(color='deepskyblue')))
fig.add_trace(go.Scatter(x=bond['Date'], y=bond['Close'], name='미국10Y금리', yaxis='y2', line=dict(color='orange')))

fig.update_layout(
    title="XRP & 미국 10년물 금리",
    xaxis=dict(title="날짜"),
    yaxis=dict(title="XRP"),
    yaxis2=dict(
        title="미10년 금리",
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0, y=1.1, orientation="h"),
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# 투자 판단 로직 (간단 예시)
latest_xrp = xrp['Close'].iloc[-1]
latest_bond = bond['Close'].iloc[-1]

st.subheader("🔎 현재 지표로 본 투자 판단")

if latest_xrp < 0.5 and latest_bond > 4:
    st.success("✅ XRP 저평가 + 금리 고점 예상 → XRP 매수 기회 가능성")
elif latest_xrp > 1.0 and latest_bond < 3:
    st.warning("⚠️ XRP 고평가 + 금리 저점 → 매도 고려")
else:
    st.info("📊 중립: 명확한 추세 아님")

st.caption("데이터 출처: Yahoo Finance | 본 대시보드는 투자 참고용이며, 책임은 사용자에게 있습니다.")

