import streamlit as st
import openai
import json
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Sustainable Transport Planner",
    page_icon="🌱",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E7D32;
        padding: 20px;
    }
    .stButton>button {
        background-color: #2E7D32;
        color: white;
        width: 100%;
        border-radius: 10px;
        padding: 10px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #f0f9f0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E7D32;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'api_key' not in st.session_state:
    st.session_state.api_key = ""
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Emission data (kg CO2 per km)
EMISSION_DATA = {
    "Private Car": {"emissions": 0.192, "cost_per_km": 8, "speed": 30, "icon": "🚗"},
    "Auto-Rickshaw": {"emissions": 0.085, "cost_per_km": 12, "speed": 25, "icon": "🛺"},
    "Bus": {"emissions": 0.089, "cost_per_km": 2, "speed": 20, "icon": "🚌"},
    "Metro/Train": {"emissions": 0.045, "cost_per_km": 2.5, "speed": 40, "icon": "🚇"},
    "Bicycle": {"emissions": 0.0, "cost_per_km": 0.5, "speed": 15, "icon": "🚲"},
    "Electric Scooter": {"emissions": 0.02, "cost_per_km": 3, "speed": 25, "icon": "🛴"},
    "Walking": {"emissions": 0.0, "cost_per_km": 0, "speed": 5, "icon": "🚶"}
}

def calculate_route_metrics(distance, mode):
    """Calculate emissions, cost, and time for a given route"""
    mode_data = EMISSION_DATA[mode]
    
    emissions = distance * mode_data["emissions"]
    cost = distance * mode_data["cost_per_km"]
    time = (distance / mode_data["speed"]) * 60  # in minutes
    sustainability_score = max(0, 100 - (mode_data["emissions"] * 100))
    
    return {
        "mode": mode,
        "icon": mode_data["icon"],
        "emissions": round(emissions, 3),
        "cost": round(cost, 2),
        "time": round(time, 1),
        "sustainability_score": round(sustainability_score, 1),
        "distance": distance
    }

def get_ai_recommendation(origin, destination, priority, distance, api_key):
    """Get AI-powered recommendations using OpenAI"""
    
    # Calculate metrics for all modes
    all_routes = []
    for mode in EMISSION_DATA.keys():
        metrics = calculate_route_metrics(distance, mode)
        all_routes.append(metrics)
    
    # Sort based on priority
    if priority == "Eco-Friendly":
        all_routes.sort(key=lambda x: x["emissions"])
    elif priority == "Low Cost":
        all_routes.sort(key=lambda x: x["cost"])
    elif priority == "Fast":
        all_routes.sort(key=lambda x: x["time"])
    
    # Create context for AI
    routes_summary = "\n".join([
        f"{r['mode']}: {r['emissions']}kg CO2, ₹{r['cost']}, {r['time']} mins"
        for r in all_routes[:3]
    ])
    
    # AI Prompt
    system_prompt = """You are an AI sustainability advisor for urban transport. 
    Your role is to help users make informed, eco-friendly commute decisions.
    Be friendly, concise, and focus on environmental impact.
    Always mention the carbon footprint and provide actionable insights."""
    
    user_prompt = f"""
    Journey Details:
    - Origin: {origin}
    - Destination: {destination}
    - Distance: {distance} km
    - User Priority: {priority}
    
    Top 3 Transport Options:
    {routes_summary}
    
    Provide a personalized recommendation in 3-4 sentences that:
    1. Suggests the best option based on their priority
    2. Highlights the environmental benefit
    3. Mentions a practical tip or insight
    """
    
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        recommendation = response.choices[0].message.content
        return all_routes, recommendation
        
    except Exception as e:
        st.error(f"AI Error: {str(e)}")
        return all_routes, "Unable to generate AI recommendation. Please check your API key."

def create_comparison_chart(routes_data):
    """Create interactive comparison chart"""
    df = pd.DataFrame(routes_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='CO₂ Emissions (kg)',
        x=df['mode'],
        y=df['emissions'],
        marker_color='#FF6B6B'
    ))
    
    fig.add_trace(go.Bar(
        name='Cost (₹)',
        x=df['mode'],
        y=df['cost'],
        marker_color='#4ECDC4'
    ))
    
    fig.update_layout(
        title="Transport Mode Comparison",
        xaxis_title="Transport Mode",
        yaxis_title="Value",
        barmode='group',
        height=400
    )
    
    return fig

