# ==============================================================================
# HERPLATE GHANA
# Interactive Nutrition & Food Affordability Decision-Support App
# ==============================================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="HerPlate Ghana",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ==============================================================================
# 2. CUSTOM STYLING
# ==============================================================================

st.markdown(
    """
    <style>
    .main {
        padding-top: 1rem;
    }

    .hero-text {
        padding: 1rem 0 1rem 0;
    }

    .hero-text h1 {
        font-size: 3rem;
        margin-bottom: 0.3rem;
        color: var(--text-color);
    }

    .hero-text p {
        font-size: 1.15rem;
        color: var(--text-color);
        opacity: 0.8;
    }

    .ghana-accent {
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--text-color);
    }

    /* Subtle grey container adapting cleanly to light/dark themes */
    .metric-card, .insight-card {
        background-color: rgba(128, 128, 128, 0.08);
        border: 1px solid rgba(128, 128, 128, 0.2);
        padding: 1.2rem;
        border-radius: 12px;
        color: var(--text-color);
    }

    .metric-card {
        text-align: center;
        min-height: 115px;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-color);
    }

    .metric-label {
        font-size: 0.9rem;
        color: var(--text-color);
        opacity: 0.75;
    }

    .insight-card {
        margin-bottom: 1rem;
    }

    .insight-card h4 {
        color: var(--text-color);
        margin-top: 0;
    }

    .insight-card p {
        color: var(--text-color);
        opacity: 0.85;
        margin-bottom: 0;
    }

    .small-note {
        color: var(--text-color);
        opacity: 0.65;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ==============================================================================
# 3. CORE DATA
# ==============================================================================

# ------------------------------------------------------------------------------
# MDD-W achievement
# ------------------------------------------------------------------------------

mdd_w_national = 49.9


# ------------------------------------------------------------------------------
# Food supply changes, 2010 to 2023
# ------------------------------------------------------------------------------

food_supply_change = pd.DataFrame({
    "Food Group": [
        "Vegetables",
        "Pulses",
        "Milk",
        "Oils & fats",
        "Fruits",
        "Eggs",
        "Fish",
        "Cereals",
        "Nuts & seeds",
        "Meat"
    ],
    "Change (%)": [
        -40.72,
        -39.33,
        -24.36,
        -15.54,
        -6.27,
        3.92,
        6.69,
        12.73,
        28.73,
        32.04
    ]
})


# ------------------------------------------------------------------------------
# MDD-W consumption by geographic level
# ------------------------------------------------------------------------------

mdd_food_groups = pd.DataFrame({
    "Food Group": [
        "Eggs",
        "Meat, poultry & fish",
        "Dairy",
        "Dark green leafy vegetables",
        "Other vegetables",
        "Pulses",
        "Nuts & seeds",
        "Vitamin A fruits & vegetables",
        "Other fruits"
    ],
    "National": [
        26.5,
        67.5,
        37.3,
        52.4,
        66.8,
        48.0,
        37.5,
        42.1,
        35.7
    ],
    "Rural": [
        18.3,
        61.4,
        29.8,
        49.1,
        63.7,
        43.2,
        31.9,
        37.6,
        30.4
    ],
    "Urban": [
        34.7,
        73.9,
        45.8,
        55.7,
        70.1,
        53.1,
        43.2,
        46.7,
        41.3
    ]
})


# ------------------------------------------------------------------------------
# Protein substitution model
# ------------------------------------------------------------------------------

iron_coefficients = {
    "Animal protein": 0.02,
    "Plant protein": 0.054
}

baseline_animal = 150
baseline_plant = 30


# ------------------------------------------------------------------------------
# Healthy diet affordability model
# ------------------------------------------------------------------------------

baseline_diet_cost = 4.28
intervention_diet_cost = 3.75
population = 33.5  # million
baseline_affordability = 33.4
intervention_affordability = 40.0
additional_people = 2.2  # million


# ==============================================================================
# 4. HEADER / HERO
# ==============================================================================

# Small Ghana visual accent
st.markdown(
    """
    <div class="ghana-accent">
        🇬🇭 HerPlate Ghana
    </div>
    """,
    unsafe_allow_html=True
)

hero_col1, hero_col2 = st.columns([1.05, 1])

with hero_col1:
    st.markdown(
        """
        <div class="hero-text">
            <h1>
                What is on the plate,<br>
                what is missing,<br>
                and what can we change?
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        "An interactive decision-support framework connecting "
        "dietary diversity, food availability and healthy diet affordability."
    )


with hero_col2:
    st.image(
        "assets/ghana_food_plate.png",
        use_container_width=True
    )


# ==============================================================================
# 5. KEY METRICS
# ==============================================================================

