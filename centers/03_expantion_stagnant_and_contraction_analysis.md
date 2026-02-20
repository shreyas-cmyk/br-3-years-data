# Product Requirements Document (PRD)

# Expansion, Stagnant, Contraction Analysis (2023–2025)

---

## 1. Objective

To classify GCC centers based on their growth behavior between 2023 and 2025 into three categories:

- Expansion
- Stagnant
- Contraction

This use case aims to evaluate the health and momentum of the GCC ecosystem by identifying whether centers are scaling, remaining stable, or shrinking.

---

## 2. Scope

### This analysis includes:

- All active GCC-type centers across 2023, 2024, and 2025
- Year-wise center-level comparison
- Growth behavior classification based on employee count or operational size

### This analysis excludes:

- Account-level financial analysis
- New center entry classification (covered separately)
- Workforce segmentation by department

---

## 3. Classification Framework

Each center will be classified based on its size change over time.

---

# Use Case 3: Expansion, Stagnant, Contraction Analysis

---

## 3.1 Expansion

**Definition:**  
Centers that show an increase in size between two comparison years.

**Condition Example (Headcount Based):**

Headcount_2025 > Headcount_2023


**Interpretation:**  
Indicates scaling activity and business growth at the center level.

---

## 3.2 Stagnant

**Definition:**  
Centers with no significant change in size between comparison years.

**Condition Example:**

Headcount_2025 = Headcount_2023


(Optional: Allow small variance threshold if required)

**Interpretation:**  
Indicates operational stability but no expansion.

---

## 3.3 Contraction

**Definition:**  
Centers that show a reduction in size between comparison years.

**Condition Example:**

Headcount_2025 < Headcount_2023


**Interpretation:**  
Indicates downsizing, restructuring, or reduced activity.

---

## 4. Growth Behavior Metrics

---

## 4.1 Total Centers by Classification

Count of centers in each category:

- Total Expansion Centers
- Total Stagnant Centers
- Total Contraction Centers

**Output Format Example:**

| Category     | Count | % of Total Centers |
|-------------|-------|--------------------|
| Expansion   | X     | A%                 |
| Stagnant    | Y     | B%                 |
| Contraction | Z     | C%                 |

---

## 4.2 Share of Ecosystem by Growth Behavior

**Formula:**

(Category_Count / Total_Centers) * 100


**Purpose:**  
To evaluate overall ecosystem health.

---

## 4.3 Net Workforce Contribution by Category

**Definition:**  
Measure how much total workforce change is driven by expansion vs contraction centers.

**Formula Example:**

Total_Headcount_Gain_from_Expansion -
Total_Headcount_Loss_from_Contraction


**Insight:**  
Identifies whether ecosystem growth is broad-based or concentrated.

---

## 4.4 Year-on-Year Behavior Shift

Analyze classification changes between:

- 2023 → 2024
- 2024 → 2025

Example transitions:

- Stagnant → Expansion
- Expansion → Contraction
- Contraction → Recovery

**Purpose:**  
To measure stability and volatility within the ecosystem.

---

## 5. Data Requirements (From Centers Table + Workforce Data)

Required fields:

- `center_unique_id`
- `account_unique_id`
- `year`
- `total_headcount`
- `center_status`
- `center_entry_year`

---

## 6. Expected Output

### A. Classification Summary

| Category     | 2023–2025 Count | % Share |
|-------------|------------------|--------|
| Expansion   | X                | A%     |
| Stagnant    | Y                | B%     |
| Contraction | Z                | C%     |

---

### B. Workforce Impact Table

| Category     | Net Workforce Change |
|-------------|----------------------|
| Expansion   | +N1                  |
| Contraction | -N2                  |
| Net Impact  | +M                   |

---

## 7. Executive Insights

- What % of centers are expanding vs shrinking?
- Is ecosystem growth broad-based or concentrated?
- Are contraction centers increasing year-over-year?
- Is 2025 showing recovery trends?

---

