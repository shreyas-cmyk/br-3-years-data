import pandas as pd
import psycopg2

# -------------------------------------------------
# DATABASE CONNECTION
# -------------------------------------------------
conn = psycopg2.connect(
   "enter your connection link"
)

# -------------------------------------------------
# BASE QUERY (Active + 2024 & 2025 only)
# -------------------------------------------------
base_query = """
SELECT
    employees_range_cd,
    center_type_cons,
    cl_city_type,
    industry,
    center_legal_name_cd,
    TRIM(inc_year_cd) AS inc_year,
    LOWER(TRIM(status_cd)) AS status
FROM public.centers_consolidated
WHERE TRIM(inc_year_cd) IN ('2024','2025')
  AND LOWER(TRIM(status_cd)) LIKE '%active%'
"""

df = pd.read_sql(base_query, conn)

print("\nTotal Records Fetched:", len(df))

# -------------------------------------------------
# FUNCTION TO GENERATE EXPANSION TABLE
# -------------------------------------------------
def generate_expansion_table(data, column_name, table_title):

    pivot = pd.pivot_table(
        data,
        index=column_name,
        columns="inc_year",
        values="center_legal_name_cd",
        aggfunc=pd.Series.nunique,
        fill_value=0
    ).reset_index()

    # Ensure both years exist
    for year in ["2024", "2025"]:
        if year not in pivot.columns:
            pivot[year] = 0

    # Calculate totals
    total_2024 = pivot["2024"].sum()
    total_2025 = pivot["2025"].sum()

    # Calculate percentages
    pivot["% 2024"] = round((pivot["2024"] / total_2024) * 100, 0)
    pivot["% 2025"] = round((pivot["2025"] / total_2025) * 100, 0)

    # Add Grand Total row
    grand_total = pd.DataFrame([{
        column_name: "Grand Total",
        "2024": total_2024,
        "2025": total_2025,
        "% 2024": "",
        "% 2025": ""
    }])

    final_df = pd.concat([pivot, grand_total], ignore_index=True)

    print(f"\n================ {table_title} ================\n")
    print(final_df.to_string(index=False))

    return final_df


# -------------------------------------------------
# 1️⃣ EXPANSION BY CENTER SIZE BAND
# -------------------------------------------------
generate_expansion_table(
    df,
    "employees_range_cd",
    "Expansion by Center Size Band (2024 vs 2025)"
)

# -------------------------------------------------
# 2️⃣ EXPANSION BY CENTER TYPE
# -------------------------------------------------
generate_expansion_table(
    df,
    "center_type_cons",
    "Expansion by Center Type (2024 vs 2025)"
)

# -------------------------------------------------
# 3️⃣ EXPANSION BY CITY TIER
# -------------------------------------------------
generate_expansion_table(
    df,
    "cl_city_type",
    "Expansion by City Tier (2024 vs 2025)"
)

# -------------------------------------------------
# 4️⃣ EXPANSION BY INDUSTRY
# -------------------------------------------------
generate_expansion_table(
    df,
    "industry",
    "Expansion by Industry (2024 vs 2025)"
)

conn.close()
print("\n✅ Script execution completed.")
