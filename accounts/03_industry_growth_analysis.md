# Product Requirements Document: Industry-Wise Growth Analysis (2023–2025)

## 1. Objective
To track and analyze how different industry verticals have expanded their GCC presence in India over the 2023–2025 period.

## 2. Scope
Classifies all GCC-operating companies by their primary industry and tracks their cumulative growth over time.

## 3. Methodology

### 3.1 Industry Classification
Each company must be tagged with a **Primary Industry Classification** (e.g., Banking & Financial Services, Retail, Automotive, Healthcare).

### 3.2 Cumulative Tracking Logic
We track the **cumulative** count of accounts for each industry across three specific milestones:
1.  **Through 2023** (All accounts active by end of 2023)
2.  **Through 2024** (Counts from 2023 + New additions in 2024)
3.  **Through 2025** (Counts from 2024 + New additions in 2025 + Upcoming)

**Rule:** The counts are always cumulative.
*Example:*
- **Aerospace & Defense**:
    - Through 2023: 24 accounts
    - Added in 2024: +1
    - **Through 2024 Total:** 25
    - Added in 2025: +2
    - **Through 2025 Total:** 27

### 3.3 Ranking & Visualization
- **Ranking:** Industries should be ranked by their total account count (descending).
- **Consolidation:** Smaller categories with statistically insignificant numbers should be consolidated into an "Others" group to maintain report clarity.
- **Market Share:** Calculate each industry's percentage share of the total ecosystem for each time period to show shifts in industry mix (e.g., "Is BFSI's share growing or shrinking?").

## 4. Expected Outputs
- A data table or chart showing Industry vs. Time Period (2023, 2024, 2025).
- Share of Ecosystem analysis for top industries.
