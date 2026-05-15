import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EV Adoption Forecaster · Washington State",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&display=swap" rel="stylesheet">

<style>
/* ── Root palette ─────────────────────────────────────────────── */
:root {
    --bg0: #07090f;
    --bg1: #0d1117;
    --bg2: #141922;
    --bg3: #1a2233;
    --accent: #00e5a0;
    --accent2: #0af;
    --accent3: #f06090;
    --muted: #4a5568;
    --text0: #f0f4ff;
    --text1: #a8b8d0;
    --text2: #5a6a80;
    --border: rgba(255,255,255,0.07);
    --font-head: 'Syne', sans-serif;
    --font-body: 'DM Sans', sans-serif;
}

/* ── Global reset ─────────────────────────────────────────────── */
html, body, [class*="css"], [data-testid] {
    background-color: var(--bg0) !important;
    color: var(--text0) !important;
    font-family: var(--font-body) !important;
}

/* ── Hide Streamlit chrome ─────────────────────────────────────── */
#MainMenu, footer, header,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="collapsedControl"] { display: none !important; }

/* ── Main layout ───────────────────────────────────────────────── */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
section[data-testid="stMain"] > div { padding: 0 !important; }

/* ── Hero banner ───────────────────────────────────────────────── */
.hero {
    position: relative;
    width: 100%;
    min-height: 420px;
    background: var(--bg1);
    overflow: hidden;
    display: flex;
    align-items: flex-end;
    padding: 0 0 48px 64px;
}
.hero::before {
    content: '';
    position: absolute; inset: 0;
    background:
        radial-gradient(ellipse 80% 60% at 70% 40%, rgba(0,229,160,0.12) 0%, transparent 65%),
        radial-gradient(ellipse 50% 80% at 90% 80%, rgba(0,170,255,0.10) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 10% 20%, rgba(240,96,144,0.07) 0%, transparent 55%);
}
.hero-grid {
    position: absolute; inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.025) 1px, transparent 1px);
    background-size: 48px 48px;
    mask-image: linear-gradient(to bottom, transparent, black 30%, black 70%, transparent);
}
.hero-label {
    font-family: var(--font-head);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.18em;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 16px;
}
.hero-title {
    font-family: var(--font-head);
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    line-height: 1.05;
    color: var(--text0);
    margin: 0 0 20px;
}
.hero-title span { color: var(--accent); }
.hero-sub {
    font-size: 16px;
    font-weight: 300;
    color: var(--text1);
    max-width: 520px;
    line-height: 1.7;
}
.hero-badge {
    display: inline-block;
    background: rgba(0,229,160,0.12);
    border: 1px solid rgba(0,229,160,0.3);
    color: var(--accent);
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 24px;
}

/* ── Content wrapper ───────────────────────────────────────────── */
.content-wrap {
    padding: 56px 64px;
    background: var(--bg0);
}

/* ── Section label ─────────────────────────────────────────────── */
.section-eyebrow {
    font-family: var(--font-head);
    font-size: 10px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 8px;
}
.section-title {
    font-family: var(--font-head);
    font-size: 28px;
    font-weight: 700;
    color: var(--text0);
    margin: 0 0 32px;
}

/* ── Stat cards row ────────────────────────────────────────────── */
.stat-row {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 40px;
}
.stat-card {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px 28px;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), transparent);
}
.stat-card.blue::before { background: linear-gradient(90deg, var(--accent2), transparent); }
.stat-card.pink::before { background: linear-gradient(90deg, var(--accent3), transparent); }
.stat-num {
    font-family: var(--font-head);
    font-size: 36px;
    font-weight: 800;
    color: var(--text0);
    line-height: 1;
    margin-bottom: 6px;
}
.stat-label {
    font-size: 12px;
    color: var(--text2);
    text-transform: uppercase;
    letter-spacing: 0.1em;
}
.stat-delta {
    font-size: 12px;
    font-weight: 500;
    color: var(--accent);
    margin-top: 8px;
}
.stat-delta.down { color: var(--accent3); }

/* ── Select box ────────────────────────────────────────────────── */
[data-testid="stSelectbox"] label {
    font-family: var(--font-head) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text2) !important;
    margin-bottom: 8px !important;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--bg2) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
    color: var(--text0) !important;
    font-family: var(--font-body) !important;
    font-size: 15px !important;
    transition: border-color 0.2s !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(0,229,160,0.1) !important;
}

