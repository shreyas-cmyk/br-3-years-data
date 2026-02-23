**# Product Requirements Document (PRD)

# Services Expansion Analysis (2023–2025)

---

## 1. Objective

To analyze the expansion of services offered by GCC centers from 2023 to 2025 using the **Services table** as the primary data source.

This use case evaluates:

- Growth in number of services
- Expansion of service portfolios across centers
- Diversification of capabilities within the GCC ecosystem
- Contribution of services to overall ecosystem maturity

---

## 2. Scope

### This analysis includes:

- All active services mapped to GCC centers
- Year-wise service tracking (2023, 2024, 2025)
- Unique service count growth
- Center-level service portfolio expansion
- Service-level contribution to ecosystem growth

### This analysis excludes:

- Financial metrics (revenue per service)
- Department-level operational breakdown
- Service quality or performance metrics

---

# Use Case 1: Services Expansion Analysis

---

## 3. Key Growth Metrics

---

## 3.1 Total Unique Services (Year-Wise)

**Definition:**  
Total number of distinct services offered across all centers for each year.

**Output Example:**

| Year | Total Unique Services |
|------|-----------------------|
| 2023 | X                     |
| 2024 | Y                     |
| 2025 | Z                     |

**Purpose:**  
Measures diversification of the GCC ecosystem.

---

## 3.2 Year-over-Year Service Growth

**Formula:**

For 2024:

((Services_2024 - Services_2023) / Services_2023) * 100


For 2025:

((Services_2025 - Services_2024) / Services_2024) * 100


**Insight:**  
Identifies acceleration or slowdown in service diversification.

---

## 3.3 Three-Year Service Growth Rate (2023–2025)

**Formula:**

((Services_2025 - Services_2023) / Services_2023) * 100


**Purpose:**  
Measures long-term expansion in service capabilities.

---

## 3.4 Service Adoption Across Centers

**Definition:**  
Number of centers offering each service.

**Formula Example:**

COUNT(DISTINCT center_unique_id) GROUP BY service_name


**Purpose:**  
Identifies widely adopted vs niche services.

---

## 3.5 Average Services per Center

**Definition:**  
Average number of services offered per center.

**Formula:**

Total_Service_Mappings / Total_Centers


Compare:
- 2023 vs 2025

**Insight:**  
Measures depth of capability within centers.

---

## 3.6 Net Service Additions

**Definition:**  
Number of new services introduced year-wise.

**Formula:**

Services_2024 - Services_2023
Services_2025 - Services_2024


**Purpose:**  
Tracks innovation momentum.

---

## 3.7 Service Expansion vs Stagnation (Optional)

Classify services as:

- Expanding (offered by more centers in 2025 vs 2023)
- Stagnant (same number of centers)
- Declining (fewer centers offering the service)

**Condition Example:**

Centers_Offering_Service_2025 > Centers_Offering_Service_2023


**Insight:**  
Identifies growing capabilities within the ecosystem.

---

## 4. Data Requirements (From Services Table)

The following fields are required:

- `service_id`
- `service_name`
- `center_unique_id`
- `account_unique_id`
- `year`
- `service_category` (if available)
- `service_status`

---

## 5. Expected Output

### A. Service Growth Summary

| Metric | 2023 | 2024 | 2025 |
|--------|------|------|------|
| Total Unique Services | X | Y | Z |
| YoY Growth % | — | A% | B% |
| 3-Year Growth % | — | — | C% |
| Avg Services per Center | M | N | O |

---

### B. Service Adoption Table

| Service Name | Centers (2023) | Centers (2025) | Growth % |
|--------------|----------------|----------------|----------|
| Data Analytics | X | Y | Z% |
| Finance Ops | A | B | C% |

---
**
