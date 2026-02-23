import pandas as pd
from sqlalchemy import create_engine

# ---------------- DB CONNECTION ----------------
db_url = (
    "enter your connection link"
)

engine = create_engine(db_url)

# ---------------- QUERY (CENTER COUNTS) ----------------
query = """
SELECT
    new_time_line,
    COUNT(*) AS center_count
FROM centers_consolidated
WHERE UPPER(TRIM(status_cd)) = 'ACTIVE CENTER'
GROUP BY new_time_line;
"""

df = pd.read_sql(query, engine)

# ---------------- NORMALIZE ORDER ----------------
order = ['Till 2023', '2024', '2025']
df = df[df['new_time_line'].isin(order)]
df['new_time_line'] = pd.Categorical(
    df['new_time_line'], categories=order, ordered=True
)
df = df.sort_values('new_time_line')

# ---------------- CUMULATIVE LOGIC ----------------
df['cumulative_centers'] = df['center_count'].cumsum()

# ---------------- FINAL FORMAT ----------------
final_df = df[['new_time_line', 'cumulative_centers']]
final_df.columns = ['New Time Line', 'Center Count']

print(final_df)