/* ── Multiselect ───────────────────────────────────────────────── */
[data-testid="stMultiSelect"] label {
    font-family: var(--font-head) !important;
    font-size: 11px !important;
    letter-spacing: 0.15em !important;
    text-transform: uppercase !important;
    color: var(--text2) !important;
}
[data-testid="stMultiSelect"] > div > div {
    background: var(--bg2) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 10px !important;
}
[data-baseweb="tag"] {
    background: rgba(0,229,160,0.15) !important;
    border: 1px solid rgba(0,229,160,0.3) !important;
    border-radius: 6px !important;
    color: var(--accent) !important;
}

/* ── Charts ────────────────────────────────────────────────────── */
[data-testid="stPyplotRootElement"] {
    background: transparent !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}

/* ── Alert/success box ─────────────────────────────────────────── */
[data-testid="stAlert"] {
    background: rgba(0,229,160,0.08) !important;
    border: 1px solid rgba(0,229,160,0.25) !important;
    border-radius: 10px !important;
    color: var(--text0) !important;
}

/* ── Divider ───────────────────────────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 48px 0 !important;
}

/* ── Subheader ─────────────────────────────────────────────────── */
h2, h3, [data-testid="stHeading"] {
    font-family: var(--font-head) !important;
    font-weight: 700 !important;
    color: var(--text0) !important;
}

/* ── Footer ────────────────────────────────────────────────────── */
.footer-text {
    font-size: 12px;
    color: var(--text2);
    text-align: center;
    padding: 24px 0 40px;
    letter-spacing: 0.05em;
}
.footer-text span { color: var(--accent); }
</style>
""", unsafe_allow_html=True)

# ── Load model ───────────────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    return joblib.load(os.path.join(os.path.dirname(__file__), "forecasting_ev_model.pkl"))

model = load_model()

# ── Load data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), "preprocessed_ev_data.csv"))
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# ── Hero ─────────────────────────────────────────────────────────────────────
hero_img_path = os.path.join(os.path.dirname(__file__), "ev-car-factory.jpg")

st.markdown("""
<div class="hero">
  <div class="hero-grid"></div>
  <div style="position:relative; z-index:2;">
    <div class="hero-label">Washington State · EV Intelligence</div>
    <h1 class="hero-title">Forecast the<br><span>Electric Future</span></h1>
    <p class="hero-sub">
      Machine-learning powered EV adoption projections for every county
      in Washington State — 36-month rolling horizon.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Main content ─────────────────────────────────────────────────────────────
st.markdown('<div class="content-wrap">', unsafe_allow_html=True)

# County totals for stats
county_totals = df.groupby('County')['Electric Vehicle (EV) Total'].sum()
total_ev = int(county_totals.sum())
top_county = county_totals.idxmax()
num_counties = df['County'].nunique()

# ── Stat row ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-num">{total_ev:,}</div>
    <div class="stat-label">Total EVs Tracked</div>
    <div class="stat-delta">↑ across all counties</div>
  </div>
  <div class="stat-card blue">
    <div class="stat-num">{num_counties}</div>
    <div class="stat-label">Counties Covered</div>
    <div class="stat-delta">Full Washington State</div>
  </div>
  <div class="stat-card pink">
    <div class="stat-num">36mo</div>
    <div class="stat-label">Forecast Horizon</div>
    <div class="stat-delta">ML-powered projection</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── County selector ───────────────────────────────────────────────────────────
st.markdown('<div class="section-eyebrow">Single county analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">County Deep Dive</div>', unsafe_allow_html=True)

county_list = sorted(df['County'].dropna().unique().tolist())
col_sel, col_gap = st.columns([2, 3])
with col_sel:
    county = st.selectbox("Select a county", county_list, label_visibility="visible")

if county not in df['County'].unique():
    st.warning(f"County '{county}' not found.")
    st.stop()

county_df = df[df['County'] == county].sort_values("Date")
county_code = county_df['county_encoded'].iloc[0]

