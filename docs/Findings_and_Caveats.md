# Findings, Recommendations & Caveats

## Data and formula notice

Aarohan Consumer Products is fictional; all records are synthetic. Monetary figures are **unspecified currency units**, not INR. “Profit,” post-return sales and return value are explicitly estimates. The current rule reverses discounted selling value for returned units and reduces estimated COGS by returned units × product unit cost. If returned products are damaged, expired, restocked at a different value, or incur freight/restocking costs, a real financial model would need different rules.

## Five evidence-backed observations in this synthetic dataset

1. **Overall baseline:** net sales after estimated return adjustments are 41,546,999.57; estimated profit is 12,257,592.57; weighted estimated margin is 29.50%. These are derived from 30,000 clean transaction lines and 18,000 distinct orders.
2. **Year-over-year movement is slightly negative:** 2024 net sales = 20,990,320.77 and 2025 = 20,556,678.80. The change is -2.07%. Validate seasonality and product/channel mix before calling this a demand decline.
3. **Regional concentration:** North leads with 15,015,139.21 estimated net sales; East is lowest on this absolute-sales measure at 6,562,207.53. Total sales alone does not assess per-outlet productivity or market potential.
4. **Profit pool differs by product/category:** top estimated-profit SKU is Premium Tea 500g at 1,360,563.85; the lowest estimated-profit SKU is Salted Chips 50g at 169,224.01. The bottom five SKUs are still positive profit in this dataset, so do not label them loss-making. Highest-margin category is Snacks at 43.23%; lowest is Staples at 20.42%.
5. **Returns and discounting deserve investigation:** estimated unit-return rate overall is 3.15%; E-Commerce shows the highest rate by channel at 4.72%. The 20%+ discount band has 18.25% estimated margin versus 35.22% for the lowest discount band. This comparison is descriptive and may reflect product/channel/customer mix; it does not establish that higher discounts caused lower margin.

## Recommendations for a fictional management team

1. **Reconcile definitions with Finance first.** Confirm selling price basis, return accounting, damaged/expired stock, COGS, freight and tax treatment before using the estimates for actual decisions.
2. **Investigate return reason and channel combinations.** Start with the highest return-value reason and compare carrier, distributor, product, packaging, order size and time period. The synthetic data does not prove the cause.
3. **Review high-volume, lower-margin categories/SKUs.** Decompose margin into unit cost, realized price, discount, return mix and channel mix; avoid cancelling products based only on total profit ranking.
4. **Test discounts using controlled comparisons.** Compare like-for-like products, regions, periods and customer groups; where feasible, run a limited holdout/A-B promotion test before changing the discount policy.
5. **Investigate the 2025 decline by month and mix.** Compare same months year-over-year, orders, units, average order value, active customers and distribution coverage to separate calendar effects from mix/volume changes.

## What these data cannot prove

- No causal estimate: discounts are not proven to cause margin reduction; returns are not proven to cause a particular business decline.
- No actual inventory availability, stock-outs, delivery SLAs, marketing spend, competitor pricing, or regional population/market-potential data.
- Profit is estimated and no business currency is specified.
- Customer/distributor names are simulated; never present them as actual entities.
- All 1,000 synthetic customers in this source have at least two distinct orders, so there is no one-order customer cohort for repeat-vs-first-time comparison.
- No deployed or native Power BI file is supplied yet; dashboard preview images are static concept references.
