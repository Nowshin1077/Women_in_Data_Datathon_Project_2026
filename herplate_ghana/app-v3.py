import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Streamlit page configuration
st.set_page_config(
    page_title="HerPlate Ghana: Simplified Food System Diagnostic",
    page_icon="🇬🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean, high-impact styling
st.markdown("""
<style>
    /* Dark-mode resilient & theme-adaptive custom CSS */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #2563EB;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: var(--text-color, #4B5563);
        margin-bottom: 1.2rem;
        opacity: 0.9;
    }
    .metric-card {
        background-color: var(--secondary-background-color, #F8FAFC);
        border: 1px solid var(--border-color, #E2E8F0);
        border-left: 5px solid #2563EB !important;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        text-align: center;
        color: var(--text-color, #1F2937);
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2563EB;
    }
    .metric-label {
        font-size: 0.85rem;
        color: var(--text-color, #64748B);
        text-transform: uppercase;
        font-weight: 600;
        opacity: 0.85;
    }
    .detail-card {
        background-color: var(--secondary-background-color, #FFFFFF);
        border: 1px solid var(--border-color, #E2E8F0);
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        height: 100%;
        color: var(--text-color, #1F2937);
    }
    .detail-card h4 {
        color: var(--text-color, #1E3A8A) !important;
        margin-top: 0;
        margin-bottom: 0.5rem;
    }
    .detail-card p, .detail-card span, .detail-card b, .detail-card small {
        color: var(--text-color, #374151);
    }
    .badge-red {
        background-color: rgba(220, 38, 38, 0.15);
        color: #EF4444 !important;
        border: 1px solid rgba(220, 38, 38, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-orange {
        background-color: rgba(217, 119, 6, 0.15);
        color: #F59E0B !important;
        border: 1px solid rgba(217, 119, 6, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-blue {
        background-color: rgba(37, 99, 235, 0.15);
        color: #3B82F6 !important;
        border: 1px solid rgba(37, 99, 235, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .badge-green {
        background-color: rgba(16, 185, 129, 0.15);
        color: #10B981 !important;
        border: 1px solid rgba(16, 185, 129, 0.4);
        padding: 4px 10px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.8rem;
        display: inline-block;
    }
    .break-point {
        color: #EF4444 !important;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    .solution-point {
        color: #10B981 !important;
        font-weight: 700;
        margin-top: 0.5rem;
    }

    /* Force dark mode compatibility */
    @media (prefers-color-scheme: dark) {
        .main-header { color: #60A5FA !important; }
        .sub-header { color: #E2E8F0 !important; }
        .metric-card {
            background-color: #1E293B !important;
            border-color: #334155 !important;
            color: #F8FAFC !important;
        }
        .metric-value { color: #60A5FA !important; }
        .metric-label { color: #94A3B8 !important; }
        .metric-card small { color: #CBD5E1 !important; }
        .detail-card {
            background-color: #1E293B !important;
            border-color: #334155 !important;
            color: #F8FAFC !important;
        }
        .detail-card h4 { color: #93C5FD !important; }
        .detail-card p, .detail-card span, .detail-card b { color: #E2E8F0 !important; }
        .card-text-muted { color: #CBD5E1 !important; }
    }
</style>
""", unsafe_allow_html=True)

# Helper function to load datasets
@st.cache_data
def load_data():
    cahd_path = "cleaned_ghana_cahd.csv"
    fbs_path = "cleaned_ghana_fbs.csv"
    mddw_path = "cleaned_ghana_mddw.csv"
    
    if not (os.path.exists(cahd_path) and os.path.exists(fbs_path) and os.path.exists(mddw_path)):
        st.error("⚠️ Data files not found. Please run `python data_prep.py` first!")
        st.stop()
        
    cahd = pd.read_csv(cahd_path)
    fbs = pd.read_csv(fbs_path)
    mddw = pd.read_csv(mddw_path)
    return cahd, fbs, mddw

cahd_df, fbs_df, mddw_df = load_data()

# -------------------------------------------------------------
# SIDEBAR CONTROLS & INTERACTIVE SCENARIO
# -------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/emoji/96/000000/ghana-emoji.png", width=60)
st.sidebar.title("🇬🇭 HerPlate Ghana")
st.sidebar.markdown("**Decision-Support System for Maternal Agrifood Reform**")

location_filter = st.sidebar.radio(
    "Target Location / Demographic:",
    ["National Average", "Urban Women", "Rural Women"],
    index=0
)

col_map = {
    "National Average": "National_Consumption_Pct",
    "Urban Women": "Urban_Consumption_Pct",
    "Rural Women": "Rural_Consumption_Pct"
}
target_col = col_map[location_filter]

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Policy Intervention Simulator")
asf_subsidy = st.sidebar.slider(
    "Animal-Source Food Subsidy (%)",
    min_value=0, max_value=50, value=0, step=5,
    help="Simulate cost reduction in high-protein animal foods (Eggs, Dairy, Fish)."
)

if asf_subsidy > 0:
    st.sidebar.success(f"💡 Simulating a {asf_subsidy}% subsidy on Animal-Source Foods.")

# -------------------------------------------------------------
# HEADER & CORE PROBLEM STATEMENT
# -------------------------------------------------------------
st.markdown("<div class='main-header'>🇬🇭 HerPlate Ghana: Food System Bottleneck Diagnostic</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'><b>Core Question:</b> <i>Where is the pathway from Ghana's food system to women's plates breaking?</i></div>", unsafe_allow_html=True)

# Top 4 KPI Cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-label'>Unable to Afford Healthy Diet</div>
        <div class='metric-value'>66.6%</div>
        <small>UN SOFI Report Baseline</small>
    </div>
    """, unsafe_allow_html=True)

with kpi2:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-label'>Animal Food Basket Share</div>
        <div class='metric-value'>41.1%</div>
        <small>Largest Cost Contributor</small>
    </div>
    """, unsafe_allow_html=True)

