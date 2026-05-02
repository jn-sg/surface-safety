import streamlit as st

st.title("표면 위생 안전도 평가 프로그램")

residual = st.slider("잔존율 (%)", 0, 100, 20)
transfer = st.slider("전이율 (%)", 0, 100, 30)
removal = st.slider("제거율 (%)", 0, 100, 80)

score = 0.2 * removal + 0.4 * (100 - residual) + 0.4 * (100 - transfer)

st.subheader(f"안전 점수: {score:.2f}")