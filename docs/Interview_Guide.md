# Aarohan FMCG Analytics — Interview Preparation

> Use this as an independently developed portfolio case study with synthetic data. Explain only the stages you personally ran and can reproduce. The native Power BI report and MySQL outputs still require your own desktop verification.

## 60-second project introduction

“I built an FMCG sales and profitability analytics portfolio project for a fictional company called Aarohan Consumer Products. The goal was to show how I would convert transactional order-line data into business-ready insights while keeping the numbers trustworthy. I used Python and Pandas for data-quality checks, deduplication and calculations; wrote MySQL 8 scripts for a relational fact-and-dimension workflow and business questions; prepared an Excel workbook for KPI review and formula practice; and designed a Power BI implementation with a star schema, DAX measures and a four-page report plan. The synthetic source contains 30,060 rows, with 60 exact duplicates, leaving 30,000 clean lines and 18,000 distinct orders. I documented sales, discount, return and estimated-profit definitions, then created reconciliation outputs and a manual QA checklist. The main limitation is that all data is synthetic and profit is estimated, not audited company finance.”

## 2–3 minute end-to-end explanation

1. **Business objective:** make it easier for fictional FMCG management to assess sales, product profitability, discounting, returns and regional/channel distribution.
2. **Data grain:** a record represents an order line; one order may contain several line items. This determines why distinct orders must use `COUNT(DISTINCT order_id)`.
3. **Data quality:** inspect required fields, key uniqueness, quantity, price, discount and return-unit bounds; preserve the raw source and remove exact duplicates only from the analysis copy.
4. **Metric logic:** compute gross sales, discount value, net sales before returns, estimated return value, net sales after returns, estimated COGS, estimated profit and weighted margin. Document assumptions because real return accounting may differ.
5. **Tools:** Python creates repeatable cleaned data and summary outputs; SQL queries business questions across facts/dimensions; Excel helps inspect formulas and summary metrics; Power BI model and DAX assets outline the interactive reporting experience.
6. **Validation:** the Python run reports 24 passing checks and makes outputs available for comparison. SQL and Power BI must be executed locally and reconciled before I claim those tools' results are fully validated.
7. **Limitations:** data is fictional, currency unspecified, profit is estimated, and the provided dashboard previews are static visual references rather than an interactive PBIX.

## Five useful observations (synthetic data)

1. **KPI baseline:** net sales after estimated returns = 41,546,999.57; estimated profit = 12,257,592.57; weighted estimated margin = 29.50%.
2. **Year comparison:** estimated net sales were 20,990,320.77 in 2024 and 20,556,678.80 in 2025 (approximately -2.07% change).
3. **Regional leader:** North has the largest estimated net sales at 15,015,139.21; this absolute result says nothing by itself about efficiency per outlet.
4. **Product economics:** Premium Tea 500g has the highest estimated profit (1,360,563.85); Salted Chips 50g is lowest (169,224.01), but it is still profitable under these assumptions.
5. **Discount comparison:** observed margin is lower in the 20%+ band than in the 0–4.9% band, but product/customer/channel mix may explain some or all of the difference; it is not proof of causation.

## Five recommendations and rationale

1. Reconcile return, COGS, freight, tax and currency definitions with Finance before real-world use.
2. Analyse returns by reason × SKU × distributor × channel × month to locate a pattern worth investigating.
3. Review high-sales/lower-margin product economics using realised prices, unit cost, discounts, returns and product/channel mix.
4. Test promotions with comparable cohorts or controlled holdouts rather than inferring causality from descriptive discount bands.
5. Investigate the year-over-year movement by same month, units, order count, AOV, assortment and distribution coverage.

## Questions an interviewer may ask

### Data and KPIs
**Q: Why did you deduplicate?** Exact duplicate source lines can double-count sales and profit. I removed exact row duplicates only in the analysis copy and kept the raw file for traceability. I also validated uniqueness of the line ID.

**Q: Why is the grain important?** Line-level totals can be summed across line items, but order count must use distinct order IDs. Otherwise multi-line orders inflate order count.

**Q: How do you define margin?** Sum of estimated profit divided by sum of estimated net sales for the selected filter context. I do not average each line's margin percentage.

**Q: Why is profit “estimated”?** The synthetic source does not define currency or full accounting treatment. The model assumes returned units reverse the discounted selling value and returned units are removed from estimated COGS. Actual finance policies may differ.

**Q: Does the dataset show loss-making products?** No; even the lowest estimated-profit products are positive under the documented rules. Do not manufacture a loss-making SKU finding.

### SQL
**Q: `WHERE` vs `HAVING`?** `WHERE` filters input rows before grouping; `HAVING` filters groups after aggregation.

**Q: Why a CTE?** It gives a complex calculation a named intermediate result so its logic is easier to review, reuse and debug.

**Q: What does `ROW_NUMBER()` do here?** It numbers rows within a partition of identical business fields; retaining `duplicate_rank = 1` keeps one copy of each identical source record.

**Q: Why `NULLIF`?** Dividing by `NULLIF(total_sales, 0)` returns NULL instead of raising a divide-by-zero error when total sales is zero.

**Q: Why use `LAG()`?** To compare the current time period with the previous ordered period for a year/month growth calculation.

### Python and Excel
**Q: Why Pandas?** It makes data loading, data-quality checks, joins, type conversion, grouping and export repeatable instead of relying on a series of manual steps.

**Q: Why use `validate='many_to_one'` in joins?** It detects duplicated dimension keys that would otherwise duplicate fact rows and inflate totals.

**Q: Why XLOOKUP/INDEX-MATCH?** To find a dimension attribute (such as product unit cost) from an ID and help validate reference data.

**Q: How did you validate formula totals?** I generated independent summary outputs and designed reconciliation checks. In Excel Desktop, recheck the workbook formula engine; in SQL and Power BI, run the scripts/report locally and record the comparison.

### Power BI and DAX
**Q: Why a star schema?** Dimensions filter a central fact table, making model relationships easier to understand and reducing ambiguous filtering.

**Q: What is filter context?** The selection of rows affecting a measure through slicers, visual fields, page/report filters and relationships.

**Q: Why use a date table?** It provides a continuous calendar with consistent year/month attributes and supports time intelligence such as prior-year comparisons.

**Q: Why is `DIVIDE()` useful?** It makes ratio measures safer where the denominator may be zero and supports an optional alternate result.

**Q: What was actually completed in Power BI?** The source DAX, theme, data model, page design, and static previews are supplied. The native PBIX has not been created or interactively validated in this environment; I would only say I built the report after completing and checking it in Desktop.

## Limitations and next improvements

- Replace synthetic source data with a properly licensed real dataset or approved anonymised company data.
- Confirm currency and return/COGS policies with Finance; if necessary, separately model damaged goods, restocking, freight and tax.
- Add stock-out, delivery lead time, inventory on hand and promotion exposure for supply chain and causal analysis.
- Run MySQL script outputs and Power BI measures on the user's machine and document exact parity before marking cross-tool validation complete.
- Save/reopen a PBIX and capture actual Power BI screenshots only after local validation.

## Practice before the interview

Can you explain the data grain without looking at notes? Can you write a grouped profit query from memory? Can you explain why a product with high sales may have low margin? Can you point at every number in the dashboard and trace it to a field and formula? Can you state which parts are finished and which were not yet verified? If not, practise the project again before presenting it as your own work.
