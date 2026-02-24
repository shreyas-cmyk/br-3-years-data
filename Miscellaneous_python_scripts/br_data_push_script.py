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
).worksheet("CL-BR-3Years")

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
      .str.replace(" ", "_")
      .str.replace(r"[()]", "_", regex=True)
      .str.replace(r"[^\w_]", "", regex=True)
)

# ---------------- STEP 4: ALIGN COLUMN NAMES WITH DB ----------------
df.rename(columns={
    "last_updated_date": "last_updated_date",
    "nasscom_status": "nasscom_status",
    "nasscom_member_status": "nasscom_member_status",
    "account_global_legal_name": "account_global_legal_name",
    "about_company": "about_company",
    "hq_address": "hq_address",
    "hq_city": "hq_city",
    "hq_state": "hq_state",
    "hq_zip_code": "hq_zip_code",
    "hq_country": "hq_country",
    "hq_region": "hq_region",
    "hq_broad_line": "hq_broad_line",
    "hq_website": "hq_website",
    "hq_offerings": "hq_offerings",
    "source_link_hq_offering": "source_link_hq_offering",
    "hq_sub_industry": "hq_sub_industry",
    "hq_industry": "hq_industry",
    "primary_category": "primary_category",
    "primary_nature": "primary_nature",
    "hq_forbes_rank_2023": "hq_forbes_rank_2023",
    "hq_forture_rank_2023": "hq_forture_rank_2023",
    "hq_company_type": "hq_company_type",
    "hq_revenue_in_usd_mil": "hq_revenue_in_usd_mil",
    "hq_revenue_range": "hq_revenue_range",
    "hq_fy_end": "hq_fy_end",
    "hq_revenue_year": "hq_revenue_year",
    "source_type_hq_revenue": "source_type_hq_revenue",
    "source_link_hq_revenue": "source_link_hq_revenue",
    "hq_employee_count": "hq_employee_count",
    "hq_employee_range": "hq_employee_range",
    "source_type_hq_employee": "source_type_hq_employee",
    "source_link_hq_employee": "source_link_hq_employee",
    "comments_cd": "comments_cd",
    "data_year": "data_year",
    "entry_year_of_gcc": "entry_year_of_gcc"
}, inplace=True)

# ---------------- STEP 5: DROP ID COLUMN IF PRESENT ----------------
# (Handled automatically by BIGSERIAL in DB)
df.drop(columns=["id"], errors="ignore", inplace=True)

# ---------------- STEP 6: POSTGRES CONNECTION ----------------
conn_string = (
    "Enter your DB URL"
)

engine = create_engine(conn_string)

# ---------------- STEP 7: TRUNCATE TABLE ----------------
with engine.begin() as conn:
    conn.execute(text("TRUNCATE TABLE public.br_data"))

# ---------------- STEP 8: INSERT DATA ----------------
df.to_sql(
    "br_data",
    engine,
    if_exists="append",
    index=False,
    method="multi"
)

print("✅ Database table 'br_data' successfully refreshed from Google Sheet.")
