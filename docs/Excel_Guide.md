# Excel Analytics Workbook Guide

Workbook: `excel/Aarohan_Excel_Analytics.xlsx`.

## What is included

- `Start_Here`: workbook scope and how to use it.
- `Raw_Sample_500`: a readable 500-row sample from the raw input for data-quality exercises (not the entire 30,060-row source).
- `Analysis_Sample`: 1,000 illustrative cleaned detail rows from the full analytical output.
- Dimension sheets: product, customer, geography, channel, distributor, and date reference data.
- `KPI_Source`: key metrics calculated by the full Python pipeline from all 30,000 clean rows.
- Summary sheets: product, category, region, month, discount, returns, customer segments.
- `Data_Quality`: key validation counts and checks.
- `Formula_Practice`: formulas and lookup examples on a smaller sample to learn Excel functions.
- `Executive_Dashboard`: formula-linked executive KPIs and charts based on full-run summary figures.

**Important:** the raw and detail worksheet tabs are intentionally sampled to keep Excel file size and usability manageable. Full data files remain available in `data/` and `outputs/`. Do not calculate overall totals from the 500-/1,000-row sample and compare them to full-dataset KPIs.

## Suggested learning sequence

1. Open `Start_Here` and inspect field definitions.
2. Check `Raw_Sample_500` for exact duplicated order-line rows, missing required fields, dates and discount bounds.
3. Compare raw vs cleaned row counts: 30,060 raw, 60 exact duplicate rows, 30,000 clean lines.
4. Open `Formula_Practice`: follow the XLOOKUP / INDEX-MATCH examples, `IFERROR`, `SUMIFS`, `COUNTIFS`, `YEAR`, `TEXT`, and contribution/growth formulas. The exact displayed formula may depend on your Excel locale/semicolon settings.
5. Open the summary worksheets and trace each total back to `KPI_Source`/Python outputs.
6. Open `Executive_Dashboard` and check the values against `outputs/executive_summary.csv`.

## Recreate an all-row PivotTable

1. Open `outputs/analysis_detail.csv` in Excel via **Data → From Text/CSV** (or open it directly if Excel handles the size well).
2. Ensure date and numeric columns are typed correctly.
3. Load it to a worksheet or the Data Model; select the imported table and choose **Insert → PivotTable**.
4. Put `category` or `region_name` in Rows, `net_sales_after_returns_est` and `profit_est` in Values, and `order_date` in Filters or a timeline.
5. For margin, use total estimated profit divided by total estimated net sales. Do not average row-level margin percentages.
6. Add slicers for category, region, channel or year and confirm the numbers match Python summary CSVs.

## Formulas you should be able to explain

- `XLOOKUP`: looks up product unit cost/name using a product ID.
- `INDEX/MATCH`: older, flexible alternative lookup pattern.
- `SUMIFS`: sums profit or sales after applying multiple conditions.
- `COUNTIFS`: counts return lines or duplicate flags under selected criteria.
- `IFERROR`: supplies an intentional fallback when a lookup or division returns an error.
- `YEAR` / `TEXT`: derive year and year-month labels from dates.
- Profit margin: total profit ÷ total net sales; it is a weighted ratio when calculated on totals.

## Verification note

The workbook was generated and formula cells were included with `artifact_tool`. A full formula recalculation in desktop Microsoft Excel still needs to be confirmed on your computer. Excel versions without `XLOOKUP` can use the provided `INDEX/MATCH` alternative.
