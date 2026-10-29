# Methodology and Metric Definitions

## Analytical objective

Assess a fictional FMCG sales/distribution operation using order-line records. Main dimensions are time, product/category, customer segment/type, geography, channel, and distributor. The work is descriptive analysis for portfolio learning, not evidence about a real company.

## Source and synthetic-data construction

All seven source CSVs in `data/` are synthetic portfolio inputs. They represent a two-year transaction history (2024–2025) plus matching product, customer, geography, channel, distributor and date dimensions. The source includes 20 SKUs, 1,000 customers, 60 distributors, 16 geography/state members, four channels and a 731-day date dimension. Transaction fields model an FMCG order line: line/order identifiers, order/ship/return dates, dimension keys, quantity, unit price, discount fraction, returned units and conditional return reason/date. The synthetic source includes 60 exact duplicate order-line records deliberately to make data-quality handling visible. Quantity and price are positive, discounts are within 0–25%, and return units do not exceed line quantity.

**Generation transparency:** the archived project inputs contain the already-generated synthetic CSVs but did not include the original source-data generator or a trustworthy generation seed description. Therefore, this repository treats `data/*.csv` as the authoritative synthetic inputs and does not claim that the raw rows can be recreated byte-for-byte from a supplied generator. The *analysis pipeline* is reproducible against those included inputs: `python python/aarohan_analysis.py` deterministically redoes cleaning, calculations and outputs without changing the raw CSVs. No public dataset, client dataset or employer data is used.

## Grain and cleaning

- **Source grain:** one order line per row, with exact duplicate rows intentionally included.
- **Order key:** `order_id` can repeat across line items; use distinct order IDs for order counts.
- **Line key:** `order_line_id` should be unique after exact duplicate removal.
- **Cleaning:** preserve source; parse date columns; remove exact duplicate rows only in the analytical copy; validate required fields, positive quantity/price, discount range, returned quantity bounds, and dimension joins.
- **Dimension joins:** Python merges use `validate='many_to_one'` so a duplicated dimension key cannot silently fan out fact rows.
- **No blanket imputation:** required-field errors are surfaced as validation failures rather than automatically filled with invented values.

## Commercial calculations

For each order-line row:

1. `gross_sales = quantity × unit_price`
2. `discount_amount = gross_sales × discount_pct`
3. `net_sales_pre_returns = gross_sales − discount_amount`
4. `return_value_est = return_units × unit_price × (1 − discount_pct)`
5. `net_sales_after_returns_est = net_sales_pre_returns − return_value_est`
6. `net_units_est = quantity − return_units`
7. `cogs_net_units_est = net_units_est × product unit_cost`
8. `profit_est = net_sales_after_returns_est − cogs_net_units_est`
9. `profit_margin_pct_est = profit_est ÷ net_sales_after_returns_est`, where denominator is nonzero
10. `unit_return_rate = SUM(return_units) ÷ SUM(quantity)` for an aggregate group

For a period/category/region the weighted margin is **SUM(profit_est) / SUM(net_sales_after_returns_est)**, not the arithmetic mean of line-level margins. Average order value is total net sales divided by distinct orders, not the average order-line value.

## Assumptions and limitations

- Currency is unspecified, so all monetary amounts are “currency units” and no currency symbol is added.
- `unit_price` is treated as pre-discount unit selling price; `discount_pct` is a decimal fraction (e.g., 0.10 = 10%).
- Return value reverses the discounted selling value for `return_units` and assumes returned units reduce estimated COGS as though they are recovered at recorded unit cost. The source does not state whether returned items are resellable, damaged, expired, or subject to freight/restocking costs.
- Profit excludes other costs not in the dataset (e.g., payroll, rent, logistics, taxes, trade spend, overhead).
- “Return value” is a calculated estimate rather than an actual refund/payment ledger.
- No causation claim is made from discount-band, region, product or return differences.
- The dataset is synthetic; customer/distributor names and findings must not be represented as actual commercial facts.

## Validation approach

The Python script writes a named validation table (`outputs/validation_checks.csv`) and data-quality summary (`outputs/data_quality_checks.csv`). SQL and Power BI have equivalent definitions and reference outputs but require manual execution and reconciliation in MySQL Workbench and Power BI Desktop before their execution status can be called complete. Excel formulas have been written into the workbook; formula recalculation needs a desktop Excel check.
