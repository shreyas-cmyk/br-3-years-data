CREATE TABLE
  public.br_data (
    id bigserial NOT NULL,
    last_updated_date text NULL,
    nasscom_status text NULL,
    nasscom_member_status text NULL,
    account_global_legal_name text NULL,
    about_company text NULL,
    hq_address text NULL,
    hq_city text NULL,
    hq_state text NULL,
    hq_zip_code text NULL,
    hq_country text NULL,
    hq_region text NULL,
    hq_broad_line text NULL,
    hq_website text NULL,
    hq_offerings text NULL,
    source_link_hq_offering text NULL,
    hq_sub_industry text NULL,
    hq_industry text NULL,
    primary_category text NULL,
    primary_nature text NULL,
    hq_forbes_rank_2023 text NULL,
    hq_forture_rank_2023 text NULL,
    hq_company_type text NULL,
    hq_revenue_in_usd_mil text NULL,
    hq_revenue_range text NULL,
    hq_fy_end text NULL,
    hq_revenue_year text NULL,
    source_type_hq_revenue text NULL,
    source_link_hq_revenue text NULL,
    hq_employee_count text NULL,
    hq_employee_range text NULL,
    source_type_hq_employee text NULL,
    source_link_hq_employee text NULL,
    comments_cd text NULL,
    data_year text NULL,
    entry_year_of_gcc text NULL
  );

ALTER TABLE
  public.br_data
ADD
  CONSTRAINT br_data_pkey PRIMARY KEY (id)
