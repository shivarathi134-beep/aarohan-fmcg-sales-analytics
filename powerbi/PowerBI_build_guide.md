# Power BI Desktop Implementation Guide

## Delivery status (read first)

This folder contains DAX measures, a theme JSON, Power Query helper, model instructions, static dashboard design previews, and a manual QA checklist. **No native `.pbix` file was created or validated here.** The PNGs are Matplotlib design references, not Power BI screenshots and do not demonstrate working slicers or drill-through. Build and test the report in Power BI Desktop before describing it as complete.

## 1. Import the data

Use **Home → Get data → Text/CSV**. Import these files and rename each table exactly:

| Power BI table | File | Expected rows |
|---|---|---:|
| `FactOrders` | `outputs/fact_orders_clean.csv` | 30,000 |
| `DimProducts` | `data/dim_products.csv` | 20 |
| `DimCustomers` | `data/dim_customers.csv` | 1,000 |
| `DimDistributors` | `data/dim_distributors.csv` | 60 |
| `DimGeography` | `data/dim_geography.csv` | 16 |
| `DimChannels` | `data/dim_channels.csv` | 4 |
| `DimDate` | `data/dim_date.csv` | 731 |

In Power Query, verify `order_date`, `ship_date`, `return_date` and `DimDate[date_value]` are **Date**, percentages are Decimal Number, unit counts are Whole Number, and monetary values are Decimal Number. For monetary fields use two decimal places for display while keeping full numeric precision in the model.

## 2. Create the model

Create active one-to-many relationships with single-direction filtering from dimension to fact:

- `DimDate[date_value]` (1) → `FactOrders[order_date]` (*)
- `DimProducts[product_id]` (1) → `FactOrders[product_id]` (*)
- `DimCustomers[customer_id]` (1) → `FactOrders[customer_id]` (*)
- `DimDistributors[distributor_id]` (1) → `FactOrders[distributor_id]` (*)
- `DimGeography[geography_id]` (1) → `FactOrders[geography_id]` (*)
- `DimChannels[channel_id]` (1) → `FactOrders[channel_id]` (*)

Mark `DimDate` as the date table using `date_value`. Sort `DimDate[month_name]` by `month_num` and `year_month` by a chronological key such as `date_value` (or add a `YearMonthSort = year_num * 100 + month_num` column and sort `year_month` by it). Keep the date relationship single and active; only add separate inactive return-date relationship if you deliberately create return-date-specific measures.

## 3. Load measures and theme

1. In Power BI Desktop, create measures from `DAX_Measures.dax` one at a time in `FactOrders` (or a dedicated `_Measures` table).
2. Import `theme.json` using **View → Themes → Browse for themes**.
3. Apply consistent formatting: amount measures = 2 decimals; margin, growth, discount, contribution, return rate = percentages; order and unit counts = whole numbers.
4. Check base measures against `outputs/executive_summary.csv`. The DAX is supplied source, not a verified PBIX; Power BI's local parsing and filter behavior still need checking.

## 4. Build four clean, interactive pages

### Page 1 — Executive Overview

Header: `AAROHAN | FMCG PERFORMANCE`, report period, and a reset-filter bookmark button. KPI strip: Estimated Net Sales, Estimated Profit, Estimated Profit Margin %, Distinct Orders, Unit Return Rate %. Charts: month-by-month net sales and estimated profit, sales by region, profit by category, sales by channel. Add slicers for `DimDate[date_value]` (Between), `DimGeography[region_name]`, `DimProducts[category]`, and `DimChannels[channel_name]`.

### Page 2 — Product & Profitability

Use a horizontal bar chart for top 10 SKUs by Estimated Profit; a table with product, category, net sales, estimated profit, margin, return rate; a scatterplot of net sales vs estimated margin with product as details; category comparison; conditional formatting on margin. Add a drill-through page named `Product Detail` filtered by product; include trend, returns and channel mix.

### Page 3 — Customer & Channel

Show net sales / estimated profit by customer segment and channel, top customers by estimated net sales, distinct orders, average order value, repeat-customer segment if you build and validate a customer-level calculated table. Avoid counting line rows as orders. Enable drill-through on customer only after setting the field and validating filter propagation.

### Page 4 — Regional & Returns

Use a state-level bar chart or map only if geographical rendering is reliable. Add region/state table with net sales, profit, margin and unit-return rate. Add return reason chart and channel return-rate comparison. Highlight `Damaged in Transit` and high-return channels as investigation leads, not as proven causes.

## 5. Interactions

- Use Format → Edit interactions to ensure slicers and chart selections filter the intended visuals.
- Add report-page navigation buttons or the built-in Page Navigator.
- Add a reset bookmark: clear slicers to default → View → Bookmarks → Add → name `Reset filters` → assign it to a button.
- Create a report-page tooltip, set page size to Tooltip, add net sales, estimated profit, margin and return-rate measures, then assign it to the product/region visuals.
- Add drill-through fields on `Product Detail` and optionally `Customer Detail`; test right-click → Drill through.
- Dynamic title can use `[Executive Page Title]` from the DAX library.

## 6. QA before sharing

See `POWER_BI_MANUAL_QA.md`. At minimum verify all KPIs and time trends against Python outputs, check all slicers, month sorting, cross-filtering, reset bookmark, tooltips, page navigation, drill-through, layout at 16:9, and save/reopen the `.pbix`. Record any mismatch rather than silently adjusting the expected numbers.

## Design reference

- `dashboard_preview.png` — static executive overview design reference.
- `dashboard_product_returns_preview.png` — static SKU / returns design reference.

The previews are generated from Python summaries, have no Power BI interaction, and must not be represented as screenshots of a finished report.
