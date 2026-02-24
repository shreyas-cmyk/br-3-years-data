import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

# ---------------- DB CONNECTION ----------------
conn_string = (
     "Enter your DB URL"
)

engine = create_engine(
    conn_string,
    poolclass=NullPool,
    pool_pre_ping=True
)

# ---------------- STEP 1: FETCH DATA FROM VIEW ----------------
query = """
SELECT DISTINCT
    account_global_legal_name,
    entry_year_of_gcc_type_center
FROM public.vw_first_center_timeline_clean
WHERE entry_year_of_gcc_type_center IS NOT NULL
"""

df = pd.read_sql(query, engine)

print(f"✅ Fetched {len(df)} rows from view")

# ---------------- STEP 2: UPDATE br_data IN CHUNKS ----------------
chunk_size = 500
total_updated = 0

with engine.begin() as conn:
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]

        for _, row in chunk.iterrows():
            conn.execute(
                text("""
                    UPDATE public.br_data
                    SET entry_year_of_gcc = :entry_year
                    WHERE account_global_legal_name = :account_name
                """),
                {
                    "entry_year": row["entry_year_of_gcc_type_center"],
                    "account_name": row["account_global_legal_name"]
                }
            )

        total_updated += len(chunk)
        print(f"🔄 Updated {total_updated} records so far")

print("🎉 br_data.entry_year_of_gcc successfully populated from view!")
