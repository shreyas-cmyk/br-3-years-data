import pandas as pd
from sqlalchemy import create_engine

# -------------------------------------------------
# 1️⃣ DATABASE CONNECTION
# -------------------------------------------------
connection_string = (
    "enter your connection link"
)

engine = create_engine(connection_string)

# -------------------------------------------------
# 2️⃣ BASE QUERY (CATEGORY LEVEL AGGREGATION)
# -------------------------------------------------
query = """
WITH base AS (
    SELECT
        "Primary Category",
        "Account Global Legal Name",
        CAST(
            NULLIF(
                REGEXP_REPLACE("Entry year of GCC", '[^0-9]', '', 'g'),
                ''
            ) AS INT
        ) AS entry_year
    FROM public."br_data_cons"
),

agg AS (
    SELECT
        "Primary Category",

        COUNT(DISTINCT CASE WHEN entry_year = 2024 THEN "Account Global Legal Name" END) AS "2024",
        COUNT(DISTINCT CASE WHEN entry_year = 2025 THEN "Account Global Legal Name" END) AS "2025",
        COUNT(DISTINCT CASE WHEN entry_year <= 2023 THEN "Account Global Legal Name" END) AS "Till 2023",
        COUNT(DISTINCT CASE WHEN entry_year > 2025 THEN "Account Global Legal Name" END) AS "Upcoming",
        COUNT(DISTINCT "Account Global Legal Name") AS "Grand Total"

    FROM base
    GROUP BY "Primary Category"
)

SELECT
    *,
    ("Till 2023" + "2024") AS "Cumulative 2024",
    ("Till 2023" + "2024" + "2025") AS "Cumulative 2025"
FROM agg
ORDER BY "Primary Category";
"""

df = pd.read_sql(query, engine)

# -------------------------------------------------
# 3️⃣ ADD GRAND TOTAL ROW
# -------------------------------------------------
grand_total = df.sum(numeric_only=True)
grand_total["Primary Category"] = "Grand Total"
df = pd.concat([df, pd.DataFrame([grand_total])], ignore_index=True)

print("\n--- FULL CATEGORY LEVEL OUTPUT ---\n")
print(df)

# -------------------------------------------------
# 4️⃣ KEEP ONLY TOP CATEGORIES & PUT REST IN OTHERS
# -------------------------------------------------
top_categories = [
    "Hi-Tech",
    "Industrial",
    "IT Service",
    "Professional Services",
    "BFSI",
    "Pharma & Life Sciences",
    "Electronics",
    "Automotive",
    "Chemicals"
]

filtered_df = df[df["Primary Category"].isin(top_categories)].copy()

others_df = df[
    (~df["Primary Category"].isin(top_categories)) &
    (df["Primary Category"] != "Grand Total")
]

others_sum = others_df.sum(numeric_only=True)
others_sum["Primary Category"] = "Others"

filtered_df = pd.concat(
    [filtered_df, pd.DataFrame([others_sum])],
    ignore_index=True
)

# -------------------------------------------------
# 5️⃣ ADD GRAND TOTAL AGAIN
# -------------------------------------------------
final_total = filtered_df.sum(numeric_only=True)
final_total["Primary Category"] = "Grand Total"

filtered_df = pd.concat(
    [filtered_df, pd.DataFrame([final_total])],
    ignore_index=True
)

# -------------------------------------------------
# 6️⃣ CALCULATE PERCENTAGE SHARE
# -------------------------------------------------
percent_df = filtered_df.copy()

years = ["Till 2023", "Cumulative 2024", "Cumulative 2025"]

grand_totals = percent_df[percent_df["Primary Category"] == "Grand Total"]

for year in years:
    total_value = grand_totals.iloc[0][year]
    percent_df[year] = round((percent_df[year] / total_value) * 100, 0)

percent_df = percent_df[percent_df["Primary Category"] != "Grand Total"]

print("\n--- TOP CATEGORY OUTPUT ---\n")
print(filtered_df)

print("\n--- PERCENTAGE SHARE OUTPUT ---\n")
print(percent_df)


