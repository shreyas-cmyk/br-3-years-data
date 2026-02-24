import pandas as pd
from sqlalchemy import create_engine

# --------------------------------------------------
# 1️⃣ Database Connection
# --------------------------------------------------
connection_string = (
   "Enter your DB connection String"
)

engine = create_engine(connection_string)

# --------------------------------------------------
# 2️⃣ Fetch Data
# --------------------------------------------------
query = """
SELECT 
    account_global_legal_name,
    data_year,
    employee_count_cd,
    cn_unique_key
FROM centers
WHERE data_year IN ('2023','2024','2025')
"""

df = pd.read_sql(query, engine)

# --------------------------------------------------
# 3️⃣ Data Cleaning
# --------------------------------------------------

# Convert employee_count safely
df["employee_count_cd"] = pd.to_numeric(
    df["employee_count_cd"], errors="coerce"
).fillna(0)

# Convert year to string (keep consistent)
df["data_year"] = df["data_year"].astype(str)

# --------------------------------------------------
# 4️⃣ Create Pivot Table
# --------------------------------------------------
pivot = pd.pivot_table(
    df,
    index="account_global_legal_name",
    columns="data_year",
    values=["employee_count_cd", "cn_unique_key"],
    aggfunc={
        "employee_count_cd": "sum",
        "cn_unique_key": "count"
    },
    fill_value=0
)

pivot = pivot.sort_index(axis=1)

print("\n================ YEAR-WISE PIVOT TABLE ================\n")
print(pivot)

# --------------------------------------------------
# 5️⃣ Workforce Change (2023 → 2025)
# --------------------------------------------------

# Flatten columns
pivot.columns = [f"{col[0]}_{col[1]}" for col in pivot.columns]
pivot = pivot.reset_index()

# Ensure columns exist
for col in ["employee_count_cd_2023", "employee_count_cd_2025"]:
    if col not in pivot.columns:
        pivot[col] = 0

# Classification
def classify(row):
    if row["employee_count_cd_2025"] > row["employee_count_cd_2023"]:
        return "Workforce Expanded"
    elif row["employee_count_cd_2025"] < row["employee_count_cd_2023"]:
        return "Workforce Reduced"
    else:
        return "Workforce Stagnant"

pivot["Change_Type"] = pivot.apply(classify, axis=1)

change_counts = pivot["Change_Type"].value_counts()
total_centers = change_counts.sum()

expanded = change_counts.get("Workforce Expanded", 0)
reduced = change_counts.get("Workforce Reduced", 0)
stagnant = change_counts.get("Workforce Stagnant", 0)

expanded_pct = round((expanded / total_centers) * 100, 2) if total_centers else 0
reduced_pct = round((reduced / total_centers) * 100, 2) if total_centers else 0
stagnant_pct = round((stagnant / total_centers) * 100, 2) if total_centers else 0

# --------------------------------------------------
# 6️⃣ Headcount Change
# --------------------------------------------------
pivot["Headcount_Diff"] = (
    pivot["employee_count_cd_2025"]
    - pivot["employee_count_cd_2023"]
)

headcount_expanded = pivot[pivot["Headcount_Diff"] > 0]["Headcount_Diff"].sum()
headcount_reduced = abs(
    pivot[pivot["Headcount_Diff"] < 0]["Headcount_Diff"].sum()
)

# --------------------------------------------------
# 7️⃣ Print Summary
# --------------------------------------------------

print("\n================ CHANGE SUMMARY (2023 → 2025) ================\n")

print("Change Type\t\tFrom 2023-2025 (No. Of Centers)")
print("------------------------------------------------------------")
print(f"Workforce Stagnant\t{stagnant}\t{stagnant_pct}%")
print(f"Workforce Expanded\t{expanded}\t{expanded_pct}%")
print(f"Workforce Reduced\t{reduced}\t{reduced_pct}%")
print(f"\nTotal Centers\t\t{total_centers}")

print("\nFrom 2023-2025 (Headcount Impact)")
print("------------------------------------------------------------")
print(f"Headcount Expanded\t{int(headcount_expanded):,}")
print(f"Headcount Reduced\t{int(headcount_reduced):,}")
