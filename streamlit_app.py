import streamlit as st
from app.calculator import calculate_emissions

st.set_page_config(
    page_title="EcoRoute – Green Commute Planner",
    page_icon="🌱",
    layout="centered"
)

st.title("🌱 EcoRoute")
st.subheader("Plan the Greenest Commute (India)")

st.markdown(
    """
    This app helps you **compare transport options** based on  
    **CO₂ emissions using Indian data (2024–2025)**.
    """
)

st.divider()

# User inputs
distance = st.number_input(
    "Enter distance (in km)",
    min_value=0.1,
    step=0.5
)

mode = st.selectbox(
    "Select transport mode",
    [
        "SUV",
        "Hatchback",
        "Motorcycle",
        "Electric Bus",
        "CNG Bus",
        "Metro",
        "Walking",
        "Cycling"
    ]
)

if st.button("Calculate CO₂ Emissions"):
    try:
        emissions = calculate_emissions(mode, distance)
        st.success(
            f"🌍 Estimated CO₂ Emission: **{emissions:.2f} kg**"
        )

        if emissions == 0:
            st.balloons()
            st.info("Excellent choice! Zero emissions 🚲🚶")
    except Exception as e:
        st.error("Could not calculate emissions.")

st.divider()

st.caption(
    "🔍 Data Source: Indian transport emission factors | "
    "⚙️ Local AI (IBM Granite via Ollama)"
)