st.markdown("### The Ghana food story")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">49.9%</div>
            <div class="metric-label">
                Women achieving MDD-W
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m2:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">-39.3%</div>
            <div class="metric-label">
                Pulse supply
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m3:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">-40.7%</div>
            <div class="metric-label">
                Vegetable supply
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with m4:
    st.markdown(
        """
        <div class="metric-card">
            <div class="metric-value">+32.0%</div>
            <div class="metric-label">
                Meat supply
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown("---")


# ==============================================================================
# 6. NAVIGATION
# ==============================================================================

tab1, tab2, tab3 = st.tabs([
    "🔎 Diagnose",
    "📍 Understand",
    "🥗 Simulate"
])


# ==============================================================================
# TAB 1: DIAGNOSE
# ==============================================================================

with tab1:

    st.markdown("## What changed in Ghana's food supply?")

    st.write(
        "Between 2010 and 2023, Ghana's national food supply became more "
        "concentrated in cereals and meat, while pulses and vegetables declined."
    )

    fig = px.bar(
        food_supply_change,
        x="Change (%)",
        y="Food Group",
        orientation="h",
        title="Change in food supply, 2010-2023",
        labels={"Change (%)": "Change (%)"},
        color_discrete_sequence=["#7EB2DD"]
    )

    fig.add_vline(
        x=0,
        line_width=1,
        line_color="gray"
    )

    fig.update_layout(
        height=500,
        yaxis={"categoryorder": "total ascending"},
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div class="insight-card">
                <h4>🌱 Pulses declined</h4>
                <p>
                    Pulse supply fell by <strong>39.3%</strong>,
                    driven primarily by a <strong>42.1%</strong>
                    decline in beans.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div class="insight-card">
                <h4>🥩 Meat increased</h4>
                <p>
                    Meat supply increased by <strong>32.0%</strong>
                    over the same period.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.info(
        "Food Balance data describes national food availability, "
        "not individual food consumption. We therefore interpret it "
        "alongside dietary diversity indicators."
    )


# ==============================================================================
# TAB 2: UNDERSTAND
# ==============================================================================

with tab2:

    st.markdown("## Who is eating what?")

    st.write(
        "Dietary diversity differs across geographic groups. "
        "Explore how consumption varies between rural and urban women."
    )

    selected_food = st.selectbox(
        "Select a food group",
        mdd_food_groups["Food Group"].tolist()
    )

    selected_row = mdd_food_groups[
        mdd_food_groups["Food Group"] == selected_food
    ].iloc[0]

    comparison = pd.DataFrame({
        "Geographic Level": [
            "Rural",
            "National",
            "Urban"
        ],
        "Women consuming (%)": [
            selected_row["Rural"],
            selected_row["National"],
            selected_row["Urban"]
        ]
    })

    fig = px.bar(
        comparison,
        x="Geographic Level",
        y="Women consuming (%)",
        text="Women consuming (%)",
        title=f"{selected_food} consumption by geographic level",
        color_discrete_sequence=["#7EB2DD"]
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside"
    )

    fig.update_layout(
        yaxis_title="Women consuming (%)",
        xaxis_title="",
        yaxis_range=[0, 100],
        height=450,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    gap = selected_row["Urban"] - selected_row["Rural"]

    st.markdown(
        f"""
        <div class="insight-card">
            <h4>📊 The rural-urban gap</h4>
            <p>
                For <strong>{selected_food.lower()}</strong>,
                the urban consumption rate is
                <strong>{gap:.1f} percentage points</strong>
                higher than the rural rate.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### A closer look at eggs")

    egg_rural = 18.3
    egg_urban = 34.7

    e1, e2, e3 = st.columns(3)

    with e1:
        st.metric(
            "Rural women",
            f"{egg_rural:.1f}%"
        )

    with e2:
        st.metric(
            "Urban women",
            f"{egg_urban:.1f}%"
        )

    with e3:
        st.metric(
            "Urban-rural gap",
            f"+{egg_urban - egg_rural:.1f} pp"
        )

    st.caption(
        "MDD-W measures whether women aged 15-49 consumed foods "
        "from at least 5 of 10 core food groups."
    )


# ==============================================================================
# TAB 3: SIMULATE
# ==============================================================================

with tab3:

    st.markdown("## What could we change?")

    st.write(
        "Explore two illustrative intervention scenarios: "
        "protein substitution and healthy diet affordability."
    )


    # ==========================================================================
    # PROTEIN SUBSTITUTION
    # ==========================================================================

    st.markdown("### 🫘 Protein substitution")

    substitution = st.slider(
        "Replace part of the animal-source portion with plant protein",
        min_value=0,
        max_value=100,
        value=50,
        step=10,
        format="%d%%"
    )

    animal_amount = baseline_animal * (1 - substitution / 100)

    plant_amount = (
        baseline_plant
        + baseline_animal * (substitution / 100)
    )


    # Baseline iron
    baseline_iron = (
        baseline_animal * iron_coefficients["Animal protein"]
        + baseline_plant * iron_coefficients["Plant protein"]
    )


    # Scenario iron
    scenario_iron = (
        animal_amount * iron_coefficients["Animal protein"]
        + plant_amount * iron_coefficients["Plant protein"]
    )

    iron_change = (
        (scenario_iron - baseline_iron)
        / baseline_iron
        * 100
    )

    substitution_df = pd.DataFrame({
        "Scenario": [
            "Baseline",
            f"{substitution}% substitution"
        ],
        "Animal protein (g)": [
            baseline_animal,
            animal_amount
        ],
        "Plant protein (g)": [
            baseline_plant,
            plant_amount
        ]
    })

    fig = px.bar(
        affordability_df,
        x="Scenario",
        y="Cost (PPP/day)",
        text="Cost (PPP/day)",
        title="Healthy diet cost",
        color_discrete_sequence=["#7EB2DD"]
    )

    fig.update_traces(
        texttemplate="$%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        height=400,
        yaxis_title="PPP dollars per day",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    p1, p2, p3 = st.columns(3)

    with p1:
        st.metric(
            "Animal protein",
            f"{animal_amount:.0f} g"
        )

    with p2:
        st.metric(
            "Plant protein",
            f"{plant_amount:.0f} g"
        )

    with p3:
        st.metric(
            "Estimated iron change",
            f"{iron_change:+.1f}%"
        )

    st.caption(
        "Illustrative scenario using assumed nutrient coefficients. "
        "The 50% scenario is an example, not a mathematically optimal diet."
    )

    st.markdown("---")


    # ==========================================================================
    # HEALTHY DIET AFFORDABILITY
    # ==========================================================================

    st.markdown("### 💰 Healthy diet affordability")

    diet_cost = st.slider(
        "Explore healthy diet cost (PPP/day)",
        min_value=3.50,
        max_value=4.50,
        value=3.75,
        step=0.05
    )


    # Linear interpolation between the baseline and intervention scenarios.
    if diet_cost >= baseline_diet_cost:

        estimated_affordability = baseline_affordability

    elif diet_cost <= intervention_diet_cost:

        estimated_affordability = intervention_affordability

    else:

        cost_reduction = (
            baseline_diet_cost - diet_cost
        ) / (
            baseline_diet_cost - intervention_diet_cost
        )

        estimated_affordability = (
            baseline_affordability
            + cost_reduction
            * (
                intervention_affordability
                - baseline_affordability
            )
        )

    estimated_affordability = np.clip(
        estimated_affordability,
        0,
        100
    )

    additional_people_estimated = (
        population
        * (
            estimated_affordability
            - baseline_affordability
        )
        / 100
    )

    affordability_df = pd.DataFrame({
        "Scenario": [
            "Current",
            "Illustrative intervention"
        ],
        "Cost (PPP/day)": [
            baseline_diet_cost,
            intervention_diet_cost
        ]
    })

    fig = px.bar(
        affordability_df,
        x="Scenario",
        y="Cost (PPP/day)",
        text="Cost (PPP/day)",
        title="Healthy diet cost"
    )

    fig.update_traces(
        texttemplate="$%{text:.2f}",
        textposition="outside"
    )

    fig.update_layout(
        height=400,
        yaxis_title="PPP dollars per day"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    a1, a2, a3 = st.columns(3)

    with a1:
        st.metric(
            "Current cost",
            "$4.28 PPP/day"
        )

    with a2:
        st.metric(
            "Scenario cost",
            f"${diet_cost:.2f} PPP/day"
        )

    with a3:
        st.metric(
            "Estimated affordability",
            f"{estimated_affordability:.1f}%"
        )

    if diet_cost <= intervention_diet_cost:

        st.success(
            "At the illustrative $3.75 PPP/day scenario, "
            "estimated affordability increases from 33.4% to 40.0%, "
            "equivalent to approximately 2.2 million additional people."
        )

    st.caption(
        "Scenario simulation based on assumed income-distribution "
        "parameters. It should not be interpreted as a forecast."
    )


# ==============================================================================
# 7. FINAL TAKEAWAY
# ==============================================================================

st.markdown("---")

st.markdown("## From data to action")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(
        """
        <div class="insight-card">
            <h4>🔎 Diagnose</h4>
            <p>
                Identify changes in Ghana's national food supply.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        """
        <div class="insight-card">
            <h4>📍 Understand</h4>
            <p>
                Explore dietary diversity across population groups.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        """
        <div class="insight-card">
            <h4>🥗 Simulate</h4>
            <p>
                Explore how potential interventions could affect
                affordability.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# Clean Streamlit markdown instead of raw HTML
st.markdown("### A diverse diet is not only a nutrition problem.")

st.markdown(
    "It is also an availability, access and affordability problem."
)

st.markdown(
    "**HerPlate Ghana** turns those signals into an interactive "
    "framework for exploring solutions."
)


st.caption(
    "HerPlate Ghana | Women in Data 2026 Datathon"
)