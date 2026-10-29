# MySQL 8.0+ SQL Workflow

Target engine: **MySQL 8.0+**. MySQL Workbench is the client; a running MySQL Server is also required.

1. Run `00_create_schema.sql` — creates the schema and staging/dimension tables. It drops/recreates these tables; do not rerun after import unless you intend to clear the data.
2. Use Workbench's Table Data Import Wizard to import the seven `data/*.csv` files into tables with the same base names (`orders_raw`, `dim_products`, `dim_geography`, `dim_channels`, `dim_customers`, `dim_distributors`, `dim_date`).
3. Run `01_build_clean_fact_and_view.sql` — creates `fact_sales_clean` by removing exact duplicates while preserving `orders_raw`; creates `v_sales_enriched` with metric definitions.
4. Run `02_data_quality_checks.sql` — inspect row counts, duplicate records, invalid values and dimension key matches.
5. Run one `Q##` block at a time from `03_business_analysis.sql` — 20 business questions using grouping, joins, CTEs, CASE, subqueries, `ROW_NUMBER`, `RANK`, `DENSE_RANK` and `LAG`.

See `docs/SQL_Query_Companion.md` for the business question, expected output schema, the equivalent Python-derived baseline when available, and its execution boundary. This environment did not execute the scripts in a configured MySQL server. **Run and reconcile them locally before claiming MySQL execution in an interview.**
