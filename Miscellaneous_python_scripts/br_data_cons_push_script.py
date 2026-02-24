import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine, text

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
sheet = client.open(
    "BR Data new copy"
).worksheet("BR 2025")

df = get_as_dataframe(
    sheet,
    evaluate_formulas=True,
    dtype=str
).dropna(how="all")

# ---------------- STEP 3: KEEP ORIGINAL COLUMN NAMES ----------------
# (Important because DB column names contain spaces & special characters)
df.columns = df.columns.str.strip()

# ---------------- STEP 4: ENSURE COLUMN ORDER MATCHES DB ----------------
db_columns = [
    "Date",
    "Nasscom Status",
    "Nasscom Member Status",
    "Account Global Legal Name",
    "About Company",
    "HQ Address",
    "HQ City",
    "HQ State",
    "HQ ZIP Code",
    "HQ Country",
    "HQ Region",
    "HQ Broad Line",
    "HQ Website",
    "Linkedin Link",
    "HQ Offerings",
    "Source Link HQ Offering",
    "HQ Sub Industry",
    "HQ Industry",
    "Primary Category",
    "Primary Nature",
    "HQ Forbes Rank 2024",
    "HQ Fortune Rank 2024",
    "HQ Company Type",
    "HQ Revenue in USD Mil",
    "HQ Revenue Range",
    "HQ FY End",
    "HQ Revenue Year",
    "Source Type HQ Revenue",
    "Source Link HQ Revenue",
    "HQ Employee Count",
    "HQ Employee Range",
    "Source Type HQ Employee",
    "Source Link HQ Employee",
    "Comments CD",
    "Year",
    "Entry year of GCC"
]

# Keep only required columns
df = df[db_columns]

# ---------------- STEP 5: POSTGRES CONNECTION ----------------
conn_string = (
     "Enter your DB URL"
)

engine = create_engine(conn_string)

# ---------------- STEP 6: TRUNCATE TABLE ----------------
with engine.begin() as conn:
    conn.execute(text('TRUNCATE TABLE public."br_data_cons"'))

# ---------------- STEP 7: INSERT DATA ----------------
df.to_sql(
    "br_data_cons",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("✅ Database table 'br_data_cons' successfully refreshed from Google Sheet.")

engine.dispose()