# ── Forecasting engine ────────────────────────────────────────────────────────
def run_forecast(cty_df, cty_code, forecast_horizon=36):
    hist_ev = list(cty_df['Electric Vehicle (EV) Total'].values[-6:])
    cum_ev = list(np.cumsum(hist_ev))
    months_since_start = cty_df['months_since_start'].max()
    latest_date = cty_df['Date'].max()
    future_rows = []

    for i in range(1, forecast_horizon + 1):
        forecast_date = latest_date + pd.DateOffset(months=i)
        months_since_start += 1
        lag1, lag2, lag3 = hist_ev[-1], hist_ev[-2], hist_ev[-3]
        roll_mean = np.mean([lag1, lag2, lag3])
        pct_change_1 = (lag1 - lag2) / lag2 if lag2 != 0 else 0
        pct_change_3 = (lag1 - lag3) / lag3 if lag3 != 0 else 0
        recent_cum = cum_ev[-6:]
        slope = np.polyfit(range(len(recent_cum)), recent_cum, 1)[0] if len(recent_cum) == 6 else 0

        row = {
            'months_since_start': months_since_start,
            'county_encoded': cty_code,
            'ev_total_lag1': lag1, 'ev_total_lag2': lag2, 'ev_total_lag3': lag3,
            'ev_total_roll_mean_3': roll_mean,
            'ev_total_pct_change_1': pct_change_1,
            'ev_total_pct_change_3': pct_change_3,
            'ev_growth_slope': slope,
        }
        pred = model.predict(pd.DataFrame([row]))[0]
        future_rows.append({"Date": forecast_date, "Predicted EV Total": round(pred)})
        hist_ev.append(pred)
        if len(hist_ev) > 6: hist_ev.pop(0)
        cum_ev.append(cum_ev[-1] + pred)
        if len(cum_ev) > 6: cum_ev.pop(0)

    return pd.DataFrame(future_rows)

forecast_df = run_forecast(county_df, county_code)

hist_cum = county_df[['Date', 'Electric Vehicle (EV) Total']].copy()
hist_cum['Cumulative EV'] = hist_cum['Electric Vehicle (EV) Total'].cumsum()
hist_cum['Source'] = 'Historical'

forecast_df['Source'] = 'Forecast'
forecast_df['Cumulative EV'] = forecast_df['Predicted EV Total'].cumsum() + hist_cum['Cumulative EV'].iloc[-1]

combined = pd.concat([
    hist_cum[['Date', 'Cumulative EV', 'Source']],
    forecast_df[['Date', 'Cumulative EV', 'Source']]
], ignore_index=True)

# ── Chart ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(14, 5.5))
fig.patch.set_facecolor('#0d1117')
ax.set_facecolor('#0d1117')

hist_data = combined[combined['Source'] == 'Historical']
fore_data = combined[combined['Source'] == 'Forecast']

# Area fills
ax.fill_between(hist_data['Date'], hist_data['Cumulative EV'],
                alpha=0.15, color='#00e5a0', zorder=1)
ax.fill_between(fore_data['Date'], fore_data['Cumulative EV'],
                alpha=0.10, color='#00aaff', zorder=1)

# Lines
ax.plot(hist_data['Date'], hist_data['Cumulative EV'],
        color='#00e5a0', linewidth=2.5, zorder=3, label='Historical')
ax.plot(fore_data['Date'], fore_data['Cumulative EV'],
        color='#00aaff', linewidth=2.5, linestyle='--', zorder=3, label='Forecast')

# Transition marker
if not fore_data.empty:
    ax.axvline(x=fore_data['Date'].iloc[0], color='rgba(255,255,255,0.15)',
               linestyle=':', linewidth=1, zorder=2, alpha=0.4)
    ax.annotate('  Forecast begins', xy=(fore_data['Date'].iloc[0], ax.get_ylim()[1]),
                xytext=(fore_data['Date'].iloc[0], ax.get_ylim()[1]),
                fontsize=9, color='#5a6a80', va='top')

