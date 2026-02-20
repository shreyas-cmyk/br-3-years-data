# Product Requirements Document (PRD)

# Headcount Expansion, Stagnant & Contraction Analysis (2023–2025)

---

## 1. Objective

To analyze workforce dynamics within GCC centers from 2023 to 2025 by classifying headcount behavior into:

- Headcount Expansion
- Headcount Stagnant
- Headcount Contraction

This use case focuses specifically on **workforce movement within existing centers**, independent of new center additions.

---

## 2. Scope

### This analysis includes:

- All active GCC centers across 2023, 2024, and 2025
- Year-wise comparison of total headcount per center
- Workforce growth classification based on headcount change
- Aggregate ecosystem-level workforce behavior insights

### This analysis excludes:

- New center entry classification (covered in separate PRD)
- Financial or revenue metrics
- Department-level workforce segmentation

---

## 3. Classification Framework

Each center will be classified based on headcount movement between comparison years.

Primary comparison window:
- 2023 → 2025 (3-year analysis)
Optional:
- 2023 → 2024
- 2024 → 2025

---

# Use Case 4: Headcount Expansion, Stagnant & Contraction Analysis

---

## 3.1 Headcount Expansion

**Definition:**  
Centers that increased their total headcount over the comparison period.

**Condition:**

Headcount_2025 > Headcount_2023


**Optional Threshold-Based Classification (Advanced):**

((Headcount_2025 - Headcount_2023) / Headcount_2023) * 100 > X%


**Interpretation:**  
Indicates operational scale-up and business growth within existing centers.

---

## 3.2 Headcount Stagnant

**Definition:**  
Centers with no significant change in headcount.

**Condition:**

Headcount_2025 = Headcount_2023


(Optional threshold range example: ±5%)

**Interpretation:**  
Indicates operational stability without major scaling.

---

## 3.3 Headcount Contraction

**Definition:**  
Centers that experienced a reduction in total headcount.

**Condition:**

Headcount_2025 < Headcount_2023


**Interpretation:**  
Indicates downsizing, restructuring, or reduced operational intensity.

---

## 4. Workforce Behavior Metrics

---

## 4.1 Total Centers by Headcount Behavior

| Category             | Count | % of Total Centers |
|----------------------|-------|--------------------|
| Expansion            | X     | A%                 |
| Stagnant             | Y     | B%                 |
| Contraction          | Z     | C%                 |

**Formula for % Share:**

(Category_Count / Total_Centers) * 100


---

## 4.2 Total Workforce Contribution by Category

Measure how much each category contributes to overall workforce change.

### Net Workforce Added by Expansion Centers

SUM(Headcount_2025 - Headcount_2023 WHERE Category = 'Expansion')


### Total Workforce Lost by Contraction Centers

SUM(Headcount_2023 - Headcount_2025 WHERE Category = 'Contraction')


### Net Ecosystem Workforce Change

Total_Expansion_Gain - Total_Contraction_Loss


---

## 4.3 Share of Workforce Growth by Expansion Centers

**Definition:**  
Percentage of total ecosystem workforce growth driven by expansion centers.

(Total_Expansion_Gain / Total_Net_Workforce_Growth) * 100


**Insight:**  
Determines whether ecosystem growth is broad-based or concentrated.

---

## 4.4 Year-on-Year Workforce Behavior Shift

Analyze classification changes across:

- 2023 → 2024
- 2024 → 2025

Example transitions:

- Contraction → Expansion (Recovery)
- Expansion → Contraction (Risk)
- Stagnant → Expansion (Acceleration)

**Purpose:**  
To assess ecosystem volatility and resilience.

---

## 5. Data Requirements

The following fields are required:

- `center_unique_id`
- `account_unique_id`
- `year`
- `total_headcount`
- `center_status`
- `center_entry_year`

---

## 6. Expected Output

### A. Headcount Behavior Summary

| Category     | Centers Count | Workforce Impact |
|--------------|--------------|------------------|
| Expansion    | X            | +N1              |
| Stagnant     | Y            | 0                |
| Contraction  | Z            | -N2              |
| Net Change   | —            | +M               |

---

### B. Year-wise Workforce Change

| Year Comparison | Expansion | Stagnant | Contraction |
|----------------|----------|----------|-------------|
| 2023–2024     | A        | B        | C           |
| 2024–2025     | D        | E        | F           |

---
