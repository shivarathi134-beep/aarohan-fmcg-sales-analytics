# Power BI Manual QA Checklist

Date tested: ____________________  Power BI Desktop version: ____________________

## Data/model integrity
- [ ] `FactOrders` loads 30,000 rows and 30,000 distinct `order_line_id` values.
- [ ] Dimension row counts match: products 20; customers 1,000; distributors 60; geography 16; channels 4; dates 731.
- [ ] Six dimension→fact relationships are active, one-to-many and single-direction.
- [ ] `DimDate` is marked as date table; month name and year-month labels sort chronologically.
- [ ] No unexpected blank product/customer/region/channel labels after joins.

## Core KPI reconciliation
- [ ] Gross Sales = 47,450,732.16
- [ ] Discount Amount = 4,580,888.23
- [ ] Net Sales Before Returns = 42,869,843.93
- [ ] Estimated Return Value = 1,322,844.36
- [ ] Estimated Net Sales = 41,546,999.57
- [ ] Estimated COGS = 29,289,407.00
- [ ] Estimated Profit = 12,257,592.57
- [ ] Estimated Profit Margin = 29.50%
- [ ] Distinct Orders = 18,000
- [ ] Unit Return Rate = 3.15%

Reference CSVs: `outputs/executive_summary.csv`, `outputs/yearly_summary.csv`, `outputs/product_summary.csv`, `outputs/region_summary.csv`, `outputs/channel_summary.csv`.

## Interaction and visual QA
- [ ] Date range, region, category, channel slicers apply to intended charts/cards.
- [ ] Clicking a region/category/product cross-filters where expected.
- [ ] Date line-chart shows months in chronological order.
- [ ] Previous-year measures return blank when there is no comparable prior period; growth does not misleadingly show 0% for missing prior data.
- [ ] Reset bookmark clears filters.
- [ ] Page navigation works from every page.
- [ ] Tooltip appears on hover and shows measures matching the selected point.
- [ ] Product drill-through preserves product filter; Back button works.
- [ ] Conditional formatting has meaningful positive/negative/status semantics.
- [ ] Labels fit, figures have sensible formats, and report reads well at 16:9.
- [ ] Save as `Aarohan_Consumer_Products_Analytics.pbix`, close, reopen, and recheck the main page.

**Status must remain “Requires Manual Verification” until these checks are completed in Power BI Desktop.**
