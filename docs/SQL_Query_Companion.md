# SQL Query Companion — MySQL 8.0+

**Execution status:** the SQL scripts were authored for MySQL 8.0 and reviewed against the current data model, but the MySQL server/Workbench execution itself has **not** been performed in this environment. The figures shown below are equivalent calculations from the executed Python pipeline, not claimed MySQL outputs. Execute the SQL in MySQL Workbench and record/resolve any discrepancy before describing SQL as tested.

## Run order

1. `sql/00_create_schema.sql` — creates schema and seven input tables.
2. Import seven matching CSVs from `data/` using MySQL Workbench Table Data Import Wizard. Dimension tables and `orders_raw` names must match exactly.
3. `sql/01_build_clean_fact_and_view.sql` — removes exact duplicates into `fact_sales_clean` while retaining raw; creates `v_sales_enriched`.
4. `sql/02_data_quality_checks.sql` — run each check and review results.
5. `sql/03_business_analysis.sql` (or `sql/aarohan_analysis_mysql8.sql`) — run each `Q##` query section separately.

## Query catalogue

### Q01 — What is the overall commercial baseline?
- **Expected output:** One-row KPI result: distinct orders, sales/discount/return/profit amounts, margin, unit return rate.
- **Reference output:** `outputs/executive_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q02 — How do net sales and profit change year over year?
- **Expected output:** One row per order year with net sales, estimated profit, margin, and previous-year change using LAG().
- **Reference output:** `outputs/yearly_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q03 — What does the monthly trend look like?
- **Expected output:** One row per year-month with sales, profit, margin and units.
- **Reference output:** `outputs/monthly_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q04 — Which products contribute most and least to estimated profit?
- **Expected output:** One row per SKU including sales, profit, margin and RANK().
- **Reference output:** `outputs/product_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q05 — Which categories contribute most to sales and profit?
- **Expected output:** One row per category with sales/profit contribution and estimated margin.
- **Reference output:** `outputs/category_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q06 — Which states and regions perform best?
- **Expected output:** One row per region-state with sales, profit, margin and unit-return rate.
- **Reference output:** `outputs/state_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q07 — How do sales and profit compare by channel?
- **Expected output:** One row per channel with distinct orders, sales, profit, margin and unit-return rate.
- **Reference output:** `outputs/channel_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q08 — Which customer segments generate sales/profit?
- **Expected output:** One row per customer segment and customer type with distinct counts and totals.
- **Reference output:** `outputs/customer_segment_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q09 — Who are the top 20 customers by net sales?
- **Expected output:** Top-20 customer result, ordered by estimated net sales.
- **Reference output:** `outputs/top_25_customers.csv (top 20 subset)`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q10 — Which distributors have high sales but weaker margins?
- **Expected output:** One row per distributor with sales/profit/margin/return-rate.
- **Reference output:** `outputs/distributor_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q11 — How do observed margin levels differ across discount bands?
- **Expected output:** One row per discount band with sales, discounts, profit and margin.
- **Reference output:** `outputs/discount_band_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q12 — Which return reasons have the highest estimated value?
- **Expected output:** One row per return reason with return lines, units and estimated value.
- **Reference output:** `outputs/return_reason_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q13 — Which sales channels have higher unit-return rates?
- **Expected output:** One row per channel with ordered/returned units and rate.
- **Reference output:** `outputs/channel_summary.csv`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q14 — Which high-sales products fall below overall margin?
- **Expected output:** Product rows meeting the query rule: average product sales per order above the overall average but margin below overall.
- **Reference output:** `Derive from outputs/product_summary.csv; execute query to validate the exact filtered list.`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q15 — How many customers are repeat purchasers?
- **Expected output:** Grouped one-row-per-repeat-status result with customer count, average orders and sales.
- **Reference output:** `Requires executing the query in MySQL or recreating customer-order counts in Python.`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q16 — How do products rank within categories?
- **Expected output:** One row per product with DENSE_RANK() over category.
- **Reference output:** `outputs/product_summary.csv (rank by estimated profit can be recreated).`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q17 — What is average order value?
- **Expected output:** One-row result computed from order totals, not averages of order lines.
- **Reference output:** `Estimated AOV = total estimated net sales ÷ 18,000 distinct orders.`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q18 — Which products have the highest unit-return rate?
- **Expected output:** One row per SKU with ordered units, returned units, return rate, estimated return value and margin.
- **Reference output:** `outputs/product_summary.csv does not include the full rate columns in its summary; use outputs/analysis_detail.csv or run query.`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q19 — Which regions have margin below the region-average margin?
- **Expected output:** One row per region with a descriptive review flag based on an explicitly stated rule.
- **Reference output:** `outputs/region_summary.csv; execute query for exact flag.`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

### Q20 — Which distributor-product pairs have the most return value?
- **Expected output:** Top 25 distributor × SKU combinations by estimated return value.
- **Reference output:** `Run query; use return rows from outputs/analysis_detail.csv for an independent recreation.`
- **How to explain it:** start from the business question; identify the row grain and grouping columns; explain any `JOIN`, `GROUP BY`, `HAVING`, `CASE`, CTE, subquery, or window function; then check the result against an independent aggregation.
- **Execution status:** MySQL output requires manual execution in Workbench; do not call the expected output a MySQL-validated result until it has been run.

## Equivalent Python-validated headline results

- Raw rows: 30,060; exact duplicate rows: 60; clean rows: 30,000.
- Distinct orders: 18,000; clean order-line IDs: 30,000.
- Gross sales: 47,450,732.16; discounts: 4,580,888.23; net sales before returns: 42,869,843.93.
- Estimated return value: 1,322,844.36; estimated net sales after returns: 41,546,999.57.
- Estimated COGS after returns: 29,289,407.00; estimated profit: 12,257,592.57; weighted margin: 29.50%.
- Ordered units: 480,584; returned units: 15,132; unit return rate: 3.15%.

### Important interpretation rules

- `COUNT(*)` counts lines; `COUNT(DISTINCT order_id)` counts orders. One order can contain multiple product lines.
- Use `NULLIF(denominator, 0)` or `DIVIDE` to avoid divide-by-zero errors.
- Use weighted margin: `SUM(profit_est) / SUM(net_sales_after_returns_est)`, not the average of line-level margin percentages.
- SQL `ROW_NUMBER()` partitions by all source business fields to keep one copy of exact duplicate rows.
- Discount-band differences are descriptive; they do not prove discount causation.
- All values are synthetic currency units; estimated profit depends on the return/COGS assumptions documented in `docs/Findings_and_Caveats.md`.


## Python-derived baseline snapshots for SQL reconciliation

**These are outputs from the executed Python pipeline, not results returned by MySQL Workbench.** Use them as independent target values when you run each SQL query. Differences may indicate a query, data import, datatype, join, or formula issue and should be investigated. All figures are synthetic, unspecified currency units, and estimated where shown.

### Q02 — Annual trend
| Year | Orders | Estimated net sales | Estimated profit | Margin | Sales growth YoY | Profit growth YoY |
|---|---|---|---|---|---|---|
| 2024 | 9017 | 20,990,320.77 | 6,183,697.77 | 29.46% | — | — |
| 2025 | 8983 | 20,556,678.80 | 6,073,894.80 | 29.55% | -2.07% | -1.78% |

### Q03 — Highest/lowest monthly net-sales observations
| Group | Month | Estimated net sales | Estimated profit |
|---|---|---|---|
| Top | 2024-11 | 2,207,862.92 | 663,550.92 |
| Top 2 | 2025-10 | 2,138,447.50 | 642,019.50 |
| Top 3 | 2025-11 | 2,132,017.03 | 617,569.03 |
| Bottom | 2025-02 | 1,430,664.31 | 419,048.31 |
| Bottom 2 | 2025-01 | 1,503,163.51 | 440,909.51 |
| Bottom 3 | 2024-03 | 1,520,061.25 | 441,571.25 |

### Q04 — Product profitability ranking
| Group | Product | Estimated net sales | Estimated profit | Margin |
|---|---|---|---|---|
| Top | Premium Tea 500g | 4,133,091.85 | 1,360,563.85 | 32.92% |
| Top | Rice 5kg | 6,132,530.99 | 1,085,020.99 | 17.69% |
| Top | Instant Coffee 100g | 2,889,483.41 | 944,853.41 | 32.70% |
| Top | Tissue Pack 6 rolls | 2,520,360.17 | 853,560.17 | 33.87% |
| Top | Wheat Flour 5kg | 4,164,583.08 | 811,111.08 | 19.48% |
| Bottom | Salted Chips 50g | 380,094.01 | 169,224.01 | 44.52% |
| Bottom | Lemon Drink 500ml | 593,682.44 | 221,144.44 | 37.25% |
| Bottom | Cream Biscuits 150g | 654,342.82 | 290,582.82 | 44.41% |
| Bottom | Bath Soap 100g | 755,358.23 | 302,303.23 | 40.02% |
| Bottom | Masala Chips 100g | 769,489.59 | 332,359.59 | 43.19% |
All five bottom-ranked products remain positive estimated-profit products in this synthetic dataset.
### Q05 — Category results
| Category | Estimated net sales | Estimated profit | Profit contribution | Margin |
|---|---|---|---|---|
| Beverages | 10,691,448.20 | 3,582,004.20 | 29.22% | 33.50% |
| Staples | 16,001,287.19 | 3,266,852.19 | 26.65% | 20.42% |
| Home Care | 7,398,620.65 | 2,627,838.65 | 21.44% | 35.52% |
| Personal Care | 4,825,050.28 | 1,643,678.28 | 13.41% | 34.07% |
| Snacks | 2,630,593.25 | 1,137,219.25 | 9.28% | 43.23% |

### Q06 — Regional results
| Region | Estimated net sales | Estimated profit | Margin | Unit return rate |
|---|---|---|---|---|
| North | 15,015,139.21 | 4,428,442.21 | 29.49% | 3.22% |
| South | 10,549,392.47 | 3,152,187.47 | 29.88% | 3.38% |
| West | 9,420,260.36 | 2,737,507.36 | 29.06% | 2.77% |
| East | 6,562,207.53 | 1,939,455.53 | 29.55% | 3.13% |
Top states by estimated net sales:
| State | Region | Estimated net sales | Estimated profit | Margin |
|---|---|---|---|---|
| Maharashtra | West | 5,281,800.05 | 1,542,326.05 | 29.20% |
| Uttar Pradesh | North | 4,822,874.93 | 1,432,151.93 | 29.69% |
| Karnataka | South | 3,561,579.48 | 1,075,681.48 | 30.20% |
| Rajasthan | North | 3,556,115.96 | 1,041,275.96 | 29.28% |
| Gujarat | West | 3,346,675.93 | 978,032.93 | 29.22% |

### Q07 and Q13 — Channel summary
| Channel | Orders | Estimated net sales | Estimated profit | Margin | Unit return rate |
|---|---|---|---|---|---|
| General Trade | 8709 | 19,972,411.75 | 5,958,651.75 | 29.83% | 2.93% |
| Modern Trade | 4004 | 9,559,583.72 | 2,886,443.72 | 30.19% | 3.00% |
| Wholesale | 3526 | 7,903,388.10 | 2,177,958.10 | 27.56% | 3.04% |
| E-Commerce | 1761 | 4,111,616.00 | 1,234,539.00 | 30.03% | 4.72% |

### Q08 — Customer-segment results
| Segment | Customer type | Orders | Estimated net sales | Estimated profit | Margin |
|---|---|---|---|---|---|
| Small Retailer | Business Customer | 7133 | 16,569,992.36 | 4,927,147.36 | 29.74% |
| Large Retailer | Business Customer | 5543 | 12,811,298.74 | 3,743,648.74 | 29.22% |
| Wholesaler | Business Customer | 3696 | 8,517,120.02 | 2,502,832.02 | 29.39% |
| Supermarket | Business Customer | 1628 | 3,648,588.46 | 1,083,964.46 | 29.71% |

### Q09 — Top five customers preview (query returns top 20)
| Customer | Segment | Orders | Estimated net sales | Estimated profit |
|---|---|---|---|---|
| Ishita Saxena Stores 030 | Large Retailer | 27 | 97,405.49 | 28,596.49 |
| Dev Khan Stores 908 | Wholesaler | 28 | 91,407.04 | 26,932.04 |
| Dev Malhotra Stores 671 | Large Retailer | 25 | 86,673.11 | 22,615.11 |
| Vivaan Mehta Stores 287 | Small Retailer | 26 | 85,718.11 | 23,294.11 |
| Ishaan Das Stores 386 | Large Retailer | 26 | 85,023.59 | 22,574.59 |

### Q10 — Top five distributors by net sales (query returns all; investigate margin and return rate)
| Distributor | Tier | Orders | Estimated net sales | Estimated profit | Margin | Unit return rate |
|---|---|---|---|---|---|---|
| Aarohan Distributor 50 | Platinum | 350 | 865,754.42 | 256,380.42 | 29.61% | 2.41% |
| Aarohan Distributor 43 | Silver | 317 | 835,947.08 | 236,925.08 | 28.34% | 2.32% |
| Aarohan Distributor 13 | Platinum | 320 | 804,408.98 | 239,117.98 | 29.73% | 3.55% |
| Aarohan Distributor 49 | Platinum | 324 | 788,454.96 | 234,876.96 | 29.79% | 4.18% |
| Aarohan Distributor 54 | Platinum | 333 | 784,227.51 | 231,589.51 | 29.53% | 3.71% |

### Q11 — Discount-band results

| Discount band | Orders | Gross sales | Discount amount | Estimated net sales | Estimated profit | Margin |
|---|---:|---:|---:|---:|---:|---:|
| 0–4.9% | 6,458 | 11,503,822.41 | 145,611.13 | 10,997,094.74 | 3,872,815.74 | 35.22% |
| 5–9.9% | 6,455 | 11,348,487.67 | 787,387.62 | 10,238,437.96 | 3,241,906.96 | 31.66% |
| 10–19.9% | 10,762 | 20,598,155.20 | 2,754,621.21 | 17,299,790.93 | 4,593,294.93 | 26.55% |
| 20%+ | 2,405 | 4,000,266.88 | 893,268.27 | 3,011,675.94 | 549,574.94 | 18.25% |

Observed band differences are not evidence that discount level caused the margin result.

### Q12 — Return reason results
| Return reason | Lines | Distinct orders | Returned units | Estimated return value |
|---|---|---|---|---|
| Damaged in Transit | 522 | 517 | 4550 | 416,366.40 |
| Wrong Item | 370 | 369 | 3273 | 275,043.92 |
| Quality Issue | 379 | 376 | 3079 | 270,062.35 |
| Expiry / Near Expiry | 307 | 307 | 2554 | 214,265.99 |
| Customer Preference | 233 | 232 | 1676 | 147,105.69 |

### Q14 — Above-average sales-per-product-order but below-overall-margin products
Overall average sales per distinct order is 2,308.17; overall weighted estimated margin is 29.50%.
| Product | Category | Estimated net sales | Orders containing SKU | SKU sales / SKU order | Margin |
|---|---|---|---|---|---|
| Rice 5kg | Staples | 6,132,530.99 | 1521 | 4,031.91 | 17.69% |
| Wheat Flour 5kg | Staples | 4,164,583.08 | 1487 | 2,800.66 | 19.48% |

### Q15 — Repeat purchase summary (independent Python calculation)
| Customer group | Customers | Average orders/customer | Estimated net sales |
|---|---|---|---|
| Repeat customer | 1000 | 18.00 | 41,546,999.57 |

**Observation:** the current source places all 1,000 synthetic customers in the repeat-customer group (at least two distinct orders). There is no one-order customer cohort in this sample, so the dataset cannot compare one-time versus repeat purchasers. This is a synthetic-data limitation, not an insight about a real customer base.

### Q16 — Highest estimated-profit SKU within each category
| Category | Top SKU | Estimated profit |
|---|---|---|
| Beverages | Premium Tea 500g | 1,360,563.85 |
| Home Care | Tissue Pack 6 rolls | 853,560.17 |
| Personal Care | Shampoo 180ml | 762,615.02 |
| Snacks | Sweet Biscuits 200g | 345,052.83 |
| Staples | Rice 5kg | 1,085,020.99 |

### Q17 — Order value
- Distinct orders: 18,000
- Estimated net sales total: 41,546,999.57
- Average order value: 2,308.17
- Average estimated profit per order: 680.98

### Q18 — Five highest unit-return-rate SKUs
| Product | Units ordered | Units returned | Unit return rate | Estimated return value |
|---|---|---|---|---|
| Toothpaste 150g | 24650 | 929 | 3.77% | 67,205.47 |
| Bath Soap 100g | 24762 | 917 | 3.70% | 28,372.39 |
| Salted Chips 50g | 24323 | 893 | 3.67% | 14,557.94 |
| Masala Chips 100g | 25186 | 901 | 3.58% | 28,914.50 |
| Laundry Powder 1kg | 23202 | 824 | 3.55% | 71,019.83 |

### Q19 — Region margin review flag
Unweighted mean of the four region-level margins = 29.50%. The SQL query compares each regional margin with this mean.
| Region | Estimated net sales | Margin | Rule-based flag |
|---|---|---|---|
| North | 15,015,139.21 | 29.49% | Review margin drivers |
| South | 10,549,392.47 | 29.88% | At/above region-average margin |
| West | 9,420,260.36 | 29.06% | Review margin drivers |
| East | 6,562,207.53 | 29.55% | At/above region-average margin |

### Q20 — Top five distributor × product return-value combinations (query returns top 25)
| Distributor | Product | Returned units | Estimated return value |
|---|---|---|---|
| Aarohan Distributor 13 | Rice 5kg | 49 | 13,541.38 |
| Aarohan Distributor 35 | Wheat Flour 5kg | 79 | 12,401.74 |
| Aarohan Distributor 08 | Cooking Oil 1L | 102 | 12,326.40 |
| Aarohan Distributor 05 | Rice 5kg | 40 | 9,916.99 |
| Aarohan Distributor 25 | Premium Tea 500g | 47 | 8,670.34 |

