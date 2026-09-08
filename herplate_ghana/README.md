# 🇬🇭 HerPlate Ghana — 2026 Datathon Project Setup

Welcome to the full repository setup for **HerPlate Ghana**, an interactive decision-support tool built to map the breaking links between food supply, market cost, and women's plates (Minimum Dietary Diversity for Women - MDD-W). 

Our core research question: **Where is the pathway from Ghana's food system to women's plates breaking?**
Our main finding: **Same dietary gap. Different bottlenecks.**

---

## 📂 Project Structure

This project is organized into four main components:
1.  `data_prep.py`: Ingestion and clean-up script that generates simulated FAOSTAT (FBS, CAHD, and MDD-W) datasets for Ghana to feed your model.
2.  `app.py`: A highly-polished, interactive Streamlit application containing the HerPlate Diagnostic Matrix, value-chain pathway charts, and a live MILP (Mixed-Integer Linear Programming) optimization solver.
3.  `requirements.txt`: Python dependencies required to run the project.
4.  `README.md`: This file, guiding you step-by-step through setting up and launching the tool.

---

## 🛠️ Step-by-Step Installation & Run Guide

Follow these steps to run the complete **HerPlate Ghana** suite on your local machine:

### Step 1: Clone or Set Up Your Project Directory
Create a new directory on your local machine and navigate into it:
```bash
mkdir herplate_ghana
cd herplate_ghana
```
Place `data_prep.py`, `app.py`, and `requirements.txt` inside this folder.

### Step 2: Set Up a Virtual Environment (Highly Recommended)
Create a Python virtual environment to prevent package version conflicts:
```bash
# On macOS/Linux
python3 -m venv venv
source venv/bin/activate

# On Windows
python -m venv venv
venv\Scripts\activate
```

### Step 3: Install Required Packages
Install all necessary data science, optimization, and visualization libraries:
```bash
pip install -r requirements.txt
```

### Step 4: Run Data Preparation
Run the ingestion script to clean and output the aligned dataset files. This creates `cleaned_ghana_cahd.csv`, `cleaned_ghana_fbs.csv`, and `cleaned_ghana_mddw.csv` in your directory:
```bash
python data_prep.py
```

### Step 5: Launch the Streamlit Decision-Support Tool
With your datasets generated, boot up the local interactive app server:
```bash
streamlit run app.py
```
This will automatically launch the browser window running your beautiful **HerPlate Ghana** decision-support tool!

---

## 🧪 Deep-Dive Math: Bioavailability & MILP Constraints

The tool features a live **Mixed-Integer Linear Programming** (MILP) model implemented using the `PuLP` package. 
*   **Bioavailability Scaling:** In WRA, plant-based iron and zinc absorption is heavily muted (~10% for plant iron vs ~18% for heme iron found in animal foods). The optimization constraint implements a discount factor so the target of **1.8mg absorbed iron per day** is strictly satisfied with biologically useful nutrients, not just theoretical numbers.
*   **Minimum Dietary Diversity (MDD-W):** The solver links continuous food intake variables (grams) to binary active-group variables. The solver will only solve if it can select a combination that guarantees **at least 4-5 different food groups** (with a minimum of 10g consumption per group), satisfying dietary diversity while minimizing costs.

---

## 🏆 Presentation Quick-Reference For Your Team
*   **Track Designation:** EAT Track (Nutrition, Affordability & Diets)
*   **Presentation Limit:** Strictly between 5 and 7 minutes.
*   **Key Pitch Hook:** *"Same dietary gap. Different bottlenecks. HerPlate Ghana helps identify where deeper intervention should begin instead of treating every low-consumption food as the same problem."*
