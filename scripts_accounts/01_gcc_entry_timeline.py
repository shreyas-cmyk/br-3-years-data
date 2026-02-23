import psycopg2
import pandas as pd

# -------------------------------
# DB CONNECTION (Neon)
# -------------------------------
DATABASE_URL = ( "enter your connection link"
)

conn = psycopg2.connect(DATABASE_URL)

# -------------------------------
# FETCH DATA
# -------------------------------
query = """
SELECT DISTINCT
    account_global_legal_name,
    entry_year_of_gcc
FROM br_data;
"""

df = pd.read_sql(query, conn)
conn.close()

# -------------------------------
# YEAR BUCKETING LOGIC (FIXED)
# -------------------------------
def categorize_year(year):
    if pd.isna(year):
        return "Upcoming"

    year_str = str(year).strip()

    # Handle 'Upcoming' or any non-numeric text safely
    if not year_str.isdigit():
        return "Upcoming"

    year = int(year_str)

    if year < 2024:
        return "Till 2023"
    elif year == 2024:
        return "2024"
    elif year == 2025:
        return "2025"
    else:
        return "Upcoming"

df["Entry year of GCC (Till Year)"] = df["entry_year_of_gcc"].apply(categorize_year)

# -------------------------------
# AGGREGATION
# -------------------------------
result = (
    df.groupby("Entry year of GCC (Till Year)")["account_global_legal_name"]
      .nunique()
      .reset_index(name="COUNTA of Account Global Legal Name")
)

order = ["Till 2023", "2024", "2025", "Upcoming"]
result["Entry year of GCC (Till Year)"] = pd.Categorical(
    result["Entry year of GCC (Till Year)"],
    categories=order,
    ordered=True
)

result = result.sort_values("Entry year of GCC (Till Year)")

# -------------------------------
# GRAND TOTAL
# -------------------------------
grand_total = result["COUNTA of Account Global Legal Name"].sum()

# -------------------------------
# DISPLAY RESULT
# -------------------------------
print("\nEntry year of GCC (Till Year)\n")
print(result.to_string(index=False))
print("\nGrand Total:", grand_total)

