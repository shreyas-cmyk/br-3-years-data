# BR 3 Years Data - Project Overview

## 1. Detailed Project Objective
The central objective of this project is to support a comprehensive **3-Year GCC Ecosystem Analysis (2023–2025)** by tracking and analyzing quantitative and qualitative data around Global Capability Centers (GCCs) in India. The analytical data pipelines and scripts answer core strategic questions regarding:
- **Determining Company GCC Entry Timeline**: Establishing exactly when an overarching account first established a GCC-type center in India.
- **Ecosystem Growth Trends (2023–2025)**: Measuring the massive expansion in total workforce, net new accounts established, and the count of total active centers.
- **Industry & Regional Footprint Analysis**: Tracking sector-wise and region-wise expansion to identify leading domain disruptors.
- **Services Expansion Analysis**: Understanding functional capability scaling across service portfolios (IT, ER&D, FNA, HR, Procurement, etc.).

- The system is hosted via **Neon PostgreSQL (AWS – US East 1)**.

---


## 2. Defining "GCC-Type Centers"
For all underlying analysis metrics, a rigorous definition is applied to what qualifies as an active GCC. 
A center is classified as a "GCC-Type Center" and thus calculated in the metrics **if and only if**:
- The explicit **status** (`status_cd`) is strictly equal to **"Active Center"**.
- The explicit **center type classification** (`center_type_cd`) falls into one of these specific strings mathematically validated by the SQL Views:
  - `GCC`, `GIC`, `GCC/GIC`, `SSC`, `COE`, `GBS`, `R&D`, `ENGINEERING & DESIGN`, `IT`, `ENGINEERING`.

---

## 3. Google Sheets Reference
The data originates primarily from three source Google Sheets workbooks which serve as the foundation of the pipeline:
- **BR 3 Years CL Data** (Source Workbook Name)
  - **Sheet:** `CL-BR-3Years` (Source mapped to `br_data` table)
  - **Sheet:** `BR 2025` (Source mapped to `br_data_cons` table)
- **CM – 3 Years CL Data** (Source Workbook Name)
  - **Sheet:** `CL-3 Years Data` (Source mapped to `centers` table)
  - **Sheet:** `CM-2025` (Source mapped to `centers_consolidated` table)
- **SM – 3 Years CL Data** (Source Workbook Name)
  - **Sheet:** `SM-3 Years Data` (Source mapped to `services` table)
 

All reporting pipelines follow this exact data flow architecture:
**Google Sheets → Data Cleaning (Python/Google Sheets) → PostgreSQL Tables → Filtered Views → Analytics Queries**

| Core Google Sheets Workbook | Relevant Internal Sheet | Target PostgreSQL Table |
|-----------------------------|-------------------------|--------------------------|
| **CM – 3 Years CL Data** | `CL-3 Years Data` | `centers` |
| **CM – 3 Years CL Data** | `CM-2025` | `centers_consolidated` |
| **SM – 3 Years CL Data** | `SM-3 Years Data` | `services` |
| **BR – 3 Years CL Data** | `CL-BR-3Years` | `br_data` |
| **BR – 3 Years CL Data** | `BR 2025` | `br_data_cons` |

## 3. Database Schema Mapping
A Neon PostgreSQL Database holds all cleaned structural tables that ingest the Google Sheets data:
- `br_data`: Contains raw business registry data and account validation details.
- `br_data_cons`: Consolidated and cleaned BR dataset exclusively for analytical reports.
- `centers`: Raw center-level dataset for growth, expansion, and location-based operations analysis.
- `centers_consolidated`: Cleaned center dataset strictly for aggregated year-wise tracking.
- `services`: Detailed tracking of service-levels and department footprints within each specific center.
- `vw_first_center_timeline_clean` (View): Logical construct designed to dynamically calculate the 2023 vs 2024 vs 2025 GCC entry buckets.

---


## 4. Mandatory Data Push & Quality Guidelines (Violation Checks)
Before data reaches the analytical states inside the Database, standard Python Scripts extract the Google Sheets and ingest it into PostgreSQL.

> [!WARNING]
> Before pushing any data to the DB, it is **mandatory** to verify these critical constraints across all raw files. Violating these rules will instantly break database JOIN commands.

### 4.1 Account Name Consistency
`account_global_legal_name` must be perfectly identical across `br_data`, `centers`, and `services`.
- Case consistency is required.
- **No extra blank spaces** allowed at start or end.
- All special characters must mirror each other exactly.

### 4.2 Column Name Formatting Matches
Google Sheet columns **must mirror** database columns identically. The target names are configured inside the Python Scripts (e.g. `br_data_push_script.py` normalizing step 3 & 4).
- Do not add random spaces or mixed casings. Follow standard PostgreSQL underscore `snake_case`.

### 4.3 Clean Datatype Casting
- Categorical `year` fields must strictly be 4 digits (Accepted: *2023, 2024, 2025*. Rejected: *23, FY23, 2023-24*).
- Status codes such as `status_cd` or `center_type_cd` cannot have numeric artifacts.
- Numeric `employee_count_cd` columns strictly cannot have hidden text (e.g. "5000 approx" will break the ETL).

---


## 5. Python & SQL Scripts Traceability & Explanation

