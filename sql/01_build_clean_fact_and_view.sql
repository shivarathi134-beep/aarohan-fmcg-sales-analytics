USE aarohan_analytics;

-- Create the curated fact by removing exact duplicate transaction rows only.
-- This leaves orders_raw unchanged for auditability.
DROP VIEW IF EXISTS v_sales_enriched;
DROP TABLE IF EXISTS fact_sales_clean;

CREATE TABLE fact_sales_clean AS
WITH ranked AS (
  SELECT o.*,
         ROW_NUMBER() OVER (
           PARTITION BY order_line_id, order_id, order_date, ship_date,
                        product_id, customer_id, distributor_id, geography_id,
                        channel_id, quantity, unit_price, discount_pct,
                        return_units, return_reason, return_date
           ORDER BY order_line_id
         ) AS duplicate_rank
  FROM orders_raw AS o
)
SELECT order_line_id, order_id, order_date, ship_date, product_id, customer_id,
       distributor_id, geography_id, channel_id, quantity, unit_price,
       discount_pct, return_units, return_reason, return_date
FROM ranked
WHERE duplicate_rank = 1;

ALTER TABLE fact_sales_clean
  ADD PRIMARY KEY (order_line_id),
  ADD INDEX idx_fact_order_date(order_date),
  ADD INDEX idx_fact_order_id(order_id),
  ADD INDEX idx_fact_product_id(product_id),
  ADD INDEX idx_fact_customer_id(customer_id),
  ADD INDEX idx_fact_geography_id(geography_id),
  ADD INDEX idx_fact_channel_id(channel_id),
  ADD INDEX idx_fact_distributor_id(distributor_id),
  ADD CONSTRAINT fk_fact_order_date FOREIGN KEY (order_date) REFERENCES dim_date(date_value),
  ADD CONSTRAINT fk_fact_product FOREIGN KEY (product_id) REFERENCES dim_products(product_id),
  ADD CONSTRAINT fk_fact_customer FOREIGN KEY (customer_id) REFERENCES dim_customers(customer_id),
  ADD CONSTRAINT fk_fact_distributor FOREIGN KEY (distributor_id) REFERENCES dim_distributors(distributor_id),
  ADD CONSTRAINT fk_fact_geography FOREIGN KEY (geography_id) REFERENCES dim_geography(geography_id),
  ADD CONSTRAINT fk_fact_channel FOREIGN KEY (channel_id) REFERENCES dim_channels(channel_id);

-- Semantic view centralises the metric definitions used by the analysis queries.
CREATE OR REPLACE VIEW v_sales_enriched AS
SELECT
  f.order_line_id, f.order_id, f.order_date, f.ship_date, f.return_date,
  YEAR(f.order_date) AS order_year,
  DATE_FORMAT(f.order_date, '%Y-%m') AS year_month,
  f.product_id, p.product_name, p.category, p.brand, p.pack_size,
  p.unit_cost, p.list_price,
  f.customer_id, c.customer_name, c.customer_segment, c.customer_type,
  f.distributor_id, d.distributor_name, d.distributor_tier,
  f.geography_id, g.state_name, g.region_name,
  f.channel_id, ch.channel_name,
  f.quantity, f.unit_price, f.discount_pct, f.return_units,
  f.return_reason,
  f.quantity * f.unit_price AS gross_sales,
  f.quantity * f.unit_price * f.discount_pct AS discount_amount,
  f.quantity * f.unit_price * (1 - f.discount_pct) AS net_sales_pre_returns,
  f.return_units * f.unit_price * (1 - f.discount_pct) AS return_value_est,
  f.quantity * f.unit_price * (1 - f.discount_pct)
    - f.return_units * f.unit_price * (1 - f.discount_pct) AS net_sales_after_returns_est,
  f.quantity - f.return_units AS net_units_est,
  (f.quantity - f.return_units) * p.unit_cost AS cogs_net_units_est,
  (f.quantity * f.unit_price * (1 - f.discount_pct)
    - f.return_units * f.unit_price * (1 - f.discount_pct)
    - (f.quantity - f.return_units) * p.unit_cost) AS profit_est
FROM fact_sales_clean AS f
JOIN dim_products AS p ON f.product_id = p.product_id
JOIN dim_customers AS c ON f.customer_id = c.customer_id
JOIN dim_distributors AS d ON f.distributor_id = d.distributor_id
JOIN dim_geography AS g ON f.geography_id = g.geography_id
JOIN dim_channels AS ch ON f.channel_id = ch.channel_id;

-- Add the unique-key constraint and curated row count should now be 30,000.
SELECT COUNT(*) AS clean_fact_rows,
       COUNT(DISTINCT order_line_id) AS unique_order_lines,
       COUNT(DISTINCT order_id) AS distinct_orders
FROM fact_sales_clean;
