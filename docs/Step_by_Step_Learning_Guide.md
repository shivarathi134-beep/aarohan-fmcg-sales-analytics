# Step-by-Step Learning & Execution Guide

This guide assumes Windows and a beginner-to-junior analyst skill level. Read each phase, run it, verify it, then practise explaining it in your own words.

## Software and licence notes

- **Python:** Python 3.10+ and pip. Install libraries from `requirements.txt` inside a virtual environment.
- **MySQL:** a running MySQL Server 8.0+ instance is required; Workbench is the graphical client, not the database server. Install a Workbench release compatible with your server. See the [MySQL 8.0 Windows installation guide](https://dev.mysql.com/doc/refman/8.0/en/windows-installation.html) and [Workbench manual](https://dev.mysql.com/doc/workbench/en/). Oracle has introduced a newer Workbench version series, so check current client/server compatibility if you are installing from scratch.
- **Excel:** a desktop version that can open `.xlsx` and supports formula recalculation is recommended. The workbook includes `XLOOKUP`; an `INDEX/MATCH` alternative is described for older Excel versions.
- **Power BI:** [Power BI Desktop is free for local report authoring](https://learn.microsoft.com/en-us/power-bi/fundamentals/desktop-get-the-desktop). Online publishing/sharing rights depend on the tenant/capacity and can require Power BI Pro or Premium Per User; see [Microsoft's current licence feature matrix](https://learn.microsoft.com/en-us/power-bi/fundamentals/service-features-license-type). You do not need to publish online to build and save a local `.pbix` file for an interview.
- **Git:** optional until you publish to GitHub. No repository is created remotely by this project package.

## Stage 1 — Understand the business question
**Do:** Read `README.md`, `docs/Data_Dictionary.md`, and `docs/Findings_and_Caveats.md`. Open `data/orders_raw.csv` and the dimension CSVs.

**Why:** Before using tools, establish the row grain, keys, metric definitions, and source limitations.

**Expected:** You should be able to say that the transaction file has one product-line record per row, while an order can contain multiple lines; the source company and records are synthetic.

**Verify:** Reconcile dimensions and field names with `docs/Data_Dictionary.md`.

**Interview explanation:** “I started by defining the grain and business rules so order counts and profitability weren’t calculated at the wrong level.”

## Stage 2 — Run Python
1. Install Python 3.10+ from the official Python distribution, or use an existing compatible installation.
2. Extract the project ZIP and open the project directory in VS Code or Terminal.
3. Windows PowerShell commands:

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python python/aarohan_analysis.py
python python/make_dashboard_preview.py
```

If PowerShell activation is blocked by company policy, use Command Prompt and `.venv\Scripts\activate.bat`; do not change managed-device security settings without permission.

**Why:** Python creates a repeatable cleaning/analysis pipeline and outputs used by the other tools.

**Expected:** `outputs/` is refreshed, including clean fact CSV, KPI, monthly, product, region, channel, category, customer-segment, discount-band and return-reason summaries. The script prints validation results.

**Verify:** Look for `Validation checks: 24 PASS, 0 REVIEW, 0 FAIL`; inspect `outputs/kpi_summary.json` and `outputs/validation_checks.csv`.

**Interview explanation:** “I preserved the raw file, removed exact duplicate records only in the analytical copy, validated keys and business rules, then produced summaries from a reproducible Pandas pipeline.”

## Stage 3 — Study Excel
**Do:** Open `excel/Aarohan_Excel_Analytics.xlsx`. Start at `Start_Here`, then examine `Data_Quality`, `KPI_Source`, the summary sheets, `Formula_Practice`, and `Executive_Dashboard`.

**Why:** Excel is useful for quick review, lookup checks, conditional calculations and stakeholder-friendly summaries.

**Expected:** Formula examples and dashboard KPIs that trace to the full-run Python summaries.

**Verify:** Compare the workbook KPI values with `outputs/executive_summary.csv`. Recalculate in desktop Excel; this environment cannot verify your local Excel formula engine or your version's function compatibility.

**Practice:** Explain XLOOKUP/INDEX-MATCH, SUMIFS, COUNTIFS, IFERROR and why weighted profit margin must be calculated from totals.

**Important:** `Raw_Sample_500` and `Analysis_Sample` are samples. Do not use those tabs to calculate the all-record totals; all complete records are in the CSV files.

## Stage 4 — Execute SQL in MySQL Workbench
1. Install MySQL Server 8.0 and MySQL Workbench if you do not already have them. MySQL Workbench alone is a client; it needs access to a running MySQL server.
2. Open Workbench and connect to the server.
3. Run `sql/00_create_schema.sql`.
4. Use **Table Data Import Wizard** to import these seven CSVs into matching names: `orders_raw.csv`, `dim_products.csv`, `dim_geography.csv`, `dim_channels.csv`, `dim_customers.csv`, `dim_distributors.csv`, `dim_date.csv`. If Workbench's wizard auto-selects datatypes poorly, confirm dates and DECIMAL fields before loading.
5. Run `sql/01_build_clean_fact_and_view.sql`.
6. Run `sql/02_data_quality_checks.sql`.
7. Run `sql/03_business_analysis.sql` one `Q##` section at a time.

**Why:** SQL demonstrates querying relational data, joining dimensions, aggregation, CTEs, CASE expressions, subqueries and window functions.

**Expected:** `fact_sales_clean` contains 30,000 rows; `v_sales_enriched` combines sales rows with the descriptive dimensions.

**Verify:** Compare Q01 totals with `outputs/executive_summary.csv`; compare year/category/product/region/channel/discount/return reason output to the corresponding CSV summaries. Record mismatches before editing anything. Do not assume script execution succeeds until you execute it.

**Interview explanation:** “I kept the raw staging table intact, used a window function to remove duplicate source rows in a clean fact, then centralised metric definitions in a view so business queries used the same calculations.”

## Stage 5 — Build Power BI Desktop report
1. Open Power BI Desktop (desktop application required for creating/saving `.pbix`).
2. Import `outputs/fact_orders_clean.csv` and six dimension CSVs per `powerbi/PowerBI_build_guide.md`.
3. Set types, rename tables exactly as specified, and create the six one-to-many relationships.
4. Mark `DimDate` as date table and sort month fields.
5. Create measures from `powerbi/DAX_Measures.dax`, one measure at a time; fix any syntax/type warnings in Desktop.
6. Import `powerbi/theme.json` from View → Themes → Browse for themes.
7. Build four pages using the layout guide. Add slicers, page navigation, reset bookmark, tooltip and product drill-through.
8. Complete every relevant row in `powerbi/POWER_BI_MANUAL_QA.md`, save as `Aarohan_Consumer_Products_Analytics.pbix`, close and reopen to verify.

**Why:** Power BI shows your ability to model data, create measures and communicate results interactively.

**Expected:** A native interactive report that reproduces the Python totals and filters correctly.

**Verify:** KPI reconciliation, slicer/cross-filter behavior, date sort, tooltips, navigation, drill-through, bookmark, save/reopen. Static PNGs are design references only.

**Interview explanation:** “I created a star-schema model with a dedicated date table, defined explicit DAX measures, and reconciled core cards to independent Python summaries before validating interactions.” Only use that past-tense wording after doing the work yourself.

## Stage 6 — Prepare GitHub
1. Read `docs/CV_LinkedIn_Package.md` and only use CV claims for tools you have personally run and can explain.
2. Install Git and configure your Git identity on your own machine.
3. From the project root:

```bash
git init
git add .
git commit -m "Add Aarohan FMCG analytics portfolio project"
git branch -M main
```

Create an empty GitHub repository, then replace the placeholder username in:

```bash
git remote add origin https://github.com/YOUR_USERNAME/aarohan-fmcg-sales-analytics.git
git push -u origin main
```

Do not push passwords, personal credentials, client data or employer data. Do not claim that the project has been published until you have pushed it and verified the repository page.

## Common troubleshooting

- `python` not found: install Python and enable PATH, then reopen Terminal.
- Package import error: activate `.venv`, rerun `python -m pip install -r requirements.txt`.
- PowerShell blocks activation: use Command Prompt activation, subject to organization policy.
- MySQL import fails on dates/decimals: inspect column mapping and charset in the import wizard; use MySQL Server 8.0+.
- Duplicate key error on `fact_sales_clean`: first verify source deduplication and `order_line_id`; do not simply drop the primary key.
- Power BI totals multiply: check one-to-many relationships, duplicate dimension IDs, bidirectional filters, and whether the same dimension was loaded twice.
- Time intelligence is blank/wrong: confirm contiguous date dimension, date type, marked date table, active order-date relationship and current filter period.
- XLOOKUP unavailable: use the included INDEX/MATCH pattern in Formula_Practice.
- Money values: do not add an INR symbol because the source has no currency specification.