### 5.1 SQL Scripts (`Miscellaneous_scripts` Folder)
These scripts handle database table schemas and views initializations.
- `br_data_table_create.sql`: Defines `br_data` schema mapping columns such as `account_global_legal_name`, `entry_year_of_gcc`, `hq_revenue_range`, and `nasscom_status`.
- `br_data_cons_table_create.sql`: Similar architectural definition for the heavily filtered `br_data_cons` set.
- `centers_table_create.sql`: Defines `centers` schema to map granular facilities tracking `center_type_cd`, `status_cd`, `inc_year_cd`, and `employee_count_cd`.
- `centers_consolidated_table_create.sql`: Defines `centers_consolidated` schema, crucial for utilizing the `new_time_line` column.
- `services_table_create.sql`: Defines `services` schema with specific binary flags (`it`, `erd`, `fna`, `hr`, `procurement_and_supply_chain`, `customer_services`).
- `vw_first_center_timeline_clean.sql`: Core logic SQL computing earliest GCC entry year per `account_global_legal_name` and classifying against center categories like 'SSC', 'GBS', 'R&D', using condition blocks on `inc_year_cd`.

### 5.2 Python Push Scripts (`Miscellaneous_python_scripts` Folder)
ETL scripts to extract data from the respective Google Sheets, normalize structural column headers, strictly format datasets, and append records directly to PostgreSQL.
- `br_data_push_script.py`: Target Table: `br_data` 
- `br_data_cons_push_script.py`: Target Table: `br_data_cons` 
- `centers_3y_data_push_script.py`: Target Table: `centers` 
- `centers_cons_push_script.py`: Target Table: `centers_consolidated` 
- `services_3y_data_push_script.py`: Target Table: `services` 
- `Gcc_entry_year_column_push_from_view.py`: Utility to pull calculated values from the `vw` structures and standardize database entries to main br_data table.

### 5.3 Accounts Growth Trends (`accounts/scripts` Folder)
- `01_gcc_entry_timeline.py`
  - **Objective:** Buckets existing accounts into "Till 2023", "2024", "2025" or "Upcoming".
  - **Tables Used:** `br_data`
  - **Columns Targeted:** `account_global_legal_name`, `entry_year_of_gcc`
- `02_ecosystem_growth_trends.py`
  - **Objective:** Calculates massive aggregate factors including expansion in existing workforce sizes, net new workforce editions, total cumulative center footprints, and baseline increases versus year 2023 bounds.
  - **Tables Used:** `br_data`, `centers_consolidated`, `centers`
  - **Columns Targeted:** `entry_year_of_gcc`, `new_time_line`, `status_cd` ('Active Center' filter), `employee_count_cd`, `data_year`
- `03_industry_growth_analysis.py`
  - **Objective:** Groups and tracks YoY accounts count categorized by distinct parent Industry mappings to see sectoral leadership changes.
- `04_regional_growth_analysis.py`
  - **Objective:** Calculates volumetric shifts split by primary Headquarter region to validate geopolitical investment originators context.

### 5.4 Centers Expansion Insights (`centers/scripts` Folder)
- `01_year_wise_center_growth.py`
  - **Objective:** Evaluates strictly absolute center counts against timeline buckets with cumulative cumulative sums.
  - **Tables Used:** `centers_consolidated`
  - **Columns Targeted:** `new_time_line`, `status_cd`
- `02_center_type_wise_growth.py`
  - **Objective:** Analyzes the segmented structural shifts between pure R&D facilities versus conventional Shared Service Centers (SSC).
- `03_expantion_stagnant_and_contraction_analysis.py`
  - **Objective:** Determines which specific GCC structures grew radically vs which stagnated over 3 years.
- `04_headcount_expantion_stagnant_and_contraction_analysis.py`
  - **Objective:** Numeric correlation comparing 2023 absolute headcounts directly against 2025 reported metrics.
- `05_city_wise_growth_analysis.py`
  - **Objective:** Distributions calculating geographic footprints and Tier-1 vs Tier-2 dispersion logic. 
- `06_industry_wise_analysis.py`
  - **Objective:** Matrix breakdown correlating pure center-capacities by respective industry domain tagging.

### 5.5 Service Offerings Tracks (`services/scripts` Folder)
- `01_services_expansion_analysis.py`
  - **Objective:** Iterates through boolean mapped columns to accurately identify aggregate shifts from IT-focused delivery to broad capability centers (multi-function presence).
  - **Tables Used:** `services`
  - **Columns Targeted:** `year`, `cn_unique_key`, `it`, `erd`, `fna`, `hr`, `procurement_and_supply_chain`, `sales_and_marketing`, `customer_services`.
- `02_year_wise_percentage_analysis_of_services_expansion.py`
  - **Objective:** Calculates proportional domain shifts, showing the relative acceleration of categories like ER&D comparing 2023 baselines to year 2025 totals.
  - **Tables Used:** `services`
  - **Columns Targeted:** `year`, `cn_unique_key`, `it`, `erd`, `fna`, `hr`, `procurement_and_supply_chain`, `sales_and_marketing`, `customer_services`.
 
---


## 6. Project Architecture Component Summary

1. **Table Creates (DDL Files):** Defined under `Miscellaneous_scripts/`. Directly translates the Google Sheets data dimensions into PostgreSQL native elements (e.g., `centers_table_create.sql`). Core logic for classifying what counts organically rests in `vw_first_center_timeline_clean.sql`.
2. **Push Pipeline Scripts:** Defined under `Miscellaneous_python_scripts/`. Ingest pipeline designed strictly to handle authentication logic, strip bad datatypes/white spacing configurations and blindly append into Neon DB infrastructure via pandas bulk `.to_sql()`. 
3. **Core Analytic Modules:** Folders (`accounts/`, `centers/`, `services/`) house the `psycopg2`/`sqlalchemy` mapping logic processing final cumulative aggregations and printing finalized formatted dataframes.

---
