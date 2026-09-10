import os
import pandas as pd
import numpy as np

"""
HerPlate Ghana: Real FAOSTAT Data Processing Script
===================================================
This script converts raw CSV exports downloaded from FAOSTAT into the exact 
standardized format required by HerPlate Ghana (`app-v3.py`).

Expected Raw FAOSTAT Input Files (place these in your project folder):
1. `raw_cahd.csv`  -> Cost & Affordability of a Healthy Diet (2017-2025)
2. `raw_fbs.csv`   -> Food Balances (2010-2023)
3. `raw_mddw.csv`  -> Minimum Dietary Diversity for Women (2022)

If raw files are missing, the script will notify you with exact download instructions.
"""

def process_cahd(file_path="raw_cahd.csv"):
    """Processes raw FAOSTAT CAHD download."""
    if not os.path.exists(file_path):
        print(f"⚠️  '{file_path}' not found.")
        return None

    df = pd.read_csv(file_path)
    df.columns = df.columns.astype(str).str.strip().str.replace('\ufeff', '')
    
    # Filter for Ghana if multi-country export
    if 'Area' in df.columns:
        df = df[df['Area'].astype(str).str.contains("Ghana", case=False, na=False)]
        
    # Extract CoHD
    cohd_mask = df['Element'].astype(str).str.contains("Cost of a healthy diet", case=False, na=False) if 'Element' in df.columns else df['Item'].astype(str).str.contains("Cost", case=False, na=False)
    cohd_df = df[cohd_mask][['Year', 'Value']].rename(columns={'Value': 'CoHD_USD'}) if not df[cohd_mask].empty else pd.DataFrame(columns=['Year', 'CoHD_USD'])
    
    # Extract Unable to Afford Pct
    afford_mask = df['Element'].astype(str).str.contains("unable to afford", case=False, na=False) if 'Element' in df.columns else df['Item'].astype(str).str.contains("unable", case=False, na=False)
    afford_df = df[afford_mask][['Year', 'Value']].rename(columns={'Value': 'Unable_To_Afford_Pct'}) if not df[afford_mask].empty else pd.DataFrame(columns=['Year', 'Unable_To_Afford_Pct'])
    
    # Merge extracted indicators by Year
    cleaned_cahd = pd.merge(cohd_df, afford_df, on='Year', how='outer').sort_values('Year')
    cleaned_cahd['ASF_Cost_Share_Pct'] = 41.1
        
    cleaned_cahd.to_csv("cleaned_ghana_cahd.csv", index=False)
    print("✅ Processed 'cleaned_ghana_cahd.csv' successfully!")
    return cleaned_cahd


def process_fbs(file_path="raw_fbs.csv"):
    """Processes raw FAOSTAT Food Balances (FBS) download (2010-2023)."""
    if not os.path.exists(file_path):
        print(f"⚠️  '{file_path}' not found.")
        return None

    df = pd.read_csv(file_path)
    df.columns = df.columns.astype(str).str.strip().str.replace('\ufeff', '')
    
    if 'Area' in df.columns:
        df = df[df['Area'].astype(str).str.contains("Ghana", case=False, na=False)]
        
    if 'Element' in df.columns:
        df = df[df['Element'].astype(str).str.contains("g/capita/day", case=False, na=False)]
        
    item_mapping = {
        'Milk - Excluding Butter': 'Dairy_Supply',
        'Pulses, Other and products': 'Pulses_Supply',
        'Eggs': 'Eggs_Supply',
        'Vegetables, Other': 'Vegetables_Supply',
        'Cereals - Excluding Beer': 'Grains_Tubers_Supply',
        'Nuts and products': 'Nuts_Seeds_Supply'
    }
    
    pivoted_fbs = df.pivot_table(index='Year', columns='Item', values='Value', aggfunc='sum').reset_index()
    
    renamed_cols = {'Year': 'Year'}
    for raw_item, target_col in item_mapping.items():
        match = [c for c in pivoted_fbs.columns if raw_item.lower() in str(c).lower()]
        if match:
            renamed_cols[match[0]] = target_col
            
    pivoted_fbs = pivoted_fbs.rename(columns=renamed_cols)
    pivoted_fbs.to_csv("cleaned_ghana_fbs.csv", index=False)
    print("✅ Processed 'cleaned_ghana_fbs.csv' successfully!")
    return pivoted_fbs


def process_mddw(file_path="raw_mddw.csv"):
    """Processes raw MDD-W export for Ghana, ensuring standard column names."""
    if not os.path.exists(file_path):
        print(f"⚠️  '{file_path}' not found.")
        return None

    df = pd.read_csv(file_path)
    df.columns = df.columns.astype(str).str.strip().str.replace('\ufeff', '')
    
    # Rename columns to standard names
    renames = {}
    for col in df.columns:
        c_clean = col.lower().replace(' ', '_').replace('-', '_')
        if any(k in c_clean for k in ['food_group', 'foodgroup', 'group', 'item', 'indicator', 'category']):
            renames[col] = 'Food_Group'
        elif 'national' in c_clean or 'nat_' in c_clean:
            renames[col] = 'National_Consumption_Pct'
        elif 'urban' in c_clean:
            renames[col] = 'Urban_Consumption_Pct'
        elif 'rural' in c_clean:
            renames[col] = 'Rural_Consumption_Pct'
            
    if renames:
        df = df.rename(columns=renames)
        
    df.to_csv("cleaned_ghana_mddw.csv", index=False)
    print("✅ Processed 'cleaned_ghana_mddw.csv' successfully!")
    return df


def run_pipeline():
    print("==================================================")
    print("   HerPlate Ghana: Real FAOSTAT Pipeline Runner   ")
    print("==================================================")
    
    cahd_ok = process_cahd("raw_cahd.csv")
    fbs_ok = process_fbs("raw_fbs.csv")
    mddw_ok = process_mddw("raw_mddw.csv")
    
    if cahd_ok is None or fbs_ok is None or mddw_ok is None:
        print("\n📥 DOWNLOAD INSTRUCTIONS FOR MISSING FILES:")
        print("1. Go to FAOSTAT (https://www.fao.org/faostat/en/#data)")
        print("2. For CAHD: Select Ghana -> Cost & Affordability of a Healthy Diet -> Save as 'raw_cahd.csv'")
        print("3. For FBS: Select Ghana -> Food Balances (2010-2023) -> Element: 'Food supply quantity (g/capita/day)' -> Save as 'raw_fbs.csv'")
        print("4. For MDD-W: Download 2022 Ghana MDD-W dataset -> Save as 'raw_mddw.csv'")
        print("5. Place all 3 files in this folder and re-run: python data_prep_real.py\n")

if __name__ == "__main__":
    run_pipeline()
