### Note: Core Pipeline & Streamlit Web App

# 🇬🇭 HerPlate Ghana: Food System Bottleneck Diagnostic

**Decision-Support System for Maternal Agrifood Reform**  
*Women in Data Science Datathon Project 2026*

---

## 📌 Project Overview & Core Question

**Core Question:** *Where is the pathway from Ghana's food system to women's plates breaking?*

Rather than assuming all nutrition gaps share the same cause, **HerPlate Ghana** integrates three independent UN FAOSTAT datasets to classify nutritious food categories by their specific structural bottleneck:

1. **Healthy-Diet Affordability (CoAHD 2017–2025)**: Evaluates macro financial barriers and food basket component costs.
2. **Minimum Dietary Diversity for Women (MDD-W 2022)**: Measures actual consumption rates among Women of Reproductive Age (WRA 15–49) across National, Urban, and Rural demographics.
3. **Food Balances (FBS 2010–2023)**: Tracks 13-year national daily per-capita food availability (`g/capita/day`) to identify supply trajectories.

---

## 🎯 Main Empirical Findings & Bottleneck Classifications

| Food Group | Women's Plate Consumption (2022) | 10-Yr National Supply Trend | Parent Cost Component Share | Bottleneck Classification | Structural Breakdown Location |
| :--- | :--- | :--- | :--- | :--- | :--- |
| 🥛 **Dairy Products** | **15.4%** *(Rural: 8.1%)* | **-24.4%** *(Declining)* | High (ASF Basket ~41.1%) | **Convergent Pressure** | Production ➔ Market Cold Chain ➔ Household |
| 🫘 **Pulses (Legumes)** | **23.5%** *(Rural: 25.5%)* | **-39.4%** *(Declining)* | Low Relative Cost ($0.39 PPP) | **Supply / Diversity Pressure** | Upstream Agricultural Production |
| 🥚 **Eggs** | **27.6%** *(Urban: 34.7%)* | **+3.9%** *(Stable)* | Moderate Market Margin | **Access Beyond Supply** | Local Market Distribution ➔ Intra-Household |
| 🥬 **Vegetables** | **51.5%** *(Leafy: 71.8%)* | **-40.7%** *(Declining)* | Low-Moderate Cost ($0.46 PPP) | **Emerging Supply Risk** | Upstream Farming & Irrigation |

---

## 📂 Project Repository Structure

```text
HerPlate_Ghana/
├── eda_coahd.py             # Individual EDA for Cost & Affordability (CoAHD)
├── eda_mddw.py              # Individual EDA for Women's Dietary Diversity (MDD-W)
├── eda_fbs.py               # Individual EDA for Food Balances 13-Yr Supply Trends (FBS)
├── data_pipeline.py         # Data processing pipeline (Merates 2022 baseline matrix)
├── app.py                   # Production Streamlit Web Dashboard
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation & setup guide
```

---

## 🛠️ Step-by-Step Setup & Execution Workflow

### Step 1: Clone Repository & Create Virtual Environment
```bash
git clone https://github.com/Nowshin1077/Women_in_Data_Datathon_Project_2026.git
cd Women_in_Data_Datathon_Project_2026

# Create virtual environment
python -m venv venv

# Activate environment
# On Windows Command Prompt:
venv\Scripts\activate
# On macOS / Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Exploratory Data Analysis (EDA)
Execute the three individual EDA scripts to inspect the empirical figures:
```bash
python eda_coahd.py
python eda_mddw.py
python eda_fbs.py
```

### Step 4: Run Data Processing Pipeline
Merge the datasets on the 2022 baseline and generate clean CSV exports:
```bash
python data_pipeline.py
```

### Step 5: Launch Streamlit Decision-Support Dashboard
```bash
python -m streamlit run app.py
```

---

## ☁️ Deploying on Streamlit Community Cloud

1. Commit and push all files to your GitHub repository:
   ```bash
   git add .
   git commit -m "Deploy HerPlate Ghana dashboard and EDA scripts"
   git push origin main
   ```
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **New App**.
3. Select:
   * **Repository**: `Nowshin1077/Women_in_Data_Datathon_Project_2026`
   * **Branch**: `main`
   * **Main file path**: `app.py`
4. Click **Deploy!**
