CREATE TABLE
  public.centers (
    id bigserial NOT NULL,
    last_updated_date text NULL,
    account_global_legal_name text NULL,
    industry text NULL,
    cn_unique_key text NULL,
    status_cd text NULL,
    inc_year_cd text NULL,
    announced_year text NULL,
    month text NULL,
    inc_year_notes text NULL,
    updated_inc_year_link text NULL,
    time_line text NULL,
    end_year_cd text NULL,
    center_legal_name_cd text NULL,
    business_segment_cd text NULL,
    business_sub_segment_cd text NULL,
    center_management_partner text NULL,
    jv_status_cd text NULL,
    jv_name_cd text NULL,
    center_type_cd text NULL,
    center_type_tagging text NULL,
    center_foucs_cd text NULL,
    center_souce_link text NULL,
    center_website_cd text NULL,
    center_linkedin_page_cd text NULL,
    address_cd text NULL,
    city_cd text NULL,
    state_cd text NULL,
    zip_code_cd text NULL,
    country_cd text NULL,
    region_cd text NULL,
    broadline_number_cd text NULL,
    employee_count_cd text NULL,
    employees_range_cd text NULL,
    employee_source_link_cd text NULL,
    comments_cd text NULL,
    data_year text NULL
  );

ALTER TABLE
  public.centers
ADD
  CONSTRAINT centers_pkey PRIMARY KEY (id)
