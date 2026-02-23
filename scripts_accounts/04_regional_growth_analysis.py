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
# 2️⃣ QUERY (Use Case 4 Logic - SAFE VERSION)
# -------------------------------------------------
query = """
WITH base AS (
    SELECT
        "HQ Region",
        "Account Global Legal Name",

        -- SAFE CASTING (handles blanks / NA / text values)
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
        "HQ Region",

        COUNT(DISTINCT CASE 
            WHEN entry_year = 2024 
            THEN "Account Global Legal Name" 
        END) AS "2024",

        COUNT(DISTINCT CASE 
            WHEN entry_year = 2025 
            THEN "Account Global Legal Name" 
        END) AS "2025",

        COUNT(DISTINCT CASE 
            WHEN entry_year <= 2023 
            THEN "Account Global Legal Name" 
        END) AS "Till 2023",

        COUNT(DISTINCT CASE 
            WHEN entry_year > 2025 
            THEN "Account Global Legal Name" 
        END) AS "Upcoming",

        COUNT(DISTINCT "Account Global Legal Name") AS "Grand Total"

    FROM base
    GROUP BY "HQ Region"
)

SELECT
    *,
    ("Till 2023" + "2024") AS "Cumulative 2024",
    ("Till 2023" + "2024" + "2025") AS "Cumulative 2025"
FROM agg
ORDER BY "HQ Region";
"""

# -------------------------------------------------
# 3️⃣ EXECUTE QUERY
# -------------------------------------------------
df = pd.read_sql(query, engine)

# -------------------------------------------------
# 4️⃣ ADD GRAND TOTAL ROW (Like Pivot Table)
# -------------------------------------------------
grand_total = df.sum(numeric_only=True)
grand_total["HQ Region"] = "Grand Total"

df = pd.concat([df, pd.DataFrame([grand_total])], ignore_index=True)

# -------------------------------------------------
# 5️⃣ DISPLAY RESULT
# -------------------------------------------------
print("\nUse Case 4 Output:\n")
print(df)

# -------------------------------------------------
# 6️⃣ OPTIONAL: EXPORT TO EXCEL
# -------------------------------------------------
df.to_excel("UseCase4_BR_Data.xlsx", index=False)

print("\nExcel file saved as UseCase4_BR_Data.xlsx")

