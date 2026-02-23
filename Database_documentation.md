# br-3-years-data
# GCC Analytics Database – Documentation

---

# 1. Database Overview

This database is designed to support **3-Year GCC Ecosystem Analysis (2023–2025)** including:

- Accounts Growth
- Centers Growth & Expansion
- Services Expansion
- BR Data Validation
- Entry Timeline Tracking for GCC-type Centers

The database is hosted on **Neon PostgreSQL (AWS – US East 1)**.

---

# 2. Database Schema Structure

The database currently contains:

## ✅ 5 Tables  
## ✅ 1 View

---

# 3. Tables Overview

---

## 3.1 `br_data`

**Source Workbook:**  
BR 3 Years CL Data, Sheet--->CL-BR-3Years

**Purpose:**
- Raw Business Registry data
- Account validation
- Cross-checking legal names
- Base reference for ecosystem tracking

---

## 3.2 `br_data_cons`

**Source Workbook:**  
BR 3 Years CL Data , Sheet--->BR 2025

**Purpose:**
- Consolidated / cleaned BR dataset
- Standardized version for analytics
- Used for reconciled account-level reporting

---

## 3.3 `centers`

**Source Workbook:**  
CM – 3 Years CL Data, Sheet--->CL-3 Years Data

**Purpose:**
- Raw center-level dataset
- Used for:
  - Year-wise center growth
  - Center type analysis
  - Entry timeline calculation
  - City & industry analysis
  - Expansion / contraction logic

---

## 3.4 `centers_consolidated`

**Source Workbook:**  
CM – 3 Years CL Data , Sheet--->CM-2025

**Purpose:**
- Cleaned / structured center dataset
- Used for analytics-ready queries
- Supports aggregation and reporting

---

## 3.5 `services`

**Source Workbook:**  
SM – 3 Years CL Data, Sheet--->SM-3 Years Data

**Purpose:**
- Service-level mapping per center
- Used for:
  - Services expansion analysis
  - Year-wise % service growth
  - Portfolio diversification tracking
  - Center-level service intensity analysis

---

# 4. View Overview

---

## 4.1 `vw_first_center_timeline_clean`

**Type:** Analytical View  

**Purpose:**
- Calculates first GCC-type center year per account
- Cleans incorporation year
- Excludes “Upcoming” where required
- Classifies entry year into:
  - 2023
  - 2024
  - 2025
  - Upcoming

This view supports:

- GCC Entry Timeline PRD
- Year-wise ecosystem growth tracking
- First center classification logic

## SQL Logic Used


CREATE OR REPLACE VIEW
  "public"."vw_first_center_timeline_clean" AS
WITH
  base AS (
    SELECT
      centers.account_global_legal_name,
      centers.center_type_cd,
      centers.status_cd,
      centers.inc_year_cd,
      CASE
        WHEN centers.inc_year_cd ~ '^\d{4}$'::text THEN centers.inc_year_cd::integer
        ELSE NULL::integer
      END AS inc_year_int
    FROM
      centers
  ),
  gcc_first AS (
    SELECT
      base.account_global_legal_name,
      min(base.inc_year_int) AS first_gcc_year
    FROM
      base
    WHERE
      (
        upper(
          TRIM(
            BOTH
            FROM
              base.center_type_cd
          )
        ) = ANY (
          ARRAY[
            'GCC',
            'GIC',
            'GCC/GIC',
            'SSC',
            'COE',
            'GBS',
            'R&D',
            'ENGINEERING & DESIGN',
            'IT',
            'ENGINEERING'
          ]
        )
      )
      AND base.inc_year_int IS NOT NULL
      AND base.status_cd <> 'Upcoming'
    GROUP BY
      base.account_global_legal_name
  ),
  non_gcc_first AS (
    SELECT
      base.account_global_legal_name,
      min(base.inc_year_int) AS first_non_gcc_year
    FROM
      base
    WHERE
      base.inc_year_int IS NOT NULL
      AND base.status_cd <> 'Upcoming'
    GROUP BY
      base.account_global_legal_name
  ),
  final_base AS (
    SELECT
      b.account_global_legal_name,
      b.center_type_cd,
      b.status_cd,
      b.inc_year_cd,
      COALESCE(g.first_gcc_year, n.first_non_gcc_year) AS first_center_timeline_int
    FROM
      base b
      LEFT JOIN gcc_first g ON b.account_global_legal_name = g.account_global_legal_name
      LEFT JOIN non_gcc_first n ON b.account_global_legal_name = n.account_global_legal_name
  )
SELECT
  account_global_legal_name,
  inc_year_cd AS incorporation_year,
  center_type_cd,
  status_cd,
  COALESCE(first_center_timeline_int::text, 'Upcoming') AS first_center_timeline,
  CASE
    WHEN first_center_timeline_int IS NULL THEN 'Upcoming'
    WHEN first_center_timeline_int <= 2023 THEN '2023'
    WHEN first_center_timeline_int = 2024 THEN '2024'
    WHEN first_center_timeline_int = 2025 THEN '2025'
    ELSE 'Upcoming'
  END AS entry_year_of_gcc_type_center
FROM
  final_base;

---

# 5. Data Source Architecture

All tables are populated from Google Sheets workbooks.

| Workbook Name | Database Tables |
|---------------|-----------------|
| CM – 3 Years CL Data | centers, centers_consolidated |
| SM – 3 Years CL Data | services |
| BR – 3 Years CL Data | br_data, br_data_cons |

Data Flow:

Google Sheets → Data Cleaning → PostgreSQL Tables → Views → Analytics Queries

---

# 6. Critical Data Push Guidelines (Mandatory Before Upload)

Before pushing data from Google Sheets into PostgreSQL:

---

## 6.1 Account Name Consistency

Ensure `account_global_legal_name` is:

- Spelled exactly the same across:
  - br_data
  - centers
  - services
- Case consistent
- No extra spaces
- Special characters match exactly

Even minor variations will break joins.

---

## 6.2 Column Name Matching

Column names in Google Sheets MUST match table columns exactly:

- Same spelling
- Same underscore format
- Same casing
- No trailing spaces

Mismatch will cause:
- Insert errors
- Join failures
- Analytics inconsistencies

---

## 6.3 Data Type Validation

Before push:

- Integer columns must contain only numeric values
- Year columns must be 4-digit numeric
- No mixed data types
- NULL values handled properly
- Text fields should not contain numeric artifacts

Especially validate:

- inc_year_cd
- status_cd
- center_type_cd

---

## 6.4 Year Format Standardization

Allowed:

2023
2024
2025


Not allowed:

23
FY23
2023-24
TBD


---

# 7. Analytical Coverage Supported by This Schema

The database supports:

- Year-wise Center Growth
- Center Type-wise Growth
- Expansion / Stagnation / Contraction Analysis
- Headcount Extension Analysis
- Tier 1 vs Tier 2 City Growth
- Industry-wise Analysis
- Services Expansion
- Year-wise % Services Growth
- GCC Entry Timeline Classification

---

# 8. Governance Best Practices

- Always validate row counts before and after data push
- Never push partially cleaned sheets
- Maintain version control of Google Sheets
- Use staging approach for major refresh
- Avoid manual production table edits
- Document any schema changes

---

# 9. Owner

Database created for:

**GCC Ecosystem 3-Year Analytics (2023–2025)**

Maintained for analytical and strategic reporting purposes.
