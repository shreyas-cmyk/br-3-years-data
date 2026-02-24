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
sheet = client.open("Copy of SM-3-Years CL Data").worksheet("SM-3 Years Data")

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
    "last_update_date",
    "account_global_legal_name",
    "cn_unique_key",
    "key",
    "center_legal_name",
    "center_type",
    "center_focus",
    "center_souce_link",
    "city",
    "primary_services_foucs",
    "primary_services_source",
    "focus_region",
    "focus_region_source_link",
    "it",
    "it_source_link",
    "erd",
    "engineering_source_link",
    "fna",
    "fna_source_link",
    "hr",
    "hr_source_link",
    "procurement_and_supply_chain",
    "procurement_and_supply_chain_source_link",
    "sales_and_marketing",
    "sales_and_marketing_source_link",
    "customer_services",
    "customer_services_source_link",
    "other_service",
    "other_source_link",
    "software_vendor",
    "software_in_use",
    "software_source_link",
    "comments",
    "year"
]

# Fix common header mismatches if needed
df.rename(columns={
    "center_source_link": "center_souce_link",
    "primary_services_focus": "primary_services_foucs"
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
CHUNK_SIZE = 200
total_rows = len(df)

with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE public.services"))
    print("🧹 services table truncated")

    inserted = 0

    for start in range(0, total_rows, CHUNK_SIZE):
        end = start + CHUNK_SIZE
        chunk_df = df.iloc[start:end]

        chunk_df.to_sql(
            "services",
            conn,
            if_exists="append",
            index=False,
            method="multi"
        )

        inserted += len(chunk_df)
        print(f"✅ Inserted {inserted}/{total_rows} rows")

print("🎉 Database table 'services' successfully refreshed from Google Sheet.")