ax.set_xlabel("Year", fontsize=11, color='#4a5568', labelpad=10)
ax.set_ylabel("Cumulative EV Count", fontsize=11, color='#4a5568', labelpad=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.tick_params(colors='#4a5568', labelsize=10)
for spine in ax.spines.values():
    spine.set_edgecolor('#1a2233')
ax.grid(axis='y', color='#1a2233', linewidth=1)
ax.grid(axis='x', color='#1a2233', linewidth=0.5, alpha=0.5)

legend = ax.legend(frameon=True, facecolor='#141922', edgecolor='#1a2233',
                   labelcolor='#a8b8d0', fontsize=11, loc='upper left')

fig.tight_layout(pad=2.0)
st.subheader(f"Cumulative EV Trend — {county} County")
st.pyplot(fig)
plt.close()

# ── Growth insight ────────────────────────────────────────────────────────────
hist_total = hist_cum['Cumulative EV'].iloc[-1]
fore_total = forecast_df['Cumulative EV'].iloc[-1]
if hist_total > 0:
    pct = ((fore_total - hist_total) / hist_total) * 100
    trend = "grow" if pct > 0 else "decline"
    st.success(
        f"**{county} County** EV adoption is projected to **{trend} by {pct:.1f}%** "
        f"over the next 3 years, reaching an estimated **{int(fore_total):,} cumulative EVs**."
    )

# ── Divider ───────────────────────────────────────────────────────────────────
st.markdown("---")

# ── Multi-county comparison ───────────────────────────────────────────────────
st.markdown('<div class="section-eyebrow">Multi-county view</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">Compare Adoption Trends</div>', unsafe_allow_html=True)

multi_counties = st.multiselect(
    "Select up to 3 counties to compare",
    county_list, max_selections=3,
    help="Pick 2–3 counties to compare their projected EV growth side by side.",
)

PALETTE = ['#00e5a0', '#00aaff', '#f06090']

if multi_counties:
    forecast_horizon = 36
    comparison_data = []

    for cty in multi_counties:
        cty_df = df[df['County'] == cty].sort_values("Date")
        cty_code = cty_df['county_encoded'].iloc[0]
        fc = run_forecast(cty_df, cty_code, forecast_horizon)

        h = cty_df[['Date', 'Electric Vehicle (EV) Total']].copy()
        h['Cumulative EV'] = h['Electric Vehicle (EV) Total'].cumsum()
        fc['Cumulative EV'] = fc['Predicted EV Total'].cumsum() + h['Cumulative EV'].iloc[-1]

        full = pd.concat([h[['Date', 'Cumulative EV']], fc[['Date', 'Cumulative EV']]], ignore_index=True)
        full['County'] = cty
        comparison_data.append(full)

    comp_df = pd.concat(comparison_data, ignore_index=True)

    fig2, ax2 = plt.subplots(figsize=(14, 5.5))
    fig2.patch.set_facecolor('#0d1117')
    ax2.set_facecolor('#0d1117')

    for idx, (cty, grp) in enumerate(comp_df.groupby('County')):
        color = PALETTE[idx % len(PALETTE)]
        ax2.fill_between(grp['Date'], grp['Cumulative EV'], alpha=0.08, color=color)
        ax2.plot(grp['Date'], grp['Cumulative EV'],
                 color=color, linewidth=2.5, label=cty, zorder=3)

    ax2.set_xlabel("Year", fontsize=11, color='#4a5568', labelpad=10)
    ax2.set_ylabel("Cumulative EV Count", fontsize=11, color='#4a5568', labelpad=10)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:,.0f}'))
    ax2.tick_params(colors='#4a5568', labelsize=10)
    for spine in ax2.spines.values():
        spine.set_edgecolor('#1a2233')
    ax2.grid(axis='y', color='#1a2233', linewidth=1)
    ax2.grid(axis='x', color='#1a2233', linewidth=0.5, alpha=0.5)
    ax2.legend(frameon=True, facecolor='#141922', edgecolor='#1a2233',
               labelcolor='#a8b8d0', fontsize=11, loc='upper left')

    fig2.tight_layout(pad=2.0)
    st.subheader("EV Adoption Comparison — Historical + 3-Year Forecast")
    st.pyplot(fig2)
    plt.close()

    # Growth summary cards
    growth_parts = []
    for cty in multi_counties:
        grp = comp_df[comp_df['County'] == cty].reset_index(drop=True)
        h_tot = grp['Cumulative EV'].iloc[len(grp) - forecast_horizon - 1]
        f_tot = grp['Cumulative EV'].iloc[-1]
        if h_tot > 0:
            g = ((f_tot - h_tot) / h_tot) * 100
            growth_parts.append(f"**{cty}**: {g:+.1f}%")
        else:
            growth_parts.append(f"**{cty}**: N/A")

    st.success("Projected 3-year EV growth — " + " &nbsp;|&nbsp; ".join(growth_parts))

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-text">
  Built for the <span>AICTE Internship Cycle 2 by S4F</span> &nbsp;·&nbsp;
  Powered by Washington State EV Population Data
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)   # close content-wrap