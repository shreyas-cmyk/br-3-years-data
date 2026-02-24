import pandas as pd
from sqlalchemy import create_engine

# --------------------------------------------------
# DB CONNECTION
# --------------------------------------------------
DB_URL = (
   "enter your connection link"
)

engine = create_engine(DB_URL)

# --------------------------------------------------
# SQL QUERY – INDUSTRY WISE ANALYSIS
# --------------------------------------------------
query = """
WITH base_counts AS (
    SELECT
        COALESCE(TRIM(industry), 'Others') AS industry,
        new_time_line,
        COUNT(*) AS center_count
    FROM centers_consolidated
    WHERE status_cd = 'Active Center'
      AND new_time_line IN ('Till 2023', '2024', '2025')
    GROUP BY COALESCE(TRIM(industry), 'Others'), new_time_line
),

pivot_counts AS (
    SELECT
        industry,
        SUM(CASE WHEN new_time_line = 'Till 2023' THEN center_count ELSE 0 END) AS till_2023,
        SUM(CASE WHEN new_time_line = '2024' THEN center_count ELSE 0 END) AS y2024,
        SUM(CASE WHEN new_time_line = '2025' THEN center_count ELSE 0 END) AS y2025
    FROM base_counts
    GROUP BY industry
),

final_calc AS (
    SELECT
        industry,

        y2024 AS "2024",
        y2025 AS "2025",
        till_2023 AS "Till 2023",

        (till_2023 + y2024 + y2025) AS "Grand Total",

        -- CUMULATIVE LOGIC
        till_2023 AS "CL 2023",
        (till_2023 + y2024) AS "CL 2024",
        (till_2023 + y2024 + y2025) AS "CL 2025"

    FROM pivot_counts
)

SELECT * FROM final_calc
ORDER BY industry;
"""

# --------------------------------------------------
# EXECUTION
# --------------------------------------------------
df = pd.read_sql(query, engine)

# --------------------------------------------------
# ADD GRAND TOTAL ROW
# --------------------------------------------------
totals = df.sum(numeric_only=True)
totals["industry"] = "Grand Total"

df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------
print(df)

print("\nSanity Check:")
print("Total 2024:", df["2024"].sum())
print("Total 2025:", df["2025"].sum())
print("Total Till 2023:", df["Till 2023"].sum())

