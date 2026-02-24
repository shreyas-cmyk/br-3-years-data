import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

# ---------------- STEP 1: GOOGLE SHEETS AUTH ----------------
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
     "Enter your file credentials"
)
client = gspread.authorize(creds)

# ---------------- STEP 2: READ GOOGLE SHEET ----------------
sheet = client.open("CM Data new copy").worksheet("CL-3 Years Data")

df = get_as_dataframe(
    sheet,
    evaluate_formulas=True,
    dtype=str
).dropna(how="all")

# ---------------- STEP 3: NORMALIZE COLUMN NAMES ----------------
df.columns = (
    df.columns
      .str.strip()
      .str.lower()
      .str.replace("\n", " ")
      .str.replace("(", "", regex=False)
      .str.replace(")", "", regex=False)
      .str.replace(" ", "_")
      .str.replace(r"[^\w_]", "", regex=True)
)

# ---------------- STEP 4: FORCE EXACT DB COLUMN NAMES ----------------
expected_columns = [
    "last_updated_date",
    "account_global_legal_name",
    "industry",
    "cn_unique_key",
    "status_cd",
    "inc_year_cd",
    "announced_year",
    "month",
    "inc_year_notes",
    "updated_inc_year_link",
    "time_line",
    "end_year_cd",
    "center_legal_name_cd",
    "business_segment_cd",
    "business_sub_segment_cd",
    "center_management_partner",
    "jv_status_cd",
    "jv_name_cd",
    "center_type_cd",
    "center_type_tagging",
    "center_foucs_cd",
    "center_souce_link",
    "center_website_cd",
    "center_linkedin_page_cd",
    "address_cd",
    "city_cd",
    "state_cd",
    "zip_code_cd",
    "country_cd",
    "region_cd",
    "broadline_number_cd",
    "employee_count_cd",
    "employees_range_cd",
    "employee_source_link_cd",
    "comments_cd",
    "data_year"
]

df.rename(columns={
    "cn_uniquekey": "cn_unique_key",
    "inc_year": "inc_year_cd",
    "center_focus_cd": "center_foucs_cd",
    "center_source_link": "center_souce_link",
    "zip_code": "zip_code_cd",
    "employee_count": "employee_count_cd",
    "employees_range": "employees_range_cd",
    "employee_source_link": "employee_source_link_cd",
    "comments": "comments_cd"
}, inplace=True)

df.drop(columns=["id"], errors="ignore", inplace=True)

df = df[[c for c in expected_columns if c in df.columns]]

for col in expected_columns:
    if col not in df.columns:
        df[col] = None

df = df[expected_columns]
df = df.replace({"": None})

# ---------------- STEP 5: POSTGRES CONNECTION ----------------
conn_string = (
    "Enter your DB URL"
)

engine = create_engine(
    conn_string,
    poolclass=NullPool,
    pool_pre_ping=True
)

# ---------------- STEP 6 + 7: TRUNCATE + INSERT WITH PROGRESS ----------------
CHUNK_SIZE = 200   # 🔥 Safe for Neon (16399 rows ≈ 82 chunks)
total_rows = len(df)

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE public.centers"))
    print("🧹 centers table truncated")

    inserted = 0

    for start in range(0, total_rows, CHUNK_SIZE):
        end = start + CHUNK_SIZE
        chunk_df = df.iloc[start:end]

        chunk_df.to_sql(
            "centers",
            conn,
            if_exists="append",
            index=False,
            method="multi"   # ✅ SAFE with small chunks
        )

        inserted += len(chunk_df)
        print(f"✅ Inserted {inserted}/{total_rows} rows")

print("🎉 Database table 'centers' successfully refreshed from Google Sheet.")
