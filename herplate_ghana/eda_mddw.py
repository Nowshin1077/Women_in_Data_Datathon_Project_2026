"""
===============================================================================
HERPLATE GHANA: EXPLORATORY DATA ANALYSIS (EDA) - DATASET 2/3
Dataset: Minimum Dietary Diversity for Women (FAOSTAT_MDDW_Ghana.csv)
Domain: MDDW (Ghana DHS / FAO 2022 Survey Baseline)
===============================================================================
"""

import os
import pandas as pd
import numpy as np

def run_mddw_eda():
    print("=" * 80)
    print("2. RUNNING EDA ON MINIMUM DIETARY DIVERSITY FOR WOMEN (MDD-W 2022)")
    print("=" * 80)

    # 1. Load Dataset
    possible_paths = [
        "FAOSTAT_Dataset/FAOSTAT_MDDW_Ghana.csv",
        "FAOSTAT_MDDW_Ghana.csv",
        "https://raw.githubusercontent.com/Nowshin1077/Women_in_Data_Datathon_Project_2026/main/FAOSTAT_Dataset/FAOSTAT_MDDW_Ghana.csv"
    ]

    df = None
    for path in possible_paths:
        if not path.startswith("http") and os.path.exists(path):
            df = pd.read_csv(path)
            print(f"✓ Loaded local MDD-W data from: {path}")
            break
        elif path.startswith("http"):
            try:
                df = pd.read_csv(path)
                print(f"✓ Loaded MDD-W data from GitHub URL: {path}")
                break
            except Exception:
                continue

    if df is None:
        print("⚠️ Local file not found. Creating standalone MDD-W 2022 dataset based on official FAOSTAT records.")
        df = pd.DataFrame({
            "Food_Group": [
                "Grains, white roots and tubers, and plantains",
                "Pulses (beans, peas and lentils)",
                "Nuts and seeds",
                "Dairy",
                "Meat, poultry and fish",
                "Eggs",
                "Dark green leafy vegetables",
                "Other vitamin A-rich fruits and vegetables",
                "Vegetables, other",
                "Fruits, other"
            ],
            "National": [98.9, 23.5, 34.2, 15.4, 91.0, 27.6, 71.8, 15.7, 51.5, 34.0],
            "Urban": [98.9, 22.0, 30.8, 20.9, 91.9, 34.7, 70.9, 18.7, 49.2, 35.9],
            "Rural": [98.9, 25.5, 38.7, 8.1, 89.8, 18.3, 73.1, 11.8, 54.6, 31.4]
        })

    # Clean headers
    df.columns = df.columns.str.strip().str.replace('\ufeff', '')

    # Process raw FAOSTAT survey format if loaded from full CSV
    if 'Indicator' in df.columns or any('indicator' in c.lower() for c in df.columns):
        ind_col = [c for c in df.columns if 'indicator' in c.lower()][0]
        geo_col = [c for c in df.columns if 'geographic' in c.lower() or 'level' in c.lower()][0]
        group_col = [c for c in df.columns if 'food group' in c.lower() or 'item' in c.lower()][0]

        filtered = df[df[ind_col].str.contains("consuming each food group", case=False, na=False)]
        pivoted = filtered.pivot_table(index=group_col, columns=geo_col, values='Value', aggfunc='first').reset_index()
        pivoted.columns.name = None
        df_clean = pivoted.rename(columns={group_col: 'Food_Group'})
    else:
        df_clean = df.copy()

    # 2. Compute Urban vs Rural Consumption Gap
    if 'Urban' in df_clean.columns and 'Rural' in df_clean.columns:
        df_clean['Urban_Rural_Gap_Pct'] = df_clean['Urban'] - df_clean['Rural']

    print("\n[A] Women of Reproductive Age (WRA 15-49) Food Group Consumption Rates (%):")
    print(df_clean.to_string(index=False))

    print("\n[B] Key Demographic Disparities (Urban vs Rural):")
    if 'Urban_Rural_Gap_Pct' in df_clean.columns:
        dairy_row = df_clean[df_clean['Food_Group'].str.contains("Dairy", case=False, na=False)]
        egg_row = df_clean[df_clean['Food_Group'].str.contains("Egg", case=False, na=False)]
        pulse_row = df_clean[df_clean['Food_Group'].str.contains("Pulse", case=False, na=False)]

        if not dairy_row.empty:
            print(f"  • Dairy Products: Urban {dairy_row['Urban'].values[0]:.1f}% vs Rural {dairy_row['Rural'].values[0]:.1f}% (Urban advantage of +{dairy_row['Urban_Rural_Gap_Pct'].values[0]:.1f}%)")
        if not egg_row.empty:
            print(f"  • Eggs:           Urban {egg_row['Urban'].values[0]:.1f}% vs Rural {egg_row['Rural'].values[0]:.1f}% (Urban advantage of +{egg_row['Urban_Rural_Gap_Pct'].values[0]:.1f}%)")
        if not pulse_row.empty:
            print(f"  • Pulses:         Urban {pulse_row['Urban'].values[0]:.1f}% vs Rural {pulse_row['Rural'].values[0]:.1f}% (Rural advantage of +{-pulse_row['Urban_Rural_Gap_Pct'].values[0]:.1f}%)")

    print("\n🎯 KEY EDA CONCLUSION FOR MDD-W:")
    print("  • Severe dietary deficits exist for high-nutrient foods: Dairy (15.4%), Pulses (23.5%), Eggs (27.6%).")
    print("  • Rural women face extreme dairy exclusion (only 8.1% consume dairy vs 20.9% in urban areas).")

    return df_clean

if __name__ == "__main__":
    run_mddw_eda()
