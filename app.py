import streamlit as st
import plotly.graph_objects as go

st.set_page_config(
    page_title="Surface Hygiene Risk Dashboard",
    layout="wide"
)

st.title("Surface Hygiene Risk Dashboard")
st.caption("A data-driven evaluation tool for school facility surfaces")

# 입력 영역
st.sidebar.header("Input Variables")

residual = st.sidebar.slider("Residual Rate (%)", 0, 100, 20)
transfer = st.sidebar.slider("Transfer Rate (%)", 0, 100, 30)
removal = st.sidebar.slider("Removal Rate (%)", 0, 100, 80)
aw = st.sidebar.slider("Adsorption-Water Index (%)", 0, 100, 50)

# 점수 계산
score = 0.5 * (100 - residual) + 0.2 * removal + 0.1 * (100 - transfer) + 0.2 * (100 - aw)
risk = 100 - score

# 등급 판정
if score >= 85:
    grade = "Very Safe"
    message = "Current surface condition shows a very low level of residual and transfer risk."
elif score >= 70:
    grade = "Safe"
    message = "Current surface condition is generally safe, but some improvement may be possible."
elif score >= 50:
    grade = "Caution"
    message = "Surface hygiene management is recommended."
else:
    grade = "Dangerous"
    message = "Immediate improvement is required."

# 상단 점수 카드
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Safety Score", f"{score:.2f}")

with col2:
    st.metric("Risk Index", f"{risk:.2f}")

with col3:
    st.metric("Risk Level", grade)

st.divider()

# 그래프 영역
left_col, right_col = st.columns([1.5, 0.9])

with left_col:
    st.subheader("Multi-Indicator Hygiene Profile")

    categories = ["Residual", "Transfer", "Removal", "Adsorption"]
    values = [residual, transfer, removal, aw]

    fig_radar = go.Figure()

    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill="toself",
        name="Hygiene Indicators"
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        height=520,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig_radar, use_container_width=True)

with right_col:
    st.subheader("Hygiene Risk Index")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=risk,
        title={"text": "Risk Index"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#B22222"},
            "steps": [
                {"range": [0, 30], "color": "#D9F2D9"},
                {"range": [30, 60], "color": "#FFF2CC"},
                {"range": [60, 80], "color": "#FCE4D6"},
                {"range": [80, 100], "color": "#F4CCCC"},
            ],
        }
    ))

    fig_gauge.update_layout(
        height=520,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    st.plotly_chart(fig_gauge, use_container_width=True)

st.divider()

# 해석 및 개선 제안
bottom_left, bottom_right = st.columns(2)

with bottom_left:
    st.subheader("Automated Interpretation")
    if score >= 85:
        st.success(message)
    elif score >= 70:
        st.info(message)
    elif score >= 50:
        st.warning(message)
    else:
        st.error(message)

with bottom_right:
    st.subheader("Improvement Recommendations")

    recommendations = []

    if residual > 30:
        recommendations.append("Residual rate is relatively high. Surface material improvement should be considered.")

    if transfer > 40:
        recommendations.append("Transfer rate is relatively high. Additional surface treatment may be required.")

    if removal < 70:
        recommendations.append("Removal rate is relatively low. Cleaning method improvement is recommended.")

    if aw > 60:
        recommendations.append("Adsorption-water index is high. Moisture retention may increase contamination persistence.")

    if recommendations:
        for rec in recommendations:
            st.write("- " + rec)
    else:
        st.write("No major improvement factor was detected under the current conditions.")
