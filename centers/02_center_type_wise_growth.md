# Product Requirements Document (PRD)

# Center Type Wise GCC Growth Trends (2023–2025)

---

## 1. Objective

To measure and analyze the growth patterns of GCC centers segmented by **Center Type** (e.g., Captive, Shared Services, IT Services, R&D, etc.) from 2023 to 2025.

This use case evaluates how different types of centers are expanding and contributing to the overall GCC ecosystem growth.

---

## 2. Scope

### This analysis includes:

- All GCC-type centers categorized by `center_type`
- Year-wise segmentation (2023, 2024, 2025)
- Growth comparison across different center types
- Share contribution of each type to total ecosystem growth

### This analysis excludes:

- Workforce-level segmentation
- Financial metrics
- Account-only growth without center linkage

---

## 3. Key Growth Indicators

---

# Use Case 2: Center Type Wise Growth

---

## 3.1 Total Centers by Type per Year

**Definition:**  
Total number of centers grouped by `center_type` for each year.

**Purpose:**  
To understand structural composition of the ecosystem.

**Output Format Example:**

| Center Type | 2023 | 2024 | 2025 |
|-------------|------|------|------|
| Captive     | X    | Y    | Z    |
| IT Services | A    | B    | C    |
| R&D         | D    | E    | F    |

---

## 3.2 Year-over-Year (YoY) Growth by Center Type

**Definition:**  
Percentage growth of each center type year-over-year.

**Formula (for each type):**

For 2024:

((Type_Count_2024 - Type_Count_2023) / Type_Count_2023) * 100


For 2025:

((Type_Count_2025 - Type_Count_2024) / Type_Count_2024) * 100


**Goal:**  
To identify which center types are accelerating or slowing down.

---

## 3.3 Absolute Growth by Center Type

**Definition:**  
Net increase in number of centers for each type year-wise.

**Formula:**

Type_Count_2024 - Type_Count_2023
Type_Count_2025 - Type_Count_2024


**Insight:**  
Shows which type is driving ecosystem expansion in absolute numbers.

---

## 3.4 Three-Year Growth Rate by Center Type (2023–2025)

**Definition:**  
Overall percentage growth of each center type over the 3-year period.

**Formula:**

((Type_Count_2025 - Type_Count_2023) / Type_Count_2023) * 100


**Purpose:**  
To measure long-term expansion trends by type.

---

## 3.5 Contribution of Each Type to Total Growth

**Definition:**  
Percentage contribution of each center type to overall ecosystem growth.

**Formula:**

(Type_Total_Growth_2023_2025 / Total_Center_Growth_2023_2025) * 100


**Insight:**  
Identifies which center type is the primary growth driver of the GCC ecosystem.

---

## 3.6 Share of Ecosystem by Center Type

**Definition:**  
Percentage share of each center type in total centers for each year.

**Formula:**

(Type_Count / Total_Centers) * 100


**Compare:**
- Share in 2023 vs Share in 2025

**Insight:**  
Determines structural shifts in ecosystem composition.

---

## 4. Data Requirements (From Centers Table)

The following fields are required:

- `center_unique_id`
- `center_type`
- `account_unique_id`
- `center_entry_year`
- `center_status` (if applicable)
- `year` (snapshot year: 2023, 2024, 2025)

---

## 5. Expected Output

### A. Type-wise Growth Table

| Center Type | 2023 | 2024 | 2025 | 3-Year Growth % |
|-------------|------|------|------|------------------|
| Captive     | X    | Y    | Z    | P%               |
| IT Services | A    | B    | C    | Q%               |
| R&D         | D    | E    | F    | R%               |

---

### B. Contribution to Total Growth

| Center Type | Net Growth (2023–2025) | Contribution % |
|-------------|-------------------------|----------------|
| Captive     | N1                      | S%             |
| IT Services | N2                      | T%             |
| R&D         | N3                      | U%             |

---

## 6. Executive Insights

- Which center type is growing the fastest?
- Is growth concentrated in one category or diversified?
- Is ecosystem shifting toward IT Services, R&D, or Shared Services?
- Which type contributed most to total GCC expansion?

---
