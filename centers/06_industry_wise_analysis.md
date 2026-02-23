# Product Requirements Document (PRD)

# Industry Wise GCC Analysis (2023–2025)

---

## 1. Objective

To analyze GCC ecosystem growth and structural distribution across industries from 2023 to 2025.

This use case evaluates:

- Which industries are driving GCC expansion
- Industry-wise center growth trends
- Workforce distribution by industry
- Structural shifts in industry dominance

---

## 2. Scope

### This analysis includes:

- All active GCC centers across 2023, 2024, and 2025
- Industry classification using `industry`
- Year-wise comparison of center counts and headcount
- Industry contribution to overall ecosystem growth

### This analysis excludes:

- Account-level financial metrics
- Department-level workforce breakdown
- Micro-segmentation within industries

---

## 3. Industry Classification Framework

Each center will be mapped to an industry category such as:

- BFSI
- IT / Technology
- Healthcare & Pharma
- Manufacturing
- Retail & E-commerce
- Telecom
- Automotive
- Others

Industry mapping should be standardized and consistent across years.

---

# Use Case 6: Industry Wise Analysis

---

## 4. Key Growth Metrics

---

## 4.1 Total Centers by Industry (Year-Wise)

**Definition:**  
Total number of GCC centers grouped by industry for each year.

**Output Format Example:**

| Industry       | 2023 | 2024 | 2025 |
|---------------|------|------|------|
| BFSI          | X    | Y    | Z    |
| IT / Tech     | A    | B    | C    |
| Healthcare    | D    | E    | F    |

**Purpose:**  
To understand industry composition of the ecosystem.

---

## 4.2 Year-over-Year Growth by Industry

**Formula:**

For 2024:

((Industry_Count_2024 - Industry_Count_2023) / Industry_Count_2023) * 100


For 2025:

((Industry_Count_2025 - Industry_Count_2024) / Industry_Count_2024) * 100


**Insight:**  
Identifies fast-growing industries.

---

## 4.3 Three-Year Growth Rate by Industry (2023–2025)

**Formula:**

((Industry_Count_2025 - Industry_Count_2023) / Industry_Count_2023) * 100


**Purpose:**  
Measures long-term expansion by industry.

---

## 4.4 Absolute Growth Contribution by Industry

**Definition:**  
Net increase in number of centers per industry between 2023 and 2025.

**Formula:**

Industry_Count_2025 - Industry_Count_2023


**Insight:**  
Shows which industries are driving ecosystem expansion in absolute terms.

---

## 4.5 Workforce Distribution by Industry

**Definition:**  
Total workforce grouped by industry.

**Formula Example:**

SUM(total_headcount) GROUP BY industry


Compare:
- 2023 vs 2025

**Purpose:**  
To measure workforce intensity across industries.

---

## 4.6 Share of Ecosystem by Industry

**Definition:**  
Percentage share of total centers belonging to each industry.

**Formula:**

(Industry_Count / Total_Centers) * 100


Compare:
- Share in 2023 vs Share in 2025

**Insight:**  
Detects structural shifts in ecosystem composition.

---

## 4.7 Contribution to Total Ecosystem Growth

**Definition:**  
Percentage of total center growth driven by each industry.

**Formula:**

(Industry_Total_Growth_2023_2025 / Total_Center_Growth_2023_2025) * 100


**Purpose:**  
Identifies dominant growth engines within the GCC ecosystem.

---

## 5. Data Requirements

The following fields are required:

- `center_unique_id`
- `account_unique_id`
- `industry`
- `year`
- `total_headcount`
- `center_status`
- `center_entry_year`

---

## 6. Expected Output

### A. Industry Growth Summary

| Industry | 2023 | 2024 | 2025 | 3-Year Growth % |
|----------|------|------|------|------------------|
| BFSI     | X    | Y    | Z    | P%               |
| IT/Tech  | A    | B    | C    | Q%               |
| Healthcare | D  | E    | F    | R%               |

---

### B. Workforce Contribution

| Industry | Net Workforce Change (2023–2025) |
|----------|-----------------------------------|
| BFSI     | +N1                               |
| IT/Tech  | +N2                               |
| Healthcare | +N3                             |

---

### C. Ecosystem Share Shift

| Industry | Share 2023 | Share 2025 | Change |
|----------|------------|------------|--------|
| BFSI     | A%         | B%         | ±C%    |
| IT/Tech  | D%         | E%         | ±F%    |

---

