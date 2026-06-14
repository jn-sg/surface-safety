import streamlit as st

st.title("표면 위생 안전도 평가 프로그램")

residual = st.slider("잔존율 (%)", 0, 100, 20)
transfer = st.slider("전이율 (%)", 0, 100, 30)
removal = st.slider("제거율 (%)", 0, 100, 80)

aw = st.slider("물 흡착성 지표 (%)", 0, 100, 50)

score = 0.5 * (100 - residual) + 0.2 * removal + 0.1 * (100 - transfer) + 0.2 * (100 - aw)
risk = 100 - score

st.subheader(f"안전 점수: {score:.2f}")
# 기존 코드 아래에 추가

# 등급 표시
if score >= 85:
    st.success("매우 안전")
    st.write("현재 표면은 미생물 잔존 및 전이 위험이 매우 낮은 상태입니다.")
elif score >= 70:
    st.info("안전")
    st.write("전반적으로 안전하지만 일부 개선이 가능합니다.")
elif score >= 50:
    st.warning("보통")
    st.write("표면 위생 관리가 필요합니다.")
else:
    st.error("위험")
    st.write("즉각적인 개선이 필요합니다.")

# 개선 제안
st.subheader("개선 권장 사항")

if residual > 30:
    st.write("- 잔존율이 높음 → 소재 개선 필요")

if transfer > 40:
    st.write("- 전이율이 높음 → 표면 처리 필요")

if removal < 70:
    st.write("- 제거율이 낮음 → 청소 방법 개선 필요")

#그래프
import plotly.graph_objects as go

st.subheader("위생 지표 레이더 분석")

categories = ['Residual', 'Transfer', 'Removal', 'Adsorption']

fig = go.Figure()

fig.add_trace(go.Scatterpolar(
    r=[residual, transfer, removal, aw],
    theta=categories,
    fill='toself',
    name='Hygiene'
))

fig.update_layout(
    polar=dict(
        radialaxis=dict(visible=True, range=[0, 100])
    ),
    showlegend=False
)

st.plotly_chart(fig)
