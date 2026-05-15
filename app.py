import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="EV Intelligence Dashboard",
    page_icon="⚡",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Main App Background */
.stApp {
    background:
    radial-gradient(circle at top left, #1e1b4b, #0f172a 45%),
    linear-gradient(to right, #0f172a, #111827);
    color: white;
}

/* Main container spacing */
.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(255,255,255,0.03);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Custom Cards */
.metric-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    padding: 24px;
    border-radius: 24px;
    backdrop-filter: blur(14px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    transition: 0.3s ease;
}

.metric-card:hover {
    transform: translateY(-5px);
    background: rgba(255,255,255,0.08);
}

/* Buttons */
.stButton > button {
    background: linear-gradient(135deg,#8b5cf6,#06b6d4);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 0.8rem 1.5rem;
    font-weight: 600;
    transition: 0.3s ease;
    width: 100%;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 25px rgba(139,92,246,0.4);
}

/* Metrics */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.06);
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #8b5cf6;
    border-radius: 10px;
}

/* Headings */
h1, h2, h3, h4 {
    color: white !important;
}

/* Paragraph */
p {
    color: #cbd5e1;
}

/* Remove toolbar */
[data-testid="stToolbar"] {
    display: none;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.markdown("""
# ⚡ EV Analytics
### AI Forecast Dashboard
""")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Forecast",
        "Insights",
        "Market Trends"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 🌍 Regions

- Maharashtra
- Karnataka
- Delhi
- Gujarat
- Tamil Nadu
""")

# ============================================
# HERO SECTION
# ============================================

st.markdown("""
<div style="
padding:40px;
border-radius:28px;
background: rgba(255,255,255,0.05);
backdrop-filter: blur(14px);
border:1px solid rgba(255,255,255,0.08);
margin-bottom:30px;
">

<h1 style="
font-size:60px;
font-weight:800;
margin-bottom:10px;
">
⚡ EV Intelligence Dashboard
</h1>

<p style="
font-size:20px;
color:#94a3b8;
max-width:800px;
line-height:1.8;
">
AI-powered electric vehicle forecasting platform with predictive analytics,
future EV adoption trends, infrastructure growth analysis,
and intelligent market insights.
</p>

</div>
""", unsafe_allow_html=True)

# ============================================
# LOADING
# ============================================

with st.spinner("Analyzing EV market trends..."):
    time.sleep(1)

# ============================================
# KPI SECTION
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#94a3b8;">Projected Growth</h3>
        <h1 style="font-size:42px;">+28%</h1>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#94a3b8;">EV Sales</h3>
        <h1 style="font-size:42px;">124K</h1>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#94a3b8;">Charging Stations</h3>
        <h1 style="font-size:42px;">8.4K</h1>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <h3 style="color:#94a3b8;">Forecast Accuracy</h3>
        <h1 style="font-size:42px;">94%</h1>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.write("")

# ============================================
# SAMPLE DATA
# ============================================

dates = pd.date_range(
    start='2023-01-01',
    periods=24,
    freq='ME'
)

historical = np.random.randint(2500, 6000, 18)
forecast = np.random.randint(6500, 10000, 6)

actual_dates = dates[:18]
forecast_dates = dates[18:]

# ============================================
# CHART SECTION
# ============================================

plt.style.use("dark_background")

plt.rcParams['figure.facecolor'] = '#111827'
plt.rcParams['axes.facecolor'] = '#111827'
plt.rcParams['savefig.facecolor'] = '#111827'

fig, ax = plt.subplots(figsize=(14, 6))

fig.patch.set_facecolor('#111827')
ax.set_facecolor('#111827')

# Historical Data
ax.plot(
    actual_dates,
    historical,
    linewidth=3,
    color='#8b5cf6',
    marker='o',
    markersize=6,
    label='Historical EV Sales'
)

# Forecast Data
ax.plot(
    forecast_dates,
    forecast,
    linewidth=3,
    linestyle='--',
    color='#06b6d4',
    marker='o',
    markersize=6,
    label='Predicted EV Sales'
)

# Divider Line
ax.axvline(
    x=forecast_dates[0],
    color=(1, 1, 1, 0.15),
    linestyle=':',
    linewidth=2,
    zorder=2
)

# Chart Styling
ax.grid(alpha=0.08)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

ax.tick_params(colors='white')

legend = ax.legend()

for text in legend.get_texts():
    text.set_color("white")

ax.set_title(
    "EV Market Forecast",
    fontsize=22,
    color='white',
    pad=20
)

ax.set_xlabel("Timeline", fontsize=12)
ax.set_ylabel("EV Sales", fontsize=12)

plt.xticks(rotation=30)

st.pyplot(fig)

# ============================================
# PREDICTION SUMMARY
# ============================================

st.markdown("""
<div style="
margin-top:20px;
padding:25px;
border-radius:24px;
background: rgba(255,255,255,0.05);
border:1px solid rgba(255,255,255,0.08);
">

<h2>🚀 Prediction Summary</h2>

<p style="
font-size:18px;
line-height:1.9;
color:#cbd5e1;
">

The AI forecasting model predicts a strong upward trajectory
in EV adoption across India. Increased charging infrastructure,
government subsidies, and rising environmental awareness are
expected to accelerate market growth significantly over the
next few years.

</p>

</div>
""", unsafe_allow_html=True)

# ============================================
# INSIGHTS SECTION
# ============================================

st.write("")
st.write("")

st.markdown("""
<div style="
padding:30px;
border-radius:24px;
background: rgba(255,255,255,0.05);
border:1px solid rgba(255,255,255,0.08);
">

<h2>📈 AI Market Insights</h2>

<ul style="
font-size:18px;
line-height:2;
color:#cbd5e1;
">

<li>EV adoption expected to increase by 28% over next 2 years</li>

<li>Maharashtra projected to lead EV infrastructure growth</li>

<li>Two-wheeler EV segment dominates future market demand</li>

<li>Government incentives accelerating EV ecosystem expansion</li>

<li>Charging network expected to expand by 40%</li>

<li>Battery technology improvements reducing ownership costs</li>

</ul>

</div>
""", unsafe_allow_html=True)

# ============================================
# BUTTON SECTION
# ============================================

st.write("")
st.write("")

col1, col2 = st.columns(2)

with col1:
    st.button("⚡ Generate AI Forecast")

with col2:
    st.button("📊 Download Report")

# ============================================
# FOOTER
# ============================================

st.write("")
st.write("")

st.markdown("""
<hr style="border:1px solid rgba(255,255,255,0.08)">

<center>

<h3 style="color:white;">
⚡ EV Intelligence Dashboard
</h3>

<p style="color:#64748b;">
Built with Streamlit • AI Forecasting • Modern Frontend UI
</p>

</center>
""", unsafe_allow_html=True)