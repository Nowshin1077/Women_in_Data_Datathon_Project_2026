# HERPLATE GHANA
# Final Exploratory Data Analysis
# Women in Data Datathon 2026

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==============================================================================
# 1. SETUP
# ==============================================================================


print("=" * 80)
print("HERPLATE GHANA - EXPLORATORY DATA ANALYSIS")
print("Women in Data Datathon 2026")
print("=" * 80)

"""
BASE_DIR = Path(__file__).resolve().parent

mdd_file = BASE_DIR / "dataset" / "FAOSTAT_MDDW_Ghana.csv"
fb_file = BASE_DIR / "dataset" / "FAOSTAT_FB_Ghana.csv"

"""

BASE_DIR = Path(__file__).resolve().parent

# --- ADDED: Auto-detect correct dataset folder location or GitHub fallback ---
if not (BASE_DIR / "dataset").exists():
  if (BASE_DIR.parent / "dataset").exists():
    BASE_DIR = BASE_DIR.parent
  elif (BASE_DIR / "FAOSTAT_Dataset").exists():
    BASE_DIR = BASE_DIR / "FAOSTAT_Dataset"
  elif (BASE_DIR.parent / "FAOSTAT_Dataset").exists():
    BASE_DIR = BASE_DIR.parent / "FAOSTAT_Dataset"

# If local dataset folder still does not exist, point to GitHub raw data
GITHUB_RAW = "https://raw.githubusercontent.com/Nowshin1077/Women_in_Data_Datathon_Project_2026/main/dataset"
if not (BASE_DIR / "dataset").exists() and not (
    BASE_DIR / "FAOSTAT_MDDW_Ghana.csv"
).exists():

  class RemoteDatasetPath:

    def __init__(self, filename):
      self.url = f"{GITHUB_RAW}/{filename}"

    def __truediv__(self, other):
      return RemoteDatasetPath(other)

    def exists(self):
      return True

    def __fspath__(self):
      return self.url

    def __str__(self):
      return self.url

  BASE_DIR = RemoteDatasetPath("")
# -----------------------------------------------------------------------------

mdd_file = BASE_DIR / "dataset" / "FAOSTAT_MDDW_Ghana.csv"
fb_file = BASE_DIR / "dataset" / "FAOSTAT_FB_Ghana.csv"


if not mdd_file.exists():
  raise FileNotFoundError(f"MDD-W dataset not found at: {mdd_file}")


if not fb_file.exists():
  raise FileNotFoundError(f"Food Balances dataset not found at: {fb_file}")

# ==============================================================================
# 2. LOAD MDD-W DATA
# ==============================================================================

df_mdd = pd.read_csv(mdd_file)

print("\nMDD-W dataset loaded successfully.")
print(f"Rows: {len(df_mdd)}")
print(f"Columns: {len(df_mdd.columns)}")

# ==============================================================================
# 3. MDD-W DATA QUALITY CHECK
# ==============================================================================

print("\n" + "=" * 80)
print("MDD-W DATA QUALITY CHECK")
print("=" * 80)

print("\nMissing values:")
print(df_mdd.isnull().sum())

print("\nGeographic levels:")
print(
    df_mdd["Geographic Level"]
    .value_counts()
    .to_string()
)

print("\nIndicators:")
print(
    df_mdd[["Indicator Code", "Indicator"]]
    .drop_duplicates()
    .to_string(index=False)
)

# ==============================================================================
# 4. MDD-W ACHIEVEMENT BY GEOGRAPHIC LEVEL
# ==============================================================================

print("\n" + "=" * 80)
print("MDD-W ACHIEVEMENT BY GEOGRAPHIC LEVEL")
print("=" * 80)

mdd_achievement = df_mdd[
    df_mdd["Indicator Code"] == 6211
].copy()

mdd_achievement = mdd_achievement[
    ["Geographic Level", "Value"]
].sort_values("Geographic Level")

print("\nPercentage of women achieving MDD-W:")
print(mdd_achievement.to_string(index=False))

# ==============================================================================
# 5. FOOD GROUP CONSUMPTION BY GEOGRAPHIC LEVEL
# ==============================================================================

print("\n" + "=" * 80)
print("FOOD GROUP CONSUMPTION BY GEOGRAPHIC LEVEL")
print("=" * 80)

food_group_data = df_mdd[
    df_mdd["Indicator Code"] == 6212
].copy()

food_group_pivot = food_group_data.pivot_table(
    index="Food Group",
    columns="Geographic Level",
    values="Value",
    aggfunc="first"
)

print("\nFood group consumption:")
print(food_group_pivot.to_string())

# ==============================================================================
# 6. RURAL VS URBAN FOOD GROUP ANALYSIS
# ==============================================================================

print("\n" + "=" * 80)
print("RURAL VS URBAN FOOD GROUP ANALYSIS")
print("=" * 80)

if (
    "Rural" in food_group_pivot.columns
    and "Urban" in food_group_pivot.columns
):
    food_group_pivot["Urban - Rural"] = (
        food_group_pivot["Urban"] - food_group_pivot["Rural"]
    )

    rural_urban_gap = food_group_pivot[
        ["Rural", "Urban", "Urban - Rural"]
    ].sort_values("Urban - Rural", ascending=False)

    print("\nUrban-rural differences:")
    print(rural_urban_gap.to_string())

# ==============================================================================
# 7. MDD-W ACHIEVEMENT VISUALIZATION
# ==============================================================================

plt.figure(figsize=(8, 5))

plt.bar(
    mdd_achievement["Geographic Level"],
    mdd_achievement["Value"]
)

plt.title("Women Achieving Minimum Dietary Diversity (MDD-W)")

plt.xlabel("Geographic Level")
plt.ylabel("Women Achieving MDD-W (%)")
plt.ylim(0, 100)

for i, value in enumerate(mdd_achievement["Value"]):
    plt.text(
        i,
        value + 1,
        f"{value:.1f}%",
        ha="center"
    )

plt.tight_layout()
plt.show()

# ==============================================================================
# 8. FOOD GROUP CONSUMPTION VISUALIZATION
# ==============================================================================

plot_data = food_group_data[
    food_group_data["Food Group"] != "MDD-W Food groups"
].copy()

plt.figure(figsize=(12, 8))

for level in ["Rural", "Urban", "National"]:
    level_data = plot_data[
        plot_data["Geographic Level"] == level
    ]

    if not level_data.empty:
        plt.plot(
            level_data["Food Group"],
            level_data["Value"],
            marker="o",
            label=level
        )

plt.title("Food Group Consumption by Geographic Level")

plt.xlabel("Food Group")
plt.ylabel("Women Consuming Food Group (%)")

plt.xticks(rotation=75, ha="right")

plt.legend()
plt.tight_layout()
plt.show()

# ==============================================================================
# 9. GHANA VS KENYA MDD-W COMPARISON
# ==============================================================================

print("\n" + "=" * 80)
print("GHANA VS KENYA MDD-W COMPARISON")
print("=" * 80)

# Project reference values
ghana_mdd = 49.9
kenya_mdd = 48.5

comparison = pd.DataFrame({
    "Country": ["Ghana", "Kenya"],
    "Women achieving MDD-W (%)": [ghana_mdd, kenya_mdd]
})

print("\nMDD-W achievement:")
print(comparison.to_string(index=False))

difference = ghana_mdd - kenya_mdd

print(
    f"\nGhana is {difference:.1f} percentage points "
    f"higher than Kenya."
)

# Global reference values used in the project
global_meat_mdd = 67.5
global_dairy_mdd = 37.3

print("\nGlobal reference values:")

print(f"Global meat, poultry and fish consumption: {global_meat_mdd}%")

print(f"Global dairy consumption: {global_dairy_mdd}%")

# ==============================================================================
# 10. LOAD FOOD BALANCES DATA
# ==============================================================================

print("\n" + "=" * 80)
print("FOOD BALANCES DATASET")
print("=" * 80)

df_fb = pd.read_csv(fb_file)

print(f"\nShape: {df_fb.shape}")

print("\nColumns:")
print(df_fb.columns.tolist())

print("\nYear coverage:")
print(f"{df_fb['Year'].min()} to {df_fb['Year'].max()}")

print("\nElements:")
print(df_fb["Element"].value_counts().to_string())

print("\nUnits:")
print(df_fb["Unit"].value_counts().to_string())

print("\nMissing values:")
print(df_fb.isna().sum())

# ==============================================================================
# 11. FOOD BALANCES DATA VALIDATION
# ==============================================================================

print("\n" + "=" * 80)
print("FOOD BALANCES DATA VALIDATION")
print("=" * 80)

required_columns = [
    "Area",
    "Year",
    "Element",
    "Item",
    "Unit",
    "Value"
]

missing_columns = [
    column
    for column in required_columns
    if column not in df_fb.columns
]

if missing_columns:
    raise ValueError(
        f"Food Balances dataset is missing required columns: "
        f"{missing_columns}"
    )

print("\nRequired columns: OK")

print(f"Area(s): {df_fb['Area'].dropna().unique().tolist()}")

print(f"Year range: {df_fb['Year'].min()} to {df_fb['Year'].max()}")

print(f"Missing Value cells: {df_fb['Value'].isna().sum()}")

print(f"Duplicate rows: {df_fb.duplicated().sum()}")

expected_years = set(range(2010, 2024))
actual_years = set(df_fb["Year"].dropna().astype(int))

missing_years = sorted(expected_years - actual_years)

if missing_years:
    print(f"WARNING: Missing expected years: {missing_years}")
else:
    print("Expected 2010-2023 year coverage: OK")

# ==============================================================================
# 12. FOOD BALANCES: PROTEIN SUPPLY BY FOOD GROUP
# ==============================================================================

print("\n" + "=" * 80)
print("PROTEIN SUPPLY BY FOOD GROUP")
print("=" * 80)

# Keep only protein supply data
df_protein = df_fb[
    df_fb["Element"] == "Protein supply quantity (g/capita/day)"
].copy()

# Main food groups relevant to the HerPlate analysis
protein_items = {
    "Cereals": [
        "Wheat and products",
        "Rice and products",
        "Maize and products",
        "Sorghum and products",
        "Millet and products",
        "Cereals, other"
    ],
    "Pulses": [
        "Beans",
        "Peas",
        "Pulses, Other and products"
    ],
    "Meat": [
        "Bovine Meat",
        "Mutton & Goat Meat",
        "Pigmeat",
        "Poultry Meat",
        "Meat, Other",
        "Offals, Edible"
    ],
    "Fish": [
        "Freshwater Fish",
        "Demersal Fish",
        "Pelagic Fish",
        "Marine Fish, Other",
        "Crustaceans",
        "Cephalopods",
        "Molluscs, Other",
        "Aquatic Animals, Others"
    ],
    "Eggs": [
        "Eggs"
    ],
    "Milk": [
        "Milk - Excluding Butter"
    ],
    "Nuts and seeds": [
        "Nuts and products",
        "Groundnuts",
        "Soyabeans",
        "Sunflower seed",
        "Sesame seed"
    ]
}

# Validate protein food-group mapping
available_items = set(df_fb["Item"].dropna().unique())

print("\nProtein food-group mapping validation:")

for group, items in protein_items.items():
    missing_items = [
        item
        for item in items
        if item not in available_items
    ]

    if missing_items:
        print(f"WARNING - {group}: missing items -> {missing_items}")
    else:
        print(f"{group}: all mapped items found")

# Create food-group mapping
item_to_group = {
    item: group
    for group, items in protein_items.items()
    for item in items
}

df_protein["Food Group"] = df_protein["Item"].map(item_to_group)

# Remove items that were not mapped
df_protein = df_protein.dropna(subset=["Food Group"])

# Aggregate protein supply by food group and year
protein_by_group = (
    df_protein
    .groupby(["Year", "Food Group"], as_index=False)["Value"]
    .sum()
)

print("\n2023 protein supply by food group:")

print(
    protein_by_group[protein_by_group["Year"] == 2023]
    .sort_values("Value", ascending=False)
    .round(2)
    .to_string(index=False)
)

# ==============================================================================
# 13. FOOD BALANCES: PROTEIN SUPPLY TRENDS
# ==============================================================================

print("\n" + "=" * 80)
print("PROTEIN SUPPLY TRENDS: 2010-2023")
print("=" * 80)

protein_pivot = (
    protein_by_group
    .pivot(index="Year", columns="Food Group", values="Value")
    .fillna(0)
)

print("\nProtein supply (g/capita/day):")
print(protein_pivot.round(2).to_string())

# Calculate percentage change from 2010 to 2023
protein_change = pd.DataFrame({
    "2010": protein_pivot.loc[2010],
    "2023": protein_pivot.loc[2023]
})

protein_change["Absolute Change"] = (
    protein_change["2023"] - protein_change["2010"]
)

protein_change["% Change"] = (
    protein_change["Absolute Change"] / protein_change["2010"] * 100
)

print("\nProtein supply change, 2010 to 2023:")
print(
    protein_change
    .sort_values("% Change", ascending=False)
    .round(2)
    .to_string()
)

# ==============================================================================
# 14. PROTEIN FOOD-GROUP MAPPING VALIDATION
# ==============================================================================

print("\n" + "=" * 80)
print("PROTEIN FOOD-GROUP MAPPING: 2010 VS 2023")
print("=" * 80)

validation = (
    df_protein[
        df_protein["Year"].isin([2010, 2023])
    ][
        ["Year", "Item", "Value", "Unit", "Food Group"]
    ]
    .sort_values(["Food Group", "Year", "Item"])
)

print(validation.to_string(index=False))

# ==============================================================================
# 15. FOOD BALANCES: FOOD SUPPLY QUANTITY TRENDS
# ==============================================================================

print("\n" + "=" * 80)
print("FOOD SUPPLY QUANTITY TRENDS: 2010-2023")
print("=" * 80)

# Keep food supply quantity per person
df_food_supply = df_fb[
    df_fb["Element"] == "Food supply quantity (kg/capita/yr)"
].copy()

food_supply_items = {
    "Cereals": [
        "Wheat and products",
        "Rice and products",
        "Barley and products",
        "Maize and products",
        "Rye",
        "Oats",
        "Millet and products",
        "Sorghum and products",
        "Cereals, other"
    ],
    "Pulses": [
        "Beans",
        "Peas",
        "Pulses, Other and products"
    ],
    "Nuts and seeds": [
        "Nuts and products",
        "Soyabeans",
        "Groundnuts",
        "Sunflower seed",
        "Rape and Mustardseed",
        "Cottonseed",
        "Sesame seed",
        "Coconuts - Incl Copra",
        "Oilcrops, Other"
    ],
    "Vegetables": [
        "Tomatoes and products",
        "Onions",
        "Vegetables, other"
    ],
    "Fruits": [
        "Oranges, Mandarines",
        "Lemons, Limes and products",
        "Grapefruit and products",
        "Bananas",
        "Plantains",
        "Apples and products",
        "Pineapples and products",
        "Dates",
        "Grapes and products (excl wine)",
        "Fruits, other"
    ],
    "Meat": [
        "Bovine Meat",
        "Mutton & Goat Meat",
        "Pigmeat",
        "Poultry Meat",
        "Meat, Other",
        "Offals, Edible"
    ],
    "Fish": [
        "Freshwater Fish",
        "Demersal Fish",
        "Pelagic Fish",
        "Marine Fish, Other",
        "Crustaceans",
        "Cephalopods",
        "Molluscs, Other",
        "Aquatic Animals, Others"
    ],
    "Eggs": [
        "Eggs"
    ],
    "Milk": [
        "Milk - Excluding Butter"
    ],
    "Oils and fats": [
        "Soyabean Oil",
        "Groundnut Oil",
        "Sunflowerseed Oil",
        "Rape and Mustard Oil",
        "Cottonseed Oil",
        "Palm Oil",
        "Coconut Oil",
        "Sesameseed Oil",
        "Olive Oil",
        "Ricebran Oil",
        "Maize Germ Oil",
        "Oilcrops Oil, Other",
        "Butter, Ghee",
        "Cream",
        "Fats, Animals, Raw"
    ]
}

# Validate food-supply mapping
print("\nFood supply mapping validation:")

for group, items in food_supply_items.items():
    missing_items = [
        item
        for item in items
        if item not in available_items
    ]

    if missing_items:
        print(f"WARNING - {group}: missing items -> {missing_items}")
    else:
        print(f"{group}: all mapped items found")

item_to_supply_group = {
    item: group
    for group, items in food_supply_items.items()
    for item in items
}

df_food_supply["Food Group"] = df_food_supply["Item"].map(
    item_to_supply_group
)

# Keep only mapped food groups
df_food_supply = df_food_supply.dropna(subset=["Food Group"])

# Aggregate food supply by year and food group
food_supply_by_group = (
    df_food_supply
    .groupby(["Year", "Food Group"], as_index=False)["Value"]
    .sum()
)

# Compare 2010 and 2023
food_supply_pivot = (
    food_supply_by_group
    .pivot(index="Year", columns="Food Group", values="Value")
    .fillna(0)
)

food_supply_change = pd.DataFrame({
    "2010": food_supply_pivot.loc[2010],
    "2023": food_supply_pivot.loc[2023]
})

food_supply_change["Absolute Change"] = (
    food_supply_change["2023"] - food_supply_change["2010"]
)

food_supply_change["% Change"] = (
    food_supply_change["Absolute Change"]
    / food_supply_change["2010"]
    * 100
)

print("\nFood supply quantity change, 2010 to 2023:")

print(
    food_supply_change
    .sort_values("% Change", ascending=False)
    .round(2)
    .to_string()
)

# ==============================================================================
# 16. FOOD BALANCES: DRIVERS OF PULSE AND VEGETABLE CHANGES
# ==============================================================================

print("\n" + "=" * 80)
print("DRIVERS OF PULSE AND VEGETABLE SUPPLY CHANGES")
print("=" * 80)

focus_items = [
    "Beans",
    "Peas",
    "Pulses, Other and products",
    "Tomatoes and products",
    "Onions",
    "Vegetables, other"
]

focus_supply = df_food_supply[
    df_food_supply["Item"].isin(focus_items)
    & df_food_supply["Year"].isin([2010, 2023])
][
    ["Year", "Item", "Value", "Unit"]
].copy()

focus_pivot = (
    focus_supply
    .pivot(index="Item", columns="Year", values="Value")
)

focus_pivot["Absolute Change"] = (
    focus_pivot[2023] - focus_pivot[2010]
)

focus_pivot["% Change"] = (
    focus_pivot["Absolute Change"] / focus_pivot[2010] * 100
)

print("\nSupply change by individual food item:")

print(
    focus_pivot
    .sort_values("% Change")
    .round(2)
    .to_string()
)

# ==============================================================================
# 17. FOOD BALANCES CHART 1: PROTEIN SUPPLY TRENDS
# ==============================================================================

plt.figure(figsize=(11, 6))

for food_group in protein_pivot.columns:
    plt.plot(
        protein_pivot.index,
        protein_pivot[food_group],
        marker="o",
        label=food_group
    )

plt.title("Ghana Protein Supply by Food Group, 2010-2023")

plt.xlabel("Year")
plt.ylabel("Protein Supply (g/capita/day)")

plt.legend(
    title="Food Group",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.show()

# ==============================================================================
# 18. FOOD BALANCES CHART 2: FOOD SUPPLY CHANGE
# ==============================================================================

food_supply_chart = food_supply_change.sort_values("% Change")

plt.figure(figsize=(10, 7))

bars = plt.barh(
    food_supply_chart.index,
    food_supply_chart["% Change"]
)

plt.axvline(0, linewidth=1)

plt.title("Change in Ghana Food Supply by Food Group, 2010-2023")

plt.xlabel("Change in Food Supply (%)")
plt.ylabel("Food Group")

for bar, value in zip(bars, food_supply_chart["% Change"]):
    if value >= 0:
        x_position = value + 1
        ha = "left"
    else:
        x_position = value - 1
        ha = "right"

    plt.text(
        x_position,
        bar.get_y() + bar.get_height() / 2,
        f"{value:+.1f}%",
        va="center",
        ha=ha
    )

plt.grid(axis="x", alpha=0.3)

plt.tight_layout()
plt.show()

# ==============================================================================
# 19. FOOD BALANCES KEY FINDINGS
# ==============================================================================

print("\n" + "=" * 80)
print("FOOD BALANCES KEY FINDINGS")
print("=" * 80)

print("\n1. Food supply context:")

print(
    "   Between 2010 and 2023, Ghana's per-capita food supply "
    "became more concentrated in cereals and meat, while "
    "pulses and vegetables declined."
)

print("\n2. Pulses:")

print(
    "   Pulse supply declined by approximately 39.3%, "
    "driven primarily by a decline in beans."
)

print("\n3. Meat:")

print(
    "   Meat supply increased by approximately 32.0%, "
    "with poultry being a major contributor."
)

print("\n4. Vegetables:")

print(
    "   Vegetable supply declined by approximately 40.7%, "
    "largely reflecting a decline in tomatoes."
)

print("\n5. Interpretation:")

print(
    "   Food Balance indicators describe national food "
    "availability rather than individual consumption. "
    "They are therefore interpreted alongside MDD-W "
    "dietary consumption indicators."
)

# ==============================================================================
# 20. CoAHD: GHANA HEALTHY DIET COST TREND
# ==============================================================================

print("\n" + "=" * 80)
print("GHANA COST OF A HEALTHY DIET: 2017-2025")
print("=" * 80)

# Cost of a healthy diet from the July 2026 SOFI CoAHD data
cohd_trend = pd.DataFrame({
    "Year": [
        2017, 2018, 2019, 2020, 2021,
        2022, 2023, 2024, 2025
    ],
    "CoHD (PPP/day)": [
        3.54, 3.51, 3.48, 3.46, 3.50,
        3.83, 4.29, 4.49, 4.65
    ],
    "Unaffordability (%)": [
        67.2, 66.1, 64.8, 65.6, 64.7,
        64.7, 66.4, 65.8, 65.8
    ],
    "People unable to afford (million)": [
        20.2, 20.2, 20.3, 20.9, 21.1,
        21.5, 22.4, 22.6, 23.1
    ]
})

print("\nGhana CoHD trend:")

print(cohd_trend.to_string(index=False))

# Visualize CoHD trend
plt.figure(figsize=(9, 5))

plt.plot(
    cohd_trend["Year"],
    cohd_trend["CoHD (PPP/day)"],
    marker="o"
)

plt.title("Ghana Cost of a Healthy Diet, 2017-2025")

plt.xlabel("Year")
plt.ylabel("Cost (Int$ PPP per person per day)")

plt.xticks(cohd_trend["Year"], rotation=45)

plt.tight_layout()
plt.show()

# ==============================================================================
# 21. 2021 HEALTHY DIET BASKET
# ==============================================================================

print("\n" + "=" * 80)
print("GHANA 2021 HEALTHY DIET BASKET")
print("=" * 80)

# 2021 CoAHD food-group breakdown
coahd_data = pd.DataFrame({
    "Food Group": [
        "Animal source foods",
        "Starchy staples",
        "Legumes, nuts and seeds",
        "Vegetables",
        "Fruits",
        "Oils and fats"
    ],
    "Cost (GHS/day)": [
        3.53,
        1.70,
        0.97,
        1.13,
        0.62,
        0.65
    ],
    "Cost (PPP/day)": [
        1.44,
        0.69,
        0.39,
        0.46,
        0.25,
        0.27
    ]
})

total_ghs = coahd_data["Cost (GHS/day)"].sum()

total_ppp = coahd_data["Cost (PPP/day)"].sum()

coahd_data["Cost Share (%)"] = (
    coahd_data["Cost (PPP/day)"] / total_ppp * 100
)

print("\n2021 food-group costs:")

print(coahd_data.round(2).to_string(index=False))

print(f"\nCalculated local-currency basket: {total_ghs:.2f} GHS/day")

print(f"Calculated PPP basket: ${total_ppp:.2f} PPP/day")

print(
    "\nOfficial 2021 CoHD from the CoAHD table: "
    "$3.50 PPP/day"
)

# Visualize PPP cost contribution
plt.figure(figsize=(9, 6))

plt.barh(
    coahd_data["Food Group"],
    coahd_data["Cost (PPP/day)"]
)

plt.title("Ghana 2021 Healthy Diet Cost by Food Group")

plt.xlabel("Cost (Int$ PPP per person per day)")

plt.ylabel("Food Group")

plt.tight_layout()
plt.show()

# ==============================================================================
# 22. PROTEIN SUBSTITUTION SIMULATION
# ==============================================================================

print("\n" + "=" * 80)
print("PROTEIN SUBSTITUTION SIMULATION")
print("=" * 80)

# Baseline daily quantities
animal_base = 150  # grams
plant_base = 30    # grams

# Nutritional assumptions
animal_protein = 0.20
plant_protein = 0.22

animal_iron = 0.02
plant_iron = 0.054

# Cost assumptions
animal_cost = 0.045
plant_cost = 0.015

swap_levels = [0, 20, 40, 50, 80, 100]

swap_results = []

for swap in swap_levels:
    animal_qty = animal_base * (1 - swap / 100)

    plant_qty = plant_base + animal_base * swap / 100

    protein = (
        animal_qty * animal_protein
        + plant_qty * plant_protein
    )

    iron = (
        animal_qty * animal_iron
        + plant_qty * plant_iron
    )

    cost = (
        animal_qty * animal_cost
        + plant_qty * plant_cost
    )

    swap_results.append({
        "Swap (%)": swap,
        "Animal food (g)": animal_qty,
        "Plant food (g)": plant_qty,
        "Protein (g)": protein,
        "Iron (mg)": iron,
        "Cost": cost
    })

swap_df = pd.DataFrame(swap_results)

baseline_cost = swap_df.loc[
    swap_df["Swap (%)"] == 0, "Cost"
].iloc[0]

baseline_iron = swap_df.loc[
    swap_df["Swap (%)"] == 0, "Iron (mg)"
].iloc[0]

swap_df["Cost Reduction (%)"] = (
    (baseline_cost - swap_df["Cost"]) / baseline_cost * 100
)

swap_df["Iron Change (%)"] = (
    (swap_df["Iron (mg)"] - baseline_iron) / baseline_iron * 100
)

print("\nProtein substitution scenarios:")

print(swap_df.round(2).to_string(index=False))

# 50% scenario
swap_50 = swap_df[swap_df["Swap (%)"] == 50].iloc[0]

print("\n50% substitution scenario:")

print(f"Cost: {swap_50['Cost']:.2f}")

print(f"Cost reduction: {swap_50['Cost Reduction (%)']:.1f}%")

print(f"Iron change: {swap_50['Iron Change (%)']:+.1f}%")

# Visualize cost reduction
plt.figure(figsize=(8, 5))

plt.plot(
    swap_df["Swap (%)"],
    swap_df["Cost Reduction (%)"],
    marker="o"
)

plt.title("Healthy Diet Cost Reduction from Protein Substitution")

plt.xlabel("Animal-to-Plant Protein Swap (%)")

plt.ylabel("Cost Reduction (%)")

plt.grid(True)

plt.tight_layout()
plt.show()

# ==============================================================================
# 23. HEALTHY DIET AFFORDABILITY SIMULATION
# ==============================================================================

print("\n" + "=" * 80)
print("HEALTHY DIET AFFORDABILITY SIMULATION")
print("=" * 80)

# Ghana population used in the project model
population = 33.5e6

# Model scenario
baseline_diet_cost = 4.28
post_swap_diet_cost = 3.75

# Affordability assumptions
days_per_month = 30.4
food_budget_share = 0.52

baseline_threshold = (
    baseline_diet_cost * days_per_month / food_budget_share
)

post_swap_threshold = (
    post_swap_diet_cost * days_per_month / food_budget_share
)

print(f"\nModel baseline healthy diet cost: ${baseline_diet_cost:.2f} PPP/day")

print(f"Post-intervention healthy diet cost: ${post_swap_diet_cost:.2f} PPP/day")

print(f"\nBaseline monthly affordability threshold: ${baseline_threshold:.2f} PPP")

print(f"Post-intervention monthly affordability threshold: ${post_swap_threshold:.2f} PPP")

# Log-normal income distribution
sigma = 0.75

mu = np.log(baseline_threshold) - (0.429 * sigma)

np.random.seed(42)

sample_size = 100_000

monthly_incomes = np.random.lognormal(
    mean=mu,
    sigma=sigma,
    size=sample_size
)

# Determine affordability
baseline_affordable = monthly_incomes >= baseline_threshold

post_swap_affordable = monthly_incomes >= post_swap_threshold

baseline_affordability_rate = baseline_affordable.mean() * 100

post_swap_affordability_rate = post_swap_affordable.mean() * 100

affordability_change = (
    post_swap_affordability_rate - baseline_affordability_rate
)

population_lifted = affordability_change / 100 * population

print("\nAffordability results:")

print(f"Baseline affordability: {baseline_affordability_rate:.1f}%")

print(f"Post-intervention affordability: {post_swap_affordability_rate:.1f}%")

print(f"Change in affordability: {affordability_change:+.1f} percentage points")

print(
    "Estimated additional people able to "
    f"afford a healthy diet: {population_lifted:,.0f}"
)

# Visualize income distribution
plt.figure(figsize=(9, 5))

plt.hist(
    monthly_incomes,
    bins=100,
    density=True,
    alpha=0.7
)

plt.axvline(baseline_threshold, linestyle="--", label="Baseline threshold")

plt.axvline(post_swap_threshold, linestyle="--", label="Post-intervention threshold")

plt.title("Simulated Monthly Income Distribution")

plt.xlabel("Monthly Income (PPP)")

plt.ylabel("Density")

plt.legend()

plt.tight_layout()
plt.show()

# ==============================================================================
# 24. FINAL PROJECT FINDINGS
# ==============================================================================

print("\n" + "=" * 80)
print("KEY HERPLATE GHANA FINDINGS")
print("=" * 80)

print("\n1. Dietary diversity:")

for _, row in mdd_achievement.iterrows():
    print(
        f"   {row['Geographic Level']}: "
        f"{row['Value']:.1f}% of women achieve MDD-W"
    )

print("\n2. Ghana vs Kenya:")

print(f"   Ghana MDD-W achievement: {ghana_mdd:.1f}%")

print(f"   Kenya MDD-W achievement: {kenya_mdd:.1f}%")

print(f"   Ghana-Kenya difference: {difference:+.1f} percentage points")

print("\n3. Food supply context:")

print(
    "   Pulse supply declined by approximately "
    "39.3% between 2010 and 2023."
)

print(
    "   Vegetable supply declined by approximately "
    "40.7% between 2010 and 2023."
)

print(
    "   Meat supply increased by approximately "
    "32.0% over the same period."
)

print("\n4. Healthy diet affordability:")

print("   Ghana 2025 CoHD: $4.65 PPP/day")

print("   Ghana 2025 unaffordability: 65.8%")

print("   People unable to afford a healthy diet: 23.1 million")

print("\n5. Protein substitution scenario:")

print(f"   50% substitution cost reduction: {swap_50['Cost Reduction (%)']:.1f}%")

print(f"   50% substitution iron change: {swap_50['Iron Change (%)']:+.1f}%")

print("\n6. Intervention affordability model:")

print(f"   Baseline affordability: {baseline_affordability_rate:.1f}%")

print(f"   Post-intervention affordability: {post_swap_affordability_rate:.1f}%")

print(f"   Improvement: {affordability_change:+.1f} percentage points")

print(
    "   Estimated additional people able to "
    f"afford a healthy diet: {population_lifted:,.0f}"
)

print("\n" + "=" * 80)
print("EDA COMPLETED SUCCESSFULLY")
print("=" * 80)