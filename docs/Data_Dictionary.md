# Data Dictionary

## Fact source: `data/orders_raw.csv`
**Grain:** one order-line record, with some exact rows duplicated deliberately for data-quality practice.

| Column | Meaning | Suggested SQL type |
|---|---|---|
| order_line_id | Order-line identifier | VARCHAR(32) |
| order_id | Order identifier; may repeat across lines | VARCHAR(32) |
| order_date | Order date | DATE |
| ship_date | Ship/dispatch date | DATE |
| product_id | Product dimension key | VARCHAR(24) |
| customer_id | Customer dimension key | VARCHAR(24) |
| distributor_id | Distributor dimension key | VARCHAR(24) |
| geography_id | Geography dimension key | VARCHAR(24) |
| channel_id | Sales channel dimension key | VARCHAR(24) |
| quantity | Units on order line | INT |
| unit_price | Selling price per unit before discount | DECIMAL(12,2) |
| discount_pct | Discount fraction (0.10 = 10%) | DECIMAL(6,4) |
| return_units | Units returned | INT |
| return_reason | Return reason; conditionally blank for non-returns | VARCHAR(100) |
| return_date | Return date; conditionally blank for non-returns | DATE |

## Dimensions
- `dim_products.csv`: product name, category, brand, pack size, unit cost, list price.
- `dim_customers.csv`: customer name, customer segment, customer type.
- `dim_distributors.csv`: distributor name and tier.
- `dim_geography.csv`: state and region.
- `dim_channels.csv`: channel ID and channel name.
- `dim_date.csv`: one row per date with year, quarter, month, year-month and day attributes.

## Grain and join keys
`orders_raw` → dimensions use `product_id`, `customer_id`, `distributor_id`, `geography_id`, `channel_id`; order date joins to `dim_date.date_value`.