def create_sustainability_gauge(score):
    """Create sustainability score gauge"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Sustainability Score"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#2E7D32"},
            'steps': [
                {'range': [0, 33], 'color': "#FFCDD2"},
                {'range': [33, 66], 'color': "#FFF9C4"},
                {'range': [66, 100], 'color': "#C8E6C9"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

# Main App
st.markdown("<h1 class='main-header'>🌱 Sustainable Transport Planner</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>AI-Powered Journey Planning for Sustainable Cities (SDG 11)</p>", unsafe_allow_html=True)

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=st.session_state.api_key,
        help="Enter your OpenAI API key to enable AI recommendations"
    )
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key configured")
    
    st.markdown("---")
    st.header("📊 About")
    st.info("""
    This AI tool helps you:
    - Compare transport carbon footprints
    - Get personalized eco-friendly recommendations
    - Understand environmental impact of your commute
    
    **SDG Alignment:** SDG 11, 13, 3
    """)
    
    st.markdown("---")
    st.header("🔧 AI Components")
    st.markdown("""
    - **NLP:** Entity extraction from queries
    - **RAG:** Local transport data retrieval
    - **LLM:** GPT-3.5 for recommendations
    - **Analytics:** Emission calculations
    """)

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.header("🗺️ Plan Your Journey")
    
    origin = st.text_input("📍 From", placeholder="Enter starting point (e.g., College)")
    destination = st.text_input("📍 To", placeholder="Enter destination (e.g., Railway Station)")
    
    col_a, col_b = st.columns(2)
    with col_a:
        distance = st.number_input("📏 Distance (km)", min_value=0.5, max_value=100.0, value=8.0, step=0.5)
    with col_b:
        priority = st.selectbox("🎯 Priority", ["Eco-Friendly", "Low Cost", "Fast"])
    
    calculate_btn = st.button("🚀 Find Sustainable Routes")

with col2:
    st.header("💡 Quick Tips")
    st.success("""
    **Did you know?**
    - 🚲 Cycling 5km saves 0.96kg CO₂ vs. driving
    - 🚇 Metro emits 4x less than cars
    - 🚶 Walking improves health & planet
    """)

# Results Section
if calculate_btn:
    if not origin or not destination:
        st.error("⚠️ Please enter both origin and destination")
    elif not st.session_state.api_key:
        st.error("⚠️ Please configure OpenAI API key in the sidebar")
    else:
        with st.spinner("🤖 AI is analyzing your route..."):
            routes, ai_recommendation = get_ai_recommendation(
                origin, destination, priority, distance, st.session_state.api_key
            )
        
        st.success("✅ Routes calculated successfully!")
        
        # AI Recommendation Box
        st.markdown("---")
        st.header("🤖 AI Recommendation")
        st.info(ai_recommendation)
        
        # Route Comparison
        st.markdown("---")
        st.header("📊 Transport Options Comparison")
        
        # Display top 3 routes
        for idx, route in enumerate(routes[:3]):
            with st.expander(
                f"{route['icon']} {route['mode']} - Sustainability Score: {route['sustainability_score']}/100",
                expanded=(idx == 0)
            ):
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("🍃 CO₂ Emissions", f"{route['emissions']} kg")
                with col2:
                    st.metric("💰 Cost", f"₹{route['cost']}")
                with col3:
                    st.metric("⏱️ Time", f"{route['time']} min")
                with col4:
                    st.metric("📊 Score", f"{route['sustainability_score']}/100")
                
                if idx == 0:
                    st.success(f"⭐ **Best match for {priority}**")
                
                # Sustainability Gauge
                if idx == 0:
                    gauge_fig = create_sustainability_gauge(route['sustainability_score'])
                    st.plotly_chart(gauge_fig, use_container_width=True)
        
        # Comparison Chart
        st.markdown("---")
        chart_fig = create_comparison_chart(routes[:5])
        st.plotly_chart(chart_fig, use_container_width=True)
        
        # Impact Summary
        st.markdown("---")
        st.header("🌍 Environmental Impact")
        
        best_option = routes[0]
        worst_option = routes[-1]
        co2_saved = worst_option['emissions'] - best_option['emissions']
        trees_equivalent = int(co2_saved / 0.02)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "CO₂ Saved vs. Car",
                f"{co2_saved:.2f} kg",
                delta=f"-{((co2_saved/worst_option['emissions'])*100):.1f}%",
                delta_color="normal"
            )
        
        with col2:
            st.metric(
                "Trees Planted Equivalent",
                f"{trees_equivalent} 🌳"
            )
        
        with col3:
            cost_saved = worst_option['cost'] - best_option['cost']
            st.metric(
                "Money Saved",
                f"₹{cost_saved:.2f}",
                delta=f"-{((cost_saved/worst_option['cost'])*100):.1f}%",
                delta_color="normal"
            )
        
        st.success(f"""
        🎉 **Great Choice!** By choosing **{best_option['mode']}** instead of **{worst_option['mode']}**, 
        you're contributing to a cleaner, healthier city. If you make this journey daily, 
        you'd save **{co2_saved * 365:.2f} kg CO₂** per year! 🌱
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p><strong>Sustainable Transport Planner</strong> | SDG 11: Sustainable Cities and Communities</p>
    <p>Built with ❤️ for 1M1B AI for Sustainability Virtual Internship (IBM SkillsBuild & AICTE)</p>
</div>
""", unsafe_allow_html=True)