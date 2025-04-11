import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# 페이지 설정
st.set_page_config(page_title="XRP & 미국채 투자판단", layout="wide")

st.title("📈 암호화폐(XRP) & 미국 국채(10Y) 투자판단 대시보드")

st.markdown("---")

# 데이터 가져오기
@st.cache_data
def get_data():
    xrp_df = yf.download("XRP-USD", period="6mo", interval="1d")
    bond_df = yf.download("^TNX", period="6mo", interval="1d")  # 미국 10년 국채 수익률
    return xrp_df, bond_df

xrp_df, bond_df = get_data()

# 차트 시각화
fig = go.Figure()

fig.add_trace(go.Scatter(
    x=xrp_df.index,
    y=xrp_df["Close"],
    mode='lines',
    name='XRP 가격',
    line=dict(color='blue')
))

fig.add_trace(go.Scatter(
    x=bond_df.index,
    y=bond_df["Close"],
    mode='lines',
    name='미국 10Y 국채금리',
    line=dict(color='red'),
    yaxis='y2'
))

fig.update_layout(
    title="📊 XRP 가격 & 미국 10년물 국채금리 추이",
    xaxis=dict(title='날짜'),
    yaxis=dict(title='XRP 가격 (USD)'),
    yaxis2=dict(
        title='미국 10Y 금리 (%)',
        overlaying='y',
        side='right'
    ),
    legend=dict(x=0, y=1.1, orientation='h')
)

st.plotly_chart(fig, use_container_width=True)

# 투자 판단 로직
st.subheader("🔎 현재 지표로 본 투자 판단")

try:
    xrp_value = float(xrp_df["Close"].iloc[-1])
    bond_value = float(bond_df["Close"].iloc[-1])

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

except Exception as e:
    st.error("❌ 데이터를 불러오거나 처리하는 중 오류가 발생했습니다.")
    st.exception(e)

st.markdown("---")
st.caption("ⓒ 2025. 투자참고용 대시보드 by modan1234")
