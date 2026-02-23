# Product Requirements Document (PRD)

# City Wise Growth Analysis – Tier 1 vs Tier 2 (2023–2025)

---

## 1. Objective

To analyze GCC ecosystem growth across cities from 2023 to 2025, with a specific focus on:

- Tier 1 Cities
- Tier 2 Cities

This use case evaluates geographic expansion patterns and determines whether GCC growth is concentrated in major metros or expanding into emerging cities.

---

## 2. Scope

### This analysis includes:

- All active GCC centers across 2023, 2024, and 2025
- City-level segmentation using `city`
- Tier classification (Tier 1 / Tier 2)
- Year-wise comparison of center counts and headcount
- Growth comparison between Tier 1 and Tier 2 cities

### This analysis excludes:

- Account-level financial metrics
- Department-level workforce segmentation
- Micro-location analysis within cities

---

## 3. Tier Classification Framework

Cities will be classified into:

- Tier 1 (Major metro cities)
- Tier 2 (Emerging and growth cities)

### Example Tier 1 Cities (Illustrative)

- Bangalore
- Hyderabad
- Chennai
- Pune
- Mumbai
- Delhi NCR

All other qualifying GCC cities will be categorized as Tier 2 unless separately defined.

---

# Use Case 5: City Wise Growth Analysis – Tier 1 vs Tier 2

---

## 4. Key Growth Metrics

---

## 4.1 Total Centers by City (Year-Wise)

**Definition:**  
Total number of centers in each city for 2023, 2024, and 2025.

**Output Format Example:**

| City      | 2023 | 2024 | 2025 |
|----------|------|------|------|
| Bangalore| X    | Y    | Z    |
| Hyderabad| A    | B    | C    |

**Purpose:**  
To identify city-level growth leaders.

---

## 4.2 Total Centers by Tier (Year-Wise)

**Definition:**  
Aggregate center count grouped by Tier 1 and Tier 2.

**Output Example:**

| Tier    | 2023 | 2024 | 2025 |
|---------|------|------|------|
| Tier 1  | X    | Y    | Z    |
| Tier 2  | A    | B    | C    |

---

## 4.3 Year-over-Year Growth by Tier

**Formula:**

For 2024:

((Tier_Count_2024 - Tier_Count_2023) / Tier_Count_2023) * 100


For 2025:

((Tier_Count_2025 - Tier_Count_2024) / Tier_Count_2024) * 100


**Insight:**  
Determines whether growth momentum is shifting toward Tier 2 cities.

---

## 4.4 Three-Year Growth Rate by Tier (2023–2025)

**Formula:**

((Tier_Count_2025 - Tier_Count_2023) / Tier_Count_2023) * 100


**Purpose:**  
To measure long-term geographic expansion trends.

---

## 4.5 Workforce Growth by Tier

**Definition:**  
Total workforce change grouped by Tier 1 vs Tier 2 cities.

**Formula Example:**

SUM(Headcount_2025 - Headcount_2023) GROUP BY Tier


**Insight:**  
Determines whether Tier 2 cities are gaining workforce share.

---

## 4.6 Share of Ecosystem by Tier

**Definition:**  
Percentage share of total centers located in each tier.

**Formula:**

(Tier_Count / Total_Centers) * 100


Compare:
- Share in 2023 vs Share in 2025

**Insight:**  
Measures decentralization of GCC ecosystem.

---

## 4.7 Contribution of Tier 2 to Total Growth

**Definition:**  
Percentage of total ecosystem center growth driven by Tier 2 cities.

**Formula:**

(Tier2_Total_Growth_2023_2025 / Total_Center_Growth_2023_2025) * 100


**Purpose:**  
To evaluate emergence of new GCC hubs.

---
