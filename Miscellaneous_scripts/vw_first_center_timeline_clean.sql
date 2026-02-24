CREATE OR REPLACE VIEW
  "public"."vw_first_center_timeline_clean" AS
WITH
  base AS (
    SELECT
      centers.account_global_legal_name,
      centers.center_type_cd,
      centers.status_cd,
      centers.inc_year_cd,
      CASE
        WHEN centers.inc_year_cd ~ '^\d{4}$'::text THEN centers.inc_year_cd::integer
        ELSE NULL::integer
      END AS inc_year_int
    FROM
      centers
  ),
  gcc_first AS (
    SELECT
      base.account_global_legal_name,
      min(base.inc_year_int) AS first_gcc_year
    FROM
      base
    WHERE
      (
        upper(
          TRIM(
            BOTH
            FROM
              base.center_type_cd
          )
        ) = ANY (
          ARRAY[
            'GCC'::text,
            'GIC'::text,
            'GCC/GIC'::text,
            'SSC'::text,
            'COE'::text,
            'GBS'::text,
            'R&D'::text,
            'ENGINEERING & DESIGN'::text,
            'IT'::text,
            'ENGINEERING'::text
          ]
        )
      )
      AND base.inc_year_int IS NOT NULL
      AND base.status_cd <> 'Upcoming'::text
    GROUP BY
      base.account_global_legal_name
  ),
  non_gcc_first AS (
    SELECT
      base.account_global_legal_name,
      min(base.inc_year_int) AS first_non_gcc_year
    FROM
      base
    WHERE
      base.inc_year_int IS NOT NULL
      AND base.status_cd <> 'Upcoming'::text
    GROUP BY
      base.account_global_legal_name
  ),
  final_base AS (
    SELECT
      b.account_global_legal_name,
      b.center_type_cd,
      b.status_cd,
      b.inc_year_cd,
      COALESCE(g.first_gcc_year, n.first_non_gcc_year) AS first_center_timeline_int
    FROM
      base b
      LEFT JOIN gcc_first g ON b.account_global_legal_name = g.account_global_legal_name
      LEFT JOIN non_gcc_first n ON b.account_global_legal_name = n.account_global_legal_name
  )
SELECT
  account_global_legal_name,
  inc_year_cd AS incorporation_year,
  center_type_cd,
  status_cd,
  COALESCE(first_center_timeline_int::text, 'Upcoming'::text) AS first_center_timeline,
  CASE
    WHEN account_global_legal_name = 'HubSpot, Inc.'::text
    AND status_cd = 'Upcoming'::text
    AND inc_year_cd = '2024'::text THEN 'Upcoming'::text
    WHEN account_global_legal_name = 'Anthropic PBC'::text
    AND status_cd = 'Upcoming'::text
    AND inc_year_cd = '2026'::text THEN 'Upcoming'::text
    WHEN first_center_timeline_int IS NULL THEN 'Upcoming'::text
    WHEN first_center_timeline_int <= 2023 THEN '2023'::text
    WHEN first_center_timeline_int = 2024 THEN '2024'::text
    WHEN first_center_timeline_int = 2025 THEN '2025'::text
    ELSE 'Upcoming'::text
  END AS entry_year_of_gcc_type_center
FROM
  final_base;
