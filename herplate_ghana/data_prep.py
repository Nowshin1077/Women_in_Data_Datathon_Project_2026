import pandas as pd
import numpy as np

def generate_mock_data():
    print("Generating mock datasets to simulate FAOSTAT datasets for Ghana...")
    
    # -------------------------------------------------------------
    # 1. Cost and Affordability of a Healthy Diet (CAHD) (2017-2025)
    # -------------------------------------------------------------
    years_cahd = list(range(2017, 2026))
    # Daily cost of healthy diet in Ghana (rising over time)
    cohd_prices = [3.10, 3.25, 3.40, 3.65, 3.90, 4.20, 4.45, 4.75, 5.10] # USD PPP per day
    # % of population unable to afford a healthy diet (remains high)
    unable_to_afford = [62.5, 63.1, 64.0, 65.2, 66.0, 66.6, 67.2, 68.0, 69.1]
    # Percent cost share of animal-sourced foods in the healthy diet basket
    asf_share = [39.5, 39.8, 40.2, 40.5, 41.1, 41.1, 41.3, 41.5, 41.8]
    
    cahd_df = pd.DataFrame({
        "Year": years_cahd,
        "CoHD_USD": cohd_prices,
        "Unable_To_Afford_Pct": unable_to_afford,
        "ASF_Cost_Share_Pct": asf_share
    })
    cahd_df.to_csv("cleaned_ghana_cahd.csv", index=False)
    print("Saved 'cleaned_ghana_cahd.csv'")

    # -------------------------------------------------------------
    # 2. Food Balances (FBS) (2010-2023)
    # -------------------------------------------------------------
    years_fbs = list(range(2010, 2024))
    n_years = len(years_fbs)
    
    # Simulating trends as outlined in the findings:
    # Dairy: Crashing supply (-24.4% from 2010 to 2022)
    # Pulses: Drastic decline (-39.4% from 2010 to 2022)
    # Eggs: Relatively stable/growing (+3.9% from 2010 to 2022)
    # Vegetables: Sharp decline (-40.7% from 2010 to 2022)
    
    # We will anchor 2010 values and project downward/upward to hit target 2022 percentages
    fbs_data = {
        "Year": years_fbs,
        # Dairy supply (g/capita/day) - from ~25g down to ~18.9g (-24.4%)
        "Dairy_Supply": np.linspace(25.0, 18.9, n_years) + np.random.normal(0, 0.4, n_years),
        # Pulses supply (g/capita/day) - from ~15g down to ~9.1g (-39.4%)
        "Pulses_Supply": np.linspace(15.0, 9.1, n_years) + np.random.normal(0, 0.3, n_years),
        # Eggs supply (g/capita/day) - from ~5.1g up to ~5.3g (+3.9%)
        "Eggs_Supply": np.linspace(5.1, 5.3, n_years) + np.random.normal(0, 0.1, n_years),
        # Vegetables supply (g/capita/day) - from ~120g down to ~71.2g (-40.7%)
        "Vegetables_Supply": np.linspace(120.0, 71.2, n_years) + np.random.normal(0, 2.0, n_years),
        # Grains/Tubers supply (g/capita/day) - highly stable staple
        "Grains_Tubers_Supply": np.linspace(450.0, 465.0, n_years) + np.random.normal(0, 5.0, n_years),
        # Nuts/Seeds supply (g/capita/day)
        "Nuts_Seeds_Supply": np.linspace(45.0, 42.0, n_years) + np.random.normal(0, 1.0, n_years)
    }
    
    fbs_df = pd.DataFrame(fbs_data).round(2)
    fbs_df.to_csv("cleaned_ghana_fbs.csv", index=False)
    print("Saved 'cleaned_ghana_fbs.csv'")

    # -------------------------------------------------------------
    # 3. Minimum Dietary Diversity for Women (MDD-W) (2022 Only)
    # -------------------------------------------------------------
    # Proportion of WRA (15-49) consuming each of the 10 food groups
    mddw_data = {
        "Food_Group": [
            "Grains, roots, tubers & plantains",
            "Pulses (beans, peas, lentils)",
            "Nuts and seeds",
            "Dairy Products",
            "Meat, poultry & fish",
            "Eggs",
            "Dark green leafy vegetables",
            "Vitamin A-rich fruits & vegetables",
            "Other vegetables",
            "Other fruits"
        ],
        "MDDW_Group_No": list(range(1, 11)),
        "National_Consumption_Pct": [88.5, 23.5, 34.2, 15.4, 76.1, 27.6, 42.0, 29.5, 68.3, 31.0],
        "Urban_Consumption_Pct": [92.0, 21.0, 31.5, 23.8, 81.5, 39.4, 35.0, 33.2, 72.1, 38.5],
        "Rural_Consumption_Pct": [85.0, 26.0, 36.9, 7.0, 70.7, 15.8, 49.0, 25.8, 64.5, 23.5]
    }
    mddw_df = pd.DataFrame(mddw_data)
    mddw_df.to_csv("cleaned_ghana_mddw.csv", index=False)
    print("Saved 'cleaned_ghana_mddw.csv'")
    print("Mock data generation complete!")

if __name__ == "__main__":
    generate_mock_data()
