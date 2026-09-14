# 🇬🇭 HerPlate Ghana — 2026 Datathon Project Setup

Welcome to the full repository setup for **HerPlate Ghana**, an interactive decision-support tool built to map the breaking links between food supply, market cost, and women's plates (Minimum Dietary Diversity for Women - MDD-W). 

Our core research question: **Where is the pathway from Ghana's food system to women's plates breaking?**
*   **Track Designation:** EAT Track (Nutrition, Affordability & Diets)
*   **Key Pitch:** *"Same dietary gap. Different bottlenecks. HerPlate Ghana helps identify where deeper intervention should begin instead of treating every low-consumption food as the same problem."*

---

## 📂 Project Structure

This project is organized into four main components:
1.  `final_eda.py`: Ingestion and clean-up script that generates simulated FAOSTAT (FBS, CAHD, and MDD-W) datasets for Ghana to feed the model.
2.  `app.py`: A highly-polished, interactive Streamlit application containing the HerPlate Diagnostic Matrix, value-chain pathway charts.
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
Place `final_eda.py`, `app.py`, and `requirements.txt` inside this folder.

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
Run the ingestion script to clean and output the aligned dataset files.
```bash
src/final_eda.py
or
python final_eda.py
```

### Step 5: Launch the Streamlit Decision-Support Tool
With your datasets generated, boot up the local interactive app server:
```bash
streamlit run src/app.py
or
streamlit run app.py
```
This will automatically launch the browser window running **HerPlate Ghana** decision-support tool!

