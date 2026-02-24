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
# SQL QUERY – USE CASE 3 (CITY + TIER + CUMULATIVE + %)
# --------------------------------------------------
query = """
WITH tier_mapping AS (
    SELECT city, tier FROM (
        VALUES
        ('Bengaluru', 'Tier 1'),
        ('Delhi NCR', 'Tier 1'),
        ('Pune', 'Tier 1'),
        ('Mumbai', 'Tier 1'),
        ('Hyderabad', 'Tier 1'),
        ('Chennai', 'Tier 1'),

        ('Ahmedabad', 'Tier 2'),
        ('Kolkata', 'Tier 2'),
        ('Vadodara', 'Tier 2'),
        ('Coimbatore', 'Tier 2'),
        ('Thiruvananthapuram', 'Tier 2'),
        ('Kochi', 'Tier 2'),
        ('Bharuch', 'Tier 2'),
        ('Thane', 'Tier 2')
    ) AS t(city, tier)
),

base_city_counts AS (
    SELECT
        TRIM(cl_city_type) AS city,
        new_time_line,
        COUNT(*) AS center_count
    FROM centers_consolidated
    WHERE status_cd = 'Active Center'
      AND new_time_line IN ('Till 2023', '2024', '2025')
    GROUP BY TRIM(cl_city_type), new_time_line
),

city_with_tier AS (
    SELECT
        COALESCE(t.tier, 'Others') AS tier,
        CASE
            WHEN t.tier IS NULL THEN 'Others'
            ELSE b.city
        END AS city,
        b.new_time_line,
        b.center_count
    FROM base_city_counts b
    LEFT JOIN tier_mapping t
        ON b.city = t.city
),

city_pivot AS (
    SELECT
        tier,
        city,
        SUM(CASE WHEN new_time_line = 'Till 2023' THEN center_count ELSE 0 END) AS till_2023,
        SUM(CASE WHEN new_time_line = '2024' THEN center_count ELSE 0 END) AS y2024,
        SUM(CASE WHEN new_time_line = '2025' THEN center_count ELSE 0 END) AS y2025
    FROM city_with_tier
    GROUP BY tier, city
),

city_cumulative AS (
    SELECT
        tier,
        city,
        till_2023,
        till_2023 + y2024 AS till_2024,
        till_2023 + y2024 + y2025 AS till_2025
    FROM city_pivot
),

year_totals AS (
    SELECT
        SUM(till_2023) AS total_2023,
        SUM(till_2024) AS total_2024,
        SUM(till_2025) AS total_2025
    FROM city_cumulative
)

SELECT
    c.tier,
    c.city,
    c.till_2023,
    c.till_2024,
    c.till_2025,
    ROUND(c.till_2023 * 100.0 / t.total_2023, 1) AS pct_2023,
    ROUND(c.till_2024 * 100.0 / t.total_2024, 1) AS pct_2024,
    ROUND(c.till_2025 * 100.0 / t.total_2025, 1) AS pct_2025
FROM city_cumulative c
CROSS JOIN year_totals t
ORDER BY
    CASE c.tier
        WHEN 'Tier 1' THEN 1
        WHEN 'Tier 2' THEN 2
        ELSE 3
    END,
    c.city;
"""

# --------------------------------------------------
# EXECUTION
# --------------------------------------------------
df = pd.read_sql(query, engine)

# --------------------------------------------------
# OUTPUT
# --------------------------------------------------
print(df)
print("\nSanity Check Totals:")
print(df[['till_2023', 'till_2024', 'till_2025']].sum())

