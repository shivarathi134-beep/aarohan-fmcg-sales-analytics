# Execution Checklist — Current Project Status

## Completed in the packaged workspace
- [x] Read and profiled the seven synthetic source CSVs.
- [x] Preserve raw source data while deduplicating exact duplicate rows in the analytical copy.
- [x] Execute Python cleaning, calculations, summaries and validation checks.
- [x] Generate product, category, monthly, yearly, region/state, channel, distributor, customer-segment, discount-band and return-reason outputs.
- [x] Create an Excel workbook with formulas, lookup examples, summary sheets and an executive dashboard sheet.
- [x] Author MySQL 8 schema, clean fact/view, quality checks and 20 business analysis queries.
- [x] Create Power BI DAX measures, theme JSON, Power Query helper, data model/build guide, QA checklist, and two static design preview images.
- [x] Document assumptions, synthetic data provenance limitations, interpretation, interviews, CV/LinkedIn and GitHub publishing.

## Requires manual verification by the project owner
- [ ] Open/recalculate the Excel workbook in desktop Excel and compare dashboard KPIs to `outputs/executive_summary.csv`.
- [ ] Install/connect to MySQL Server 8.0+ and execute all SQL scripts in the documented order.
- [ ] Reconcile MySQL outputs to Python output CSVs and document any difference.
- [ ] Build the four-page report in Power BI Desktop and save a native `.pbix`.
- [ ] Validate DAX results, active one-to-many relationships, date sorting, slicers, cross-filtering, reset bookmark, page navigation, tooltip and product drill-through.
- [ ] Save, close, reopen the `.pbix`, then capture actual Power BI screenshots.
- [ ] Push to GitHub manually; a remote repository has not been created or pushed by this project package.
- [ ] Practise explaining the row grain, deduplication, formulas, SQL logic, visual choices and caveats in your own words.
