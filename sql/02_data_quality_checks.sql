USE aarohan_analytics;

-- 1. Raw row and order-line duplicate profiling.
SELECT COUNT(*) AS raw_rows,
       COUNT(DISTINCT order_line_id) AS distinct_order_line_ids,
       COUNT(*) - COUNT(DISTINCT order_line_id) AS repeated_order_line_id_rows
FROM orders_raw;

-- 2. Exact duplicate source rows.
SELECT COALESCE(SUM(duplicate_count - 1), 0) AS exact_duplicate_rows
FROM (
  SELECT order_line_id, order_id, order_date, ship_date, product_id, customer_id,
         distributor_id, geography_id, channel_id, quantity, unit_price,
         discount_pct, return_units, return_reason, return_date,
         COUNT(*) AS duplicate_count
  FROM orders_raw
  GROUP BY order_line_id, order_id, order_date, ship_date, product_id, customer_id,
           distributor_id, geography_id, channel_id, quantity, unit_price,
           discount_pct, return_units, return_reason, return_date
  HAVING COUNT(*) > 1
) AS exact_dupe_groups;

-- 3. Required-value and business-rule checks.
SELECT
  SUM(order_line_id IS NULL OR order_line_id = '') AS missing_line_id,
  SUM(order_id IS NULL OR order_id = '') AS missing_order_id,
  SUM(order_date IS NULL) AS missing_order_date,
  SUM(quantity <= 0) AS non_positive_quantity,
  SUM(unit_price <= 0) AS non_positive_unit_price,
  SUM(discount_pct < 0 OR discount_pct > 0.25) AS discount_out_of_bounds,
  SUM(return_units < 0 OR return_units > quantity) AS invalid_return_units,
  SUM(return_units > 0 AND (return_reason IS NULL OR return_date IS NULL)) AS returned_rows_missing_return_details
FROM orders_raw;

-- 4. Foreign-key lookup checks. Each unmatched count should be zero.
SELECT 'product_id' AS key_name, COUNT(*) AS unmatched_rows
FROM orders_raw o LEFT JOIN dim_products p ON o.product_id = p.product_id WHERE p.product_id IS NULL
UNION ALL
SELECT 'customer_id', COUNT(*)
FROM orders_raw o LEFT JOIN dim_customers c ON o.customer_id = c.customer_id WHERE c.customer_id IS NULL
UNION ALL
SELECT 'distributor_id', COUNT(*)
FROM orders_raw o LEFT JOIN dim_distributors d ON o.distributor_id = d.distributor_id WHERE d.distributor_id IS NULL
UNION ALL
SELECT 'geography_id', COUNT(*)
FROM orders_raw o LEFT JOIN dim_geography g ON o.geography_id = g.geography_id WHERE g.geography_id IS NULL
UNION ALL
SELECT 'channel_id', COUNT(*)
FROM orders_raw o LEFT JOIN dim_channels ch ON o.channel_id = ch.channel_id WHERE ch.channel_id IS NULL;

-- 5. Clean fact key and reconciliation checks.
SELECT COUNT(*) AS clean_rows,
       COUNT(DISTINCT order_line_id) AS distinct_order_lines,
       COUNT(*) - COUNT(DISTINCT order_line_id) AS duplicate_keys_after_cleaning
FROM fact_sales_clean;

SELECT COUNT(*) AS enriched_rows,
       SUM(gross_sales) AS gross_sales,
       SUM(discount_amount) AS discount_amount,
       SUM(net_sales_after_returns_est) AS estimated_net_sales,
       SUM(profit_est) AS estimated_profit,
       SUM(return_units) / NULLIF(SUM(quantity), 0) AS unit_return_rate
FROM v_sales_enriched;
