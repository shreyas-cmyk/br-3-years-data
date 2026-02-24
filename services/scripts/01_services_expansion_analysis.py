import pandas as pd
from sqlalchemy import create_engine

# ---------------- STEP 1: POSTGRES CONNECTION ----------------
conn_string = (
   "Enter your DB connection String"
)

engine = create_engine(conn_string)

# ---------------- STEP 2: READ SERVICES TABLE ----------------
query = """
SELECT 
    year,
    cn_unique_key,
    it,
    erd,
    fna,
    hr,
    procurement_and_supply_chain,
    sales_and_marketing,
    customer_services
FROM services
WHERE year IN ('2023','2024','2025')
"""

df = pd.read_sql(query, engine)

# ---------------- STEP 3: CLEAN SERVICE FLAGS ----------------
service_columns = [
    "it",
    "erd",
    "fna",
    "hr",
    "procurement_and_supply_chain",
    "sales_and_marketing",
    "customer_services"
]

for col in service_columns:
    df[col] = df[col].apply(lambda x: 1 if pd.notna(x) and str(x).strip() != "" else 0)

# ---------------- STEP 4: TOTAL CENTERS PER YEAR ----------------
total_centers = df.groupby("year")["cn_unique_key"].nunique().reset_index()
total_centers.columns = ["year", "total_centers"]

# ---------------- STEP 5: SERVICE COUNTS PER YEAR ----------------
service_counts = df.groupby("year")[service_columns].sum().reset_index()

# ---------------- STEP 6: FINAL OUTPUT ----------------
final_table = service_counts.merge(total_centers, on="year")

print("\n===== USE CASE 1: SERVICES EXPANSION ANALYSIS =====")
print(final_table)