with kpi3:
    st.markdown("""
    <div class='metric-card'>
        <div class='metric-label'>Target Population</div>
        <div class='metric-value'>WRA 15-49</div>
        <small>Women of Reproductive Age</small>
    </div>
    """, unsafe_allow_html=True)

with kpi4:
    st.markdown("""
    <div class='metric-card' style='border-left: 5px solid #D97706;'>
        <div class='metric-label'>Core Analytical Thesis</div>
        <div class='metric-value' style='font-size:1.1rem; color:#D97706; padding-top:0.3rem;'>
            Same Dietary Gap.<br>4 Different Bottlenecks.
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# 1 HERO GRAPH: THE BOTTLENECK DIAGNOSTIC CHART
# -------------------------------------------------------------
st.subheader("📊 The Diagnostic Overview: Supply Trend vs. Women's Plate Consumption")

# Structure data for the Hero Chart
summary_data = [
    {
        "Food Group": "🥛 Dairy Products",
        "Consumption_Pct": mddw_df.loc[mddw_df["Food_Group"] == "Dairy Products", target_col].values[0] + (asf_subsidy * 0.2),
        "Supply_Trend_Pct": -24.4,
        "Pressure_Type": "Convergent Pressure",
        "Cost_Factor": "Very High (ASF Basket)",
        "Where_It_Breaks": "Production ➔ Market ➔ Household"
    },
    {
        "Food Group": "🫘 Pulses (Beans & Peas)",
        "Consumption_Pct": mddw_df.loc[mddw_df["Food_Group"] == "Pulses (beans, peas, lentils)", target_col].values[0],
        "Supply_Trend_Pct": -39.4,
        "Pressure_Type": "Supply/Diversity Pressure",
        "Cost_Factor": "Low Relative Cost",
        "Where_It_Breaks": "Production / National Supply"
    },
    {
        "Food Group": "🥚 Eggs",
        "Consumption_Pct": mddw_df.loc[mddw_df["Food_Group"] == "Eggs", target_col].values[0] + (asf_subsidy * 0.3),
        "Supply_Trend_Pct": 3.9,
        "Pressure_Type": "Access Beyond Supply",
        "Cost_Factor": "Moderate / Market Margin",
        "Where_It_Breaks": "Market Distribution ➔ Plate"
    },
    {
        "Food Group": "🥬 Vegetables",
        "Consumption_Pct": mddw_df.loc[mddw_df["Food_Group"] == "Other vegetables", target_col].values[0],
        "Supply_Trend_Pct": -40.7,
        "Pressure_Type": "Emerging Supply Risk",
        "Cost_Factor": "Low-Moderate Cost",
        "Where_It_Breaks": "Upstream Supply Chain"
    }
]

df_hero = pd.DataFrame(summary_data)

# Toggle for chart view mode
chart_mode = st.radio(
    "Select Graph View:",
    ["Side-by-Side Diagnostic Comparison (All 4 Foods)", "Multi-Year Supply Trajectories (2010 - 2023)"],
    horizontal=True
)

if chart_mode == "Side-by-Side Diagnostic Comparison (All 4 Foods)":
    fig_hero = go.Figure()
    
    # Bar 1: Women's Consumption Rate (%)
    fig_hero.add_trace(go.Bar(
        x=df_hero["Food Group"],
        y=df_hero["Consumption_Pct"],
        name="Women's Consumption Rate (%)",
        marker_color="#3B82F6",
        text=df_hero["Consumption_Pct"].round(1).astype(str) + "%",
        textposition="auto"
    ))
    
    # Bar 2: 10-Year National Supply Trend (%)
    fig_hero.add_trace(go.Bar(
        x=df_hero["Food Group"],
        y=df_hero["Supply_Trend_Pct"],
        name="10-Yr National Supply Trend (%)",
        marker_color=["#DC2626" if val < 0 else "#16A34A" for val in df_hero["Supply_Trend_Pct"]],
        text=df_hero["Supply_Trend_Pct"].astype(str) + "%",
        textposition="auto"
    ))
    
    fig_hero.update_layout(
        title=dict(
            text=f"Comparison of National Food Supply Trends vs. Women's Plate Consumption ({location_filter})",
            font=dict(size=16)
        ),
        barmode="group",
        yaxis=dict(title=dict(text="Percentage (%)")),
        xaxis=dict(title=dict(text="Nutritious Food Category")),
        legend=dict(x=0.01, y=0.98, orientation="h"),
        template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=450
    )
    st.plotly_chart(fig_hero, use_container_width=True)

else:
    # Time Series Trajectories
    fig_ts = go.Figure()
    fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Dairy_Supply"], mode="lines+markers", name="🥛 Dairy Supply (g/day)", line=dict(color="#DC2626", width=3)))
    fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Pulses_Supply"], mode="lines+markers", name="🫘 Pulses Supply (g/day)", line=dict(color="#D97706", width=3)))
    fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Eggs_Supply"], mode="lines+markers", name="🥚 Eggs Supply (g/day)", line=dict(color="#2563EB", width=3)))
    fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Vegetables_Supply"], mode="lines+markers", name="🥬 Vegetables Supply (g/day)", line=dict(color="#059669", width=3)))
    
    fig_ts.update_layout(
        title=dict(text="13-Year National Food Availability Trajectory in Ghana (2010 - 2023)", font=dict(size=16)),
        xaxis=dict(title=dict(text="Year")),
        yaxis=dict(title=dict(text="Food Availability (g/capita/day)")),
        template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        height=450
    )
    st.plotly_chart(fig_ts, use_container_width=True)

st.markdown("---")

# -------------------------------------------------------------
# DETAILS IN 1 VIEW: THE 4 BOTTLENECK DIAGNOSTIC CARDS
# -------------------------------------------------------------
st.subheader("📋 Clear Diagnostic Breakdown: Same Dietary Gap, 4 Distinct Bottlenecks")
st.markdown("HerPlate proves that low consumption is caused by **fundamentally different structural breakdowns** across food groups:")

c1, c2, c3, c4 = st.columns(4)

# Card 1: Dairy
with c1:
    d_pct = df_hero.loc[df_hero["Food Group"] == "🥛 Dairy Products", "Consumption_Pct"].values[0]
    st.markdown(f"""
    <div class='detail-card'>
        <h4>🥛 Dairy Products</h4>
        <span class='badge-red'>Convergent Pressure</span>
        <hr style='margin:0.8rem 0;'>
        <p><b>Plate Consumption:</b> <span style='font-size:1.2rem; font-weight:700;'>{d_pct:.1f}%</span></p>
        <p><b>10-Yr National Supply:</b> <span style='color:#DC2626; font-weight:700;'>-24.4%</span></p>
        <p><b>Cost Category:</b> High (ASF Basket)</p>
        <p class='break-point'>❌ Where It Breaks:</p>
        <p class='card-text-muted'>Tripartite failure: High prices + declining national production + cold-chain gaps.</p>
        <p class='solution-point'>💡 Targeted Solution:</p>
        <p class='card-text-body'>Long-term infrastructure investment & dairy cold-chain subsidies.</p>
    </div>
    """, unsafe_allow_html=True)

# Card 2: Pulses
with c2:
    p_pct = df_hero.loc[df_hero["Food Group"] == "🫘 Pulses (Beans & Peas)", "Consumption_Pct"].values[0]
    st.markdown(f"""
    <div class='detail-card'>
        <h4>🫘 Pulses (Legumes)</h4>
        <span class='badge-orange'>Supply / Diversity Pressure</span>
        <hr style='margin:0.8rem 0;'>
        <p><b>Plate Consumption:</b> <span style='font-size:1.2rem; font-weight:700;'>{p_pct:.1f}%</span></p>
        <p><b>10-Yr National Supply:</b> <span style='color:#DC2626; font-weight:700;'>-39.4%</span></p>
        <p><b>Cost Category:</b> Low Relative Cost</p>
        <p class='break-point'>❌ Where It Breaks:</p>
        <p class='card-text-muted'>Upstream Agricultural Supply. Prices are affordable, but production is shrinking.</p>
        <p class='solution-point'>💡 Targeted Solution:</p>
        <p class='card-text-body'>Legume seed subsidies & drought-resilient cowpea farming support.</p>
    </div>
    """, unsafe_allow_html=True)

# Card 3: Eggs
with c3:
    e_pct = df_hero.loc[df_hero["Food Group"] == "🥚 Eggs", "Consumption_Pct"].values[0]
    st.markdown(f"""
    <div class='detail-card'>
        <h4>🥚 Eggs</h4>
        <span class='badge-blue'>Access Beyond Supply</span>
        <hr style='margin:0.8rem 0;'>
        <p><b>Plate Consumption:</b> <span style='font-size:1.2rem; font-weight:700;'>{e_pct:.1f}%</span></p>
        <p><b>10-Yr National Supply:</b> <span style='color:#16A34A; font-weight:700;'>+3.9% (Stable)</span></p>
        <p><b>Cost Category:</b> Moderate Market Margin</p>
        <p class='break-point'>❌ Where It Breaks:</p>
        <p class='card-text-muted'>Market Distribution & Intra-Household allocation. National supply is available!</p>
        <p class='solution-point'>💡 Targeted Solution:</p>
        <p class='card-text-body'>Direct vouchers for pregnant women & local market distribution networks.</p>
    </div>
    """, unsafe_allow_html=True)

# Card 4: Vegetables
with c4:
    v_pct = df_hero.loc[df_hero["Food Group"] == "🥬 Vegetables", "Consumption_Pct"].values[0]
    st.markdown(f"""
    <div class='detail-card'>
        <h4>🥬 Vegetables</h4>
        <span class='badge-green'>Emerging Supply Risk</span>
        <hr style='margin:0.8rem 0;'>
        <p><b>Plate Consumption:</b> <span style='font-size:1.2rem; font-weight:700;'>{v_pct:.1f}%</span></p>
        <p><b>10-Yr National Supply:</b> <span style='color:#DC2626; font-weight:700;'>-40.7%</span></p>
        <p><b>Cost Category:</b> Low-Moderate Cost</p>
        <p class='break-point'>❌ Where It Breaks:</p>
        <p class='card-text-muted'>Impending Upstream Risk. Consumption is currently higher, but supply is crashing.</p>
        <p class='solution-point'>💡 Targeted Solution:</p>
        <p class='card-text-body'>Preventative agricultural support for leafy greens (*Kontomire*) & irrigation.</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# POLICY SUMMARY BANNER FOR JUDGES
# -------------------------------------------------------------
st.info("""
🎯 **Core Takeaway for Policymakers & Judges:**
* **Don't treat every dietary gap as a farming problem:** Giving chicken-farming subsidies won't fix egg access if the break is in local market distribution and intra-household allocation.
* **Don't treat every dietary gap as a price problem:** Pulses are affordable, but national production is shrinking fast.
* **HerPlate Ghana** isolates where deeper intervention should begin, ensuring agrifood investments deliver maximum impact for women's health.
""")
