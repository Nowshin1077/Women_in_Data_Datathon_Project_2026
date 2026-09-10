import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# Set Streamlit page configuration
st.set_page_config(
    page_title="HerPlate Ghana: Food System Diagnostic",
    page_icon="🇬🇭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper function to load datasets
@st.cache_data
def load_data():
    cahd_path = "cleaned_ghana_cahd.csv"
    fbs_path = "cleaned_ghana_fbs.csv"
    mddw_path = "cleaned_ghana_mddw.csv"
    
    # Check current directory and scratch
    for path in [cahd_path, fbs_path, mddw_path]:
        if not os.path.exists(path):
            scratch_path = os.path.join("/workspace/scratch", path)
            if os.path.exists(scratch_path):
                if path == cahd_path: cahd_path = scratch_path
                elif path == fbs_path: fbs_path = scratch_path
                elif path == mddw_path: mddw_path = scratch_path

    if not (os.path.exists(cahd_path) and os.path.exists(fbs_path) and os.path.exists(mddw_path)):
        st.error("⚠️ Data files not found. Please run `process_github_data.py` first!")
        st.stop()
        
    cahd = pd.read_csv(cahd_path)
    fbs = pd.read_csv(fbs_path)
    mddw = pd.read_csv(mddw_path)
    
    # Clean headers
    for df in [cahd, fbs, mddw]:
        df.columns = df.columns.str.replace('\ufeff', '', regex=False).str.strip()
        
    # Standardize MDD-W Food Group column name
    for possible_col in ["Food_Group", "Food Group", "food_group", "Item", "Indicator"]:
        if possible_col in mddw.columns:
            mddw.rename(columns={possible_col: "Food_Group"}, inplace=True)
            break
            
    return cahd, fbs, mddw

cahd_df, fbs_df, mddw_df = load_data()

# Helper for safe value retrieval
def get_consumption_val(df, group_keyword, col_name, fallback_val):
    if "Food_Group" in df.columns and col_name in df.columns:
        match = df[df["Food_Group"].str.contains(group_keyword, case=False, na=False)]
        if not match.empty:
            return float(match[col_name].values[0])
    return fallback_val

# -------------------------------------------------------------
# SIDEBAR CONTROLS & INTERACTIVE SCENARIO
# -------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/emoji/96/000000/ghana-emoji.png", width=60)
st.sidebar.title("🇬🇭 HerPlate Ghana")
st.sidebar.caption("Decision-Support System for Maternal Agrifood Reform")

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

st.sidebar.divider()
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
st.title("🇬🇭 HerPlate Ghana: Food System Bottleneck Diagnostic")
st.markdown("**Core Question:** *Where is the pathway from Ghana's food system to women's plates breaking?*")

st.write("")

# Top 4 KPI Cards (Using Native Streamlit Containers & Metrics)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    with st.container(border=True):
        st.metric(
            label="UNAFFORDABLE HEALTHY DIET",
            value="64.7%",
            help="FAOSTAT Cost & Affordability Baseline for Ghana (2022)"
        )

with kpi2:
    with st.container(border=True):
        st.metric(
            label="ANIMAL FOOD BASKET SHARE",
            value="41.1%",
            help="Largest Cost Contributor in Healthy Diet Basket"
        )

with kpi3:
    with st.container(border=True):
        st.metric(
            label="TARGET POPULATION",
            value="WRA 15-49",
            help="Women of Reproductive Age in Ghana"
        )

with kpi4:
    with st.container(border=True):
        st.metric(
            label="CORE ANALYTICAL THESIS",
            value="4 Bottlenecks",
            delta="Same Dietary Gap",
            delta_color="normal"
        )

st.write("")

# -------------------------------------------------------------
# 1 HERO GRAPH: THE BOTTLENECK DIAGNOSTIC CHART
# -------------------------------------------------------------
st.subheader("📊 The Diagnostic Overview: Supply Trend vs. Women's Plate Consumption")

# Extract real values from MDD-W
dairy_val = get_consumption_val(mddw_df, "dairy", target_col, 15.4) + (asf_subsidy * 0.2)
pulse_val = get_consumption_val(mddw_df, "pulse", target_col, 23.5)
egg_val = get_consumption_val(mddw_df, "egg", target_col, 27.6) + (asf_subsidy * 0.3)
veg_val = get_consumption_val(mddw_df, "veg", target_col, 51.5)

summary_data = [
    {
        "Food Group": "🥛 Dairy Products",
        "Consumption_Pct": dairy_val,
        "Supply_Trend_Pct": -24.4,
        "Pressure_Type": "Convergent Pressure",
        "Cost_Factor": "Very High (ASF Basket)",
        "Where_It_Breaks": "Production ➔ Market ➔ Household"
    },
    {
        "Food Group": "🫘 Pulses (Beans & Peas)",
        "Consumption_Pct": pulse_val,
        "Supply_Trend_Pct": -39.4,
        "Pressure_Type": "Supply/Diversity Pressure",
        "Cost_Factor": "Low Relative Cost",
        "Where_It_Breaks": "Production / National Supply"
    },
    {
        "Food Group": "🥚 Eggs",
        "Consumption_Pct": egg_val,
        "Supply_Trend_Pct": 3.9,
        "Pressure_Type": "Access Beyond Supply",
        "Cost_Factor": "Moderate / Market Margin",
        "Where_It_Breaks": "Market Distribution ➔ Plate"
    },
    {
        "Food Group": "🥬 Vegetables",
        "Consumption_Pct": veg_val,
        "Supply_Trend_Pct": -40.7,
        "Pressure_Type": "Emerging Supply Risk",
        "Cost_Factor": "Low-Moderate Cost",
        "Where_It_Breaks": "Upstream Supply Chain"
    }
]

df_hero = pd.DataFrame(summary_data)

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
        marker_color="#2563EB", # Vibrant Blue that works on dark/light
        text=df_hero["Consumption_Pct"].round(1).astype(str) + "%",
        textposition="auto"
    ))
    
    # Bar 2: 10-Year National Supply Trend (%)
    fig_hero.add_trace(go.Bar(
        x=df_hero["Food Group"],
        y=df_hero["Supply_Trend_Pct"],
        name="10-Yr National Supply Trend (%)",
        marker_color=["#EF4444" if val < 0 else "#10B981" for val in df_hero["Supply_Trend_Pct"]],
        text=df_hero["Supply_Trend_Pct"].astype(str) + "%",
        textposition="auto"
    ))
    
    fig_hero.update_layout(
        title=dict(
            text=f"National Food Supply Trends vs. Women's Plate Consumption ({location_filter})"
        ),
        barmode="group",
        yaxis=dict(title=dict(text="Percentage (%)")),
        xaxis=dict(title=dict(text="Nutritious Food Category")),
        legend=dict(x=0.01, y=0.98, orientation="h"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450
    )
    st.plotly_chart(fig_hero, use_container_width=True)

else:
    fig_ts = go.Figure()
    if "Dairy_Supply" in fbs_df.columns:
        fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Dairy_Supply"], mode="lines+markers", name="🥛 Dairy Supply", line=dict(color="#EF4444", width=3)))
    if "Pulses_Supply" in fbs_df.columns:
        fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Pulses_Supply"], mode="lines+markers", name="🫘 Pulses Supply", line=dict(color="#F59E0B", width=3)))
    if "Eggs_Supply" in fbs_df.columns:
        fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Eggs_Supply"], mode="lines+markers", name="🥚 Eggs Supply", line=dict(color="#3B82F6", width=3)))
    if "Vegetables_Supply" in fbs_df.columns:
        fig_ts.add_trace(go.Scatter(x=fbs_df["Year"], y=fbs_df["Vegetables_Supply"], mode="lines+markers", name="🥬 Vegetables Supply", line=dict(color="#10B981", width=3)))
    
    fig_ts.update_layout(
        title=dict(text="13-Year National Food Availability Trajectory in Ghana (2010 - 2023)"),
        xaxis=dict(title=dict(text="Year")),
        yaxis=dict(title=dict(text="Food Availability (g/capita/day)")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=450
    )
    st.plotly_chart(fig_ts, use_container_width=True)

st.divider()

# -------------------------------------------------------------
# DETAILS IN 1 VIEW: THE 4 BOTTLENECK DIAGNOSTIC CARDS
# Native Streamlit containers: 100% Light/Dark/System Adaptable
# -------------------------------------------------------------
st.subheader("📋 Clear Diagnostic Breakdown: Same Dietary Gap, 4 Distinct Bottlenecks")
st.write("HerPlate proves that low consumption is caused by **fundamentally different structural breakdowns** across food groups:")

c1, c2, c3, c4 = st.columns(4)

# Card 1: Dairy
with c1:
    with st.container(border=True):
        st.markdown("### 🥛 Dairy")
        st.caption("🔴 **Convergent Pressure**")
        st.divider()
        st.markdown(f"**Plate Consumption:** `{dairy_val:.1f}%`")
        st.markdown("**10-Yr Supply Trend:** :red[-24.4%]")
        st.markdown("**Cost Category:** High (ASF Basket)")
        st.write("")
        st.markdown(":red[**❌ Where It Breaks:**]")
        st.write("Tripartite failure: High prices + declining national production + cold-chain gaps.")
        st.write("")
        st.markdown(":green[**💡 Targeted Solution:**]")
        st.write("Long-term infrastructure investment & dairy cold-chain subsidies.")

# Card 2: Pulses
with c2:
    with st.container(border=True):
        st.markdown("### 🫘 Pulses")
        st.caption("🟠 **Supply / Diversity Pressure**")
        st.divider()
        st.markdown(f"**Plate Consumption:** `{pulse_val:.1f}%`")
        st.markdown("**10-Yr Supply Trend:** :red[-39.4%]")
        st.markdown("**Cost Category:** Low Relative Cost ($0.39 PPP)")
        st.write("")
        st.markdown(":red[**❌ Where It Breaks:**]")
        st.write("Upstream Agricultural Supply. Prices are affordable, but production is shrinking.")
        st.write("")
        st.markdown(":green[**💡 Targeted Solution:**]")
        st.write("Legume seed subsidies & drought-resilient cowpea farming support.")

# Card 3: Eggs
with c3:
    with st.container(border=True):
        st.markdown("### 🥚 Eggs")
        st.caption("🔵 **Access Beyond Supply**")
        st.divider()
        st.markdown(f"**Plate Consumption:** `{egg_val:.1f}%`")
        st.markdown("**10-Yr Supply Trend:** :green[+3.9% (Stable)]")
        st.markdown("**Cost Category:** Moderate Market Margin")
        st.write("")
        st.markdown(":red[**❌ Where It Breaks:**]")
        st.write("Market Distribution & Intra-Household allocation. National supply is available!")
        st.write("")
        st.markdown(":green[**💡 Targeted Solution:**]")
        st.write("Direct vouchers for pregnant women & local market distribution networks.")

# Card 4: Vegetables
with c4:
    with st.container(border=True):
        st.markdown("### 🥬 Vegetables")
        st.caption("🟢 **Emerging Supply Risk**")
        st.divider()
        st.markdown(f"**Plate Consumption:** `{veg_val:.1f}%`")
        st.markdown("**10-Yr Supply Trend:** :red[-40.7%]")
        st.markdown("**Cost Category:** Low-Moderate Cost")
        st.write("")
        st.markdown(":red[**❌ Where It Breaks:**]")
        st.write("Impending Upstream Risk. Consumption is currently higher, but supply is crashing.")
        st.write("")
        st.markdown(":green[**💡 Targeted Solution:**]")
        st.write("Preventative agricultural support for leafy greens (*Kontomire*) & irrigation.")

st.write("")

# Policy Summary Banner
st.info("""
🎯 **Core Takeaway for Policymakers & Judges:**
* **Don't treat every dietary gap as a farming problem:** Giving chicken-farming subsidies won't fix egg access if the break is in local market distribution and intra-household allocation.
* **Don't treat every dietary gap as a price problem:** Pulses are affordable, but national production is shrinking fast.
* **HerPlate Ghana** isolates where deeper intervention should begin, ensuring agrifood investments deliver maximum impact for women's health.
""")
