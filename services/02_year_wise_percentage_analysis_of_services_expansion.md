# Product Requirements Document (PRD)

# Year Wise % of Services Expansion Analysis (2023–2025)

---

## 1. Objective

To measure the **percentage-based expansion of services year-over-year** within the GCC ecosystem from 2023 to 2025.

This use case focuses specifically on:

- Year-wise percentage growth in total services
- Percentage of new services introduced each year
- Service expansion momentum
- Relative (not just absolute) growth analysis

---

## 2. Scope

### This analysis includes:

- All active services mapped to GCC centers
- Year-wise service data (2023, 2024, 2025)
- Unique service count tracking
- Percentage-based growth metrics

### This analysis excludes:

- Revenue contribution per service
- Service quality or performance evaluation
- Department-level segmentation

---

# Use Case 2: Year Wise % of Services Expansion Analysis

---

## 3. Key Growth Metrics

---

## 3.1 Year-over-Year % Growth in Total Services

**Definition:**  
Percentage growth in total unique services compared to the previous year.

### Formula:

For 2024:

((Services_2024 - Services_2023) / Services_2023) * 100


For 2025:

((Services_2025 - Services_2024) / Services_2024) * 100


**Purpose:**  
To determine whether service diversification is accelerating or slowing.

---

## 3.2 Three-Year % Growth in Services (2023–2025)

**Definition:**  
Overall percentage growth across the full three-year period.

### Formula:

((Services_2025 - Services_2023) / Services_2023) * 100


**Insight:**  
Measures long-term service expansion trajectory.

---

## 3.3 % Contribution of Each Year to Total 3-Year Growth

**Definition:**  
Proportion of total service growth contributed by each year.

### Formula:

For 2024 Contribution:

((Services_2024 - Services_2023) / (Services_2025 - Services_2023)) * 100


For 2025 Contribution:

((Services_2025 - Services_2024) / (Services_2025 - Services_2023)) * 100


**Purpose:**  
Identifies which year drove the majority of expansion.

---

## 3.4 % Increase in Services per Center

**Definition:**  
Percentage growth in average number of services offered per center.

### Formula:

((Avg_Services_Per_Center_2025 - Avg_Services_Per_Center_2023)
/ Avg_Services_Per_Center_2023) * 100


**Insight:**  
Measures capability deepening within centers.

---

## 3.5 % of Centers Expanding Service Portfolio

**Definition:**  
Percentage of centers that increased their number of services between comparison years.

### Condition Example:

Services_Per_Center_2025 > Services_Per_Center_2023


### Percentage Formula:

(Expansion_Centers / Total_Centers) * 100


**Purpose:**  
Determines breadth of service expansion across the ecosystem.

---

## 4. Data Requirements (From Services Table)

The following fields are required:

- `service_id`
- `service_name`
- `center_unique_id`
- `year`
- `service_category` (if available)
- `service_status`

Additional required from Centers table:

- `center_unique_id`
- `center_status`

---
