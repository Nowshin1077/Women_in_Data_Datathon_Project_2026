This repository documentation covers dataset parameters, methodologies, and variable definitions for FAOSTAT food security and dietary indicators, with a focus on Ghana.

# Raw FAOSTAT CSV datasets (Resources)
1. Cost & Affordability of Healthy Diets (2017-2025)
2. Women's Dietary Diversity (2022 survey)
3. Food Balance (2010–2023)


## Dataset 1: Cost & Affordability of a Healthy Diet (CoAHD)

### Overview
- **Dataset Title:** FAOSTAT Cost & Affordability of a Healthy Diet (CoAHD)
- **Source & Domain:** FAOSTAT CAHD — July 2026 SOFI Release
- **Source File:** `FAOSTAT_CoAHD_Ghana.csv`
- **Geographic & Temporal Coverage:** Ghana (with regional Sahelian benchmark Mali), 2017–2025

### Methodology
Developed in partnership with **Tufts University** and the **World Bank’s Food Prices for Nutrition DataHub**. 

It calculates the least expensive combination of locally available foods that meets national Food-Based Dietary Guidelines (FBDGs) and WHO/FAO dietary standards, standardized to an adult energy requirement of **2,330 kcal/day**.

### Key Indicators & Variables

| Indicator | Variable Name in Dataset | Unit | What It Measures |
| :--- | :--- | :--- | :--- |
| **Total Diet Cost (PPP)** | Cost of a healthy diet (CoHD) | Int$ (PPP) / person / day | The international purchasing power cost to buy a nutritionally adequate diet. |
| **Total Diet Cost (Nominal)** | Cost of a healthy diet (CoHD) | LCU / person / day | The local currency cost (Ghanaian Cedis, GHS). |
| **Food Group Cost Subcomponents** | Cost of [Food Group] (6 groups) | Int$ (PPP) & LCU / day | Disaggregated daily cost for: Animal-source foods, Starchy staples, Legumes/nuts/seeds, Vegetables, Fruits, Oils/fats. |
| **Prevalence of Unaffordability** | Prevalence of unaffordability (PUA) | % of Population | The share of the population whose food expenditure budget is below the daily cost of a healthy diet. |
| **Headcount of Unaffordability** | Number of people unable to afford (NUA) | Millions of people | Absolute population locked out of healthy diets. |

---

## Dataset 2: Minimum Dietary Diversity for Women (MDD-W)

### Overview
- **Dataset Title:** FAOSTAT Minimum Dietary Diversity for Women (MDD-W)
- **Source & Domain:** FAOSTAT MDDW (Diversity — Minimum Dietary Diversity for Women) — 2022 Demographic and Health Survey (DHS) Integration
- **Source File:** `FAOSTAT_MDDW_Ghana.csv`
- **Geographic Levels:** Ghana (Disaggregated across National, Rural, and Urban populations)

### Methodology
Standardized population-level proxy indicator developed by the **FAO** and **USAID/FANTA** to track micronutrient adequacy in Women of Reproductive Age (15–49 years). 

A woman is considered to have achieved MDD-W if she consumed foods from **at least 5 out of 10 defined food groups** in the previous 24 hours.

### Key Indicators & Variables

| Indicator | Variable Name in Dataset | Unit | Categories / Details Tracked |
| :--- | :--- | :--- | :--- |
| **MDD-W Achievement Rate** | Percentage of women achieving MDD-W | % | Share of women consuming $\ge 5$ of the 10 food groups. |
| **Food Group Consumption Share** | Percentage of women consuming each food group | % | Proportion of women who consumed specific food groups over the recall period. |
| **Disaggregation Dimension** | Geographic Level | Categorical | National (`10000`), Rural (`10002`), Urban (`10001`). |

### Food Groups Tracked

#### 10 Core Food Groups (+ Sub-Categories)
1. **Grains, white roots and tubers, and plantains** *(Sub-split: Grains vs. White roots/tubers)*
2. **Pulses** *(beans, peas, and lentils)*
3. **Nuts and seeds**
4. **Dairy** *(milk, yogurt, cheese)*
5. **Meat, poultry, and fish**
6. **Eggs**
7. **Dark green leafy vegetables**
8. **Other vitamin A-rich fruits and vegetables**
9. **Vegetables, other**
10. **Fruits, other**

#### Non-MDD Food Groups Tracked
- Sweet foods
- Sweet beverages
- Fried/salty snacks
- Red palm oil

---

## Dataset 3: Food Balances (FBS) 

### Overview
- **Dataset Title:** FAOSTAT Food Balances (FBS)
- **Source & Domain:** FAOSTAT FBS (Food Balances 2010–2023) 
- **File / Script Source:** `FAOSTAT_FB_Ghana.csv` 
- **Geographic & Commodity Scope:** Ghana, 87 agricultural commodities across 14 years (2010–2023)

### Methodology
Compiles national supply-utilization accounts ($\text{Production} + \text{Imports} - \text{Exports} - \text{Feed/Seed} - \text{Waste}$) to determine the net per-capita daily food supply. 

The nutrient composition table converts raw food weights into bioavailable macro- and micronutrients.

### Key Indicators & Variables

| Indicator | Variable / Element | Unit | Details |
| :--- | :--- | :--- | :--- |
| **Dietary Energy Supply** | Food supply (kcal/capita/day) | kcal / cap / day | Daily per-capita caloric availability across 87 items. |
| **Protein Supply** | Protein supply quantity (g/capita/day) | g / cap / day | Disaggregated into Animal Products vs. Vegetal Products. |
| **Fat Supply** | Fat supply quantity (g/capita/day) | g / cap / day | Disaggregated lipid availability. |
| **Biochemical Nutrient Vectors** | `kcal`, `protein`, `iron`, `zinc`, `vit_a` | Per 100g edible portion | Biochemical nutritional parameters for local staples (millet, cassava, cowpeas, groundnuts, amaranth, dried fish). |

