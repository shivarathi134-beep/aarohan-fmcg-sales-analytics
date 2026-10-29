# Validation Status and Test Evidence

## Run evidence in this packaged workspace

`python python/aarohan_analysis.py` was executed on the included synthetic source data and regenerated the output CSVs. It reports **24 PASS, 0 REVIEW, 0 FAIL**. The tests include expected raw-row count, exact duplicate count, clean-row count, unique order-line key, required-field null checks, positive quantity/price checks, discount range, return-unit constraints, and dimension/key checks.

| Validation | Observed | Expected / rule | Status |
|---|---:|---|---|
| Raw transaction rows | 30,060 | 30,060 synthetic baseline | PASS |
| Exact duplicate rows | 60 | 60 synthetic baseline | PASS |
| Clean transaction lines | 30,000 | Raw minus duplicates | PASS |
| Unique order-line IDs | 30,000 | Equal to clean rows | PASS |
| Distinct orders | 18,000 | Distinct `order_id` | PASS |
| Estimated net sales after returns | 41,546,999.57 | Recomputed from documented formulas | PASS in Python |
| Estimated profit | 12,257,592.57 | Estimated net sales − estimated COGS | PASS in Python |
| Weighted estimated margin | 29.50% | Estimated profit ÷ estimated net sales | PASS in Python |
| Unit-return rate | 3.15% | Returned units ÷ ordered units | PASS in Python |

Full results: `outputs/validation_checks.csv`, `outputs/data_quality_checks.csv`, `outputs/python_run_log.txt`, `outputs/kpi_summary.json`.

## Tool-by-tool status

| Component | Status | Evidence / remaining work |
|---|---|---|
| Synthetic source data and dictionary | Completed | All source inputs included; synthetic origin and assumptions disclosed. |
| Python pipeline | Completed for this environment | Executed; 24/24 built-in validation checks passed. Run again locally to reproduce. |
| Output summaries and charts | Completed as generated assets | CSV summaries and static Matplotlib dashboard preview files regenerated from Python outputs. |
| Excel workbook | Structurally checked; formula recalc needs desktop check | `.xlsx` package integrity passed; 20 worksheets and 1,197 formula cells are present. Open in desktop Excel, allow formula calculation, verify `Executive_Dashboard` against `outputs/executive_summary.csv`. |
| MySQL scripts | Requires manual execution | Scripted for MySQL 8.0; no claim that Workbench executed it. Import CSVs, build fact/view, run checks and compare to Python outputs. |
| Cross-tool KPI validation | Partially completed | Python results are internally checked; SQL and Power BI totals cannot be marked passed until user executes and reconciles those tools. |
| Power BI model/DAX/theme | Assets created; manual verification required | Import data, check relationships and DAX parsing/results in Power BI Desktop. |
| Native `.pbix` | Not included / requires manual build | No fabricated PBIX. Save and reopen after completing the dashboard guide and QA. |
| Static dashboard previews | Completed | Illustrative PNGs generated from synthetic summaries; not Power BI screenshots or interactive reports. |
| GitHub publication | Not performed | Local ZIP prepared; user should create repository and push using the included commands. |

## Formula definitions that matter for reconciliation

- Gross sales = quantity × unit price.
- Discount amount = gross sales × discount percentage.
- Net sales before returns = gross sales − discount amount.
- Estimated return value = returned units × unit price × (1 − discount percentage).
- Estimated net sales = net sales before returns − estimated return value.
- Estimated COGS = (quantity − returned units) × product unit cost.
- Estimated profit = estimated net sales − estimated COGS.
- Weighted estimated margin = sum estimated profit ÷ sum estimated net sales.
- Unit return rate = sum returned units ÷ sum ordered units.

## Limitations

- All data is synthetic and there is no specified currency, so values are labelled “currency units.”
- The profit/return logic is an explicit modeling assumption, not actual accounting data.
- The MySQL workflow and Power BI Desktop report must be executed locally before marking them completed.
