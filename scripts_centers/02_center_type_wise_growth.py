import psycopg2
import pandas as pd

# -------------------------------
# DB CONNECTION
# -------------------------------
DATABASE_URL = (
    "enter your connection link"
)

conn = psycopg2.connect(DATABASE_URL)

# -------------------------------
# FETCH DATA
# -------------------------------
query = """
SELECT
    account_global_legal_name,
    center_type_cons,
    new_time_line
FROM centers_consolidated
WHERE status_cd = 'Active Center'
AND new_time_line IN ('Till 2023','2024','2025');
"""

df = pd.read_sql(query, conn)
conn.close()

# -------------------------------
# BASE COUNTS (Centers-level)
# -------------------------------
base_counts = (
    df.groupby(["center_type_cons", "new_time_line"])
      .size()
      .reset_index(name="count")
)

# -------------------------------
# PIVOT → YEAR-WISE
# -------------------------------
pivot = base_counts.pivot(
    index="center_type_cons",
    columns="new_time_line",
    values="count"
).fillna(0)

# Ensure column order
pivot = pivot[["Till 2023", "2024", "2025"]]

# -------------------------------
# CUMULATIVE COUNTS
# -------------------------------
pivot["Till 2023"] = pivot["Till 2023"]
pivot["2024"] = pivot["Till 2023"] + pivot["2024"]
pivot["2025"] = pivot["2024"] + pivot["2025"]

pivot["Grand Total"] = pivot["2025"]

# -------------------------------
# GRAND TOTAL ROW
# -------------------------------
grand_total = pivot.sum().to_frame().T
grand_total.index = ["Grand Total"]

final_counts = pd.concat([pivot, grand_total])

# -------------------------------
# % SHARE CALCULATION
# -------------------------------
percent_df = final_counts.div(final_counts.loc["Grand Total"]) * 100
percent_df = percent_df.round(0).astype("Int64").astype(str) + "%"

# -------------------------------
# DISPLAY RESULTS
# -------------------------------
print("\n=== COUNTA of Account Global Legal Name (Centers) ===\n")
print(final_counts.to_string())

print("\n=== % Share by Center Type ===\n")
print(percent_df.drop(index="Grand Total").to_string())
