import pandas as pd
from sqlalchemy import create_engine

# --------------------------------------------------
# DB CONNECTION
# --------------------------------------------------
DB_URL = (
    "enter your connection link"
)

engine = create_engine(DB_URL)

# ==================================================
# 1️⃣ TOTAL ACCOUNTS (Distinct + Cumulative)
# ==================================================

accounts_query = """
WITH yearly_accounts AS (
    SELECT
        CASE
            WHEN entry_year_of_gcc ~ '^[0-9]+$'
                 AND entry_year_of_gcc::INT <= 2023 THEN 'Till 2023'
            WHEN entry_year_of_gcc = '2024' THEN '2024'
            WHEN entry_year_of_gcc = '2025' THEN '2025'
            ELSE 'Announced beyond 2025 or upcoming'
        END AS year_bucket,
        COUNT(DISTINCT account_global_legal_name) AS yearly_count
    FROM br_data
    GROUP BY 1
),
ordered AS (
    SELECT *,
        CASE
            WHEN year_bucket = 'Till 2023' THEN 1
            WHEN year_bucket = '2024' THEN 2
            WHEN year_bucket = '2025' THEN 3
            WHEN year_bucket = 'Announced beyond 2025 or upcoming' THEN 4
        END AS order_col
    FROM yearly_accounts
)
SELECT
    year_bucket,
    SUM(yearly_count) OVER (
        ORDER BY order_col
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS total_accounts
FROM ordered
ORDER BY order_col;
"""

accounts_df = pd.read_sql(accounts_query, engine)


# ==================================================
# 2️⃣ TOTAL CENTERS (Cumulative)
# ==================================================

centers_query = """
WITH yearly_centers AS (
    SELECT
        CASE
            WHEN new_time_line = 'Till 2023' THEN 'Till 2023'
            WHEN new_time_line = '2024' THEN '2024'
            WHEN new_time_line = '2025' THEN '2025'
            ELSE 'Announced beyond 2025 or upcoming'
        END AS year_bucket,
        COUNT(*) AS yearly_count
    FROM centers_consolidated
    WHERE status_cd = 'Active Center'
    GROUP BY 1
),
ordered AS (
    SELECT *,
        CASE
            WHEN year_bucket = 'Till 2023' THEN 1
            WHEN year_bucket = '2024' THEN 2
            WHEN year_bucket = '2025' THEN 3
            WHEN year_bucket = 'Announced beyond 2025 or upcoming' THEN 4
        END AS order_col
    FROM yearly_centers
)
SELECT
    year_bucket,
    SUM(yearly_count) OVER (
        ORDER BY order_col
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) AS total_centers
FROM ordered
ORDER BY order_col;
"""

centers_df = pd.read_sql(centers_query, engine)


# ==================================================
# 3️⃣ HEADCOUNT (same as before)
# ==================================================

headcount_query = """
SELECT
    CASE
        WHEN data_year ~ '^[0-9]+$'
             AND data_year::INT <= 2023 THEN 'Till 2023'
        WHEN data_year = '2024' THEN '2024'
        WHEN data_year = '2025' THEN '2025'
    END AS year_bucket,
    SUM(
        CASE
            WHEN employee_count_cd ~ '^[0-9]+$'
            THEN employee_count_cd::BIGINT
            ELSE 0
        END
    ) AS total_headcount
FROM centers
WHERE status_cd = 'Active Center'
GROUP BY 1;
"""

headcount_df = pd.read_sql(headcount_query, engine)

# Convert to Mn
headcount_df["headcount_mn"] = (
    headcount_df["total_headcount"] / 1_000_000
)


# ==================================================
# 4️⃣ MERGE ALL DATA
# ==================================================

df = accounts_df.merge(centers_df, on="year_bucket", how="outer")
df = df.merge(
    headcount_df[["year_bucket", "headcount_mn"]],
    on="year_bucket",
    how="left"
)

df = df.rename(columns={
    "year_bucket": "Years",
    "total_accounts": "Total Accounts",
    "total_centers": "Total Centers",
    "headcount_mn": "Headcount in Mn"
})

df = df.fillna(0)

order = [
    "Till 2023",
    "2024",
    "2025",
    "Announced beyond 2025 or upcoming"
]

df["Years"] = pd.Categorical(
    df["Years"],
    categories=order,
    ordered=True
)

df = df.sort_values("Years").reset_index(drop=True)


# ==================================================
# 5️⃣ CALCULATIONS
# ==================================================

row_2023 = df[df["Years"] == "Till 2023"].iloc[0]
row_2024 = df[df["Years"] == "2024"].iloc[0]
row_2025 = df[df["Years"] == "2025"].iloc[0]

# Expansion in GCC workforce
expansion_workforce = (
    (row_2025["Headcount in Mn"] -
     row_2023["Headcount in Mn"]) /
    row_2023["Headcount in Mn"]
)

# Net workforce addition
net_workforce_add = (
    (row_2025["Headcount in Mn"] -
     row_2024["Headcount in Mn"]) /
    (row_2025["Headcount in Mn"] -
     row_2023["Headcount in Mn"])
)

# Increase in total GCC accounts
increase_accounts = (
    (row_2025["Total Accounts"] -
     row_2023["Total Accounts"]) /
    row_2023["Total Accounts"]
)

# Growth in total centres
growth_centres = (
    (row_2025["Total Centers"] -
     row_2023["Total Centers"]) /
    row_2023["Total Centers"]
)

# Increase in average workforce per centre
avg_2023 = (
    row_2023["Headcount in Mn"] * 1_000_000 /
    row_2023["Total Centers"]
)

avg_2025 = (
    row_2025["Headcount in Mn"] * 1_000_000 /
    row_2025["Total Centers"]
)

increase_avg_workforce = (
    (avg_2025 - avg_2023) / avg_2023
)


# ================================================== 
# 6️⃣ FINAL OUTPUT
# ==================================================

print("\n===== USE CASE 2 OUTPUT =====\n")
print(df)

print("\n===== CALCULATED METRICS =====")
print("Expansion in GCC workforce:",
      round(expansion_workforce * 100, 2), "%")
print("Net workforce addition occurred:",
      round(net_workforce_add * 100, 2), "%")
print("Increase in total GCC accounts:",
      round(increase_accounts * 100, 2), "%")
print("Growth in total centres:",
      round(growth_centres * 100, 2), "%")
print("Increase in average workforce per centre:",
      round(increase_avg_workforce * 100, 2), "%")

engine.dispose()

