USE aarohan_analytics;

-- Q01 | What are the headline financial and operating KPIs?
SELECT COUNT(DISTINCT order_id) AS distinct_orders,
       COUNT(DISTINCT order_line_id) AS order_lines,
       SUM(quantity) AS units_ordered,
       SUM(return_units) AS units_returned,
       SUM(gross_sales) AS gross_sales,
       SUM(discount_amount) AS discount_amount,
       SUM(net_sales_pre_returns) AS net_sales_before_returns,
       SUM(return_value_est) AS estimated_return_value,
       SUM(net_sales_after_returns_est) AS estimated_net_sales,
       SUM(cogs_net_units_est) AS estimated_cogs,
       SUM(profit_est) AS estimated_profit,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_profit_margin,
       SUM(return_units) / NULLIF(SUM(quantity), 0) AS unit_return_rate
FROM v_sales_enriched;

-- Q02 | How did yearly net sales and profit change? (year-over-year comparison)
WITH annual AS (
  SELECT order_year,
         COUNT(DISTINCT order_id) AS distinct_orders,
         SUM(net_sales_after_returns_est) AS net_sales,
         SUM(profit_est) AS estimated_profit
  FROM v_sales_enriched
  GROUP BY order_year
), lagged AS (
  SELECT annual.*,
         LAG(net_sales) OVER (ORDER BY order_year) AS prior_year_sales,
         LAG(estimated_profit) OVER (ORDER BY order_year) AS prior_year_profit
  FROM annual
)
SELECT order_year, distinct_orders, net_sales, estimated_profit,
       (net_sales - prior_year_sales) / NULLIF(prior_year_sales, 0) AS sales_growth_pct,
       (estimated_profit - prior_year_profit) / NULLIF(prior_year_profit, 0) AS profit_growth_pct
FROM lagged ORDER BY order_year;

-- Q03 | What is the monthly sales trend and change versus the prior month?
WITH monthly AS (
  SELECT year_month, MIN(order_date) AS month_start,
         SUM(net_sales_after_returns_est) AS net_sales,
         SUM(profit_est) AS estimated_profit
  FROM v_sales_enriched GROUP BY year_month
), m AS (
  SELECT monthly.*,
         LAG(net_sales) OVER (ORDER BY year_month) AS prior_month_sales
  FROM monthly
)
SELECT year_month, net_sales, estimated_profit,
       (net_sales - prior_month_sales) / NULLIF(prior_month_sales, 0) AS month_over_month_growth_pct
FROM m ORDER BY year_month;

-- Q04 | Which products contribute the most/least estimated profit?
SELECT product_id, product_name, category,
       SUM(net_sales_after_returns_est) AS net_sales,
       SUM(profit_est) AS estimated_profit,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin,
       RANK() OVER (ORDER BY SUM(profit_est) DESC) AS profit_rank
FROM v_sales_enriched
GROUP BY product_id, product_name, category
ORDER BY estimated_profit DESC;

-- Q05 | Which categories contribute most to net sales and profit?
WITH cat AS (
  SELECT category, SUM(net_sales_after_returns_est) AS net_sales,
         SUM(profit_est) AS estimated_profit
  FROM v_sales_enriched GROUP BY category
)
SELECT category, net_sales, estimated_profit,
       net_sales / NULLIF(SUM(net_sales) OVER (), 0) AS sales_contribution_pct,
       estimated_profit / NULLIF(SUM(estimated_profit) OVER (), 0) AS profit_contribution_pct,
       estimated_profit / NULLIF(net_sales, 0) AS estimated_margin
FROM cat ORDER BY estimated_profit DESC;

-- Q06 | Which regions and states contribute the most sales/profit?
SELECT region_name, state_name,
       SUM(net_sales_after_returns_est) AS net_sales,
       SUM(profit_est) AS estimated_profit,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin,
       SUM(return_units) / NULLIF(SUM(quantity), 0) AS unit_return_rate
FROM v_sales_enriched
GROUP BY region_name, state_name
ORDER BY net_sales DESC;

-- Q07 | How do sales and profitability compare by channel?
SELECT channel_name, COUNT(DISTINCT order_id) AS distinct_orders,
       SUM(net_sales_after_returns_est) AS net_sales,
       SUM(profit_est) AS estimated_profit,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin,
       SUM(return_units) / NULLIF(SUM(quantity), 0) AS unit_return_rate
FROM v_sales_enriched GROUP BY channel_name ORDER BY net_sales DESC;

-- Q08 | Which customer segments generate the most net sales?
SELECT customer_segment, customer_type,
       COUNT(DISTINCT customer_id) AS customers,
       COUNT(DISTINCT order_id) AS distinct_orders,
       SUM(net_sales_after_returns_est) AS net_sales,
       SUM(profit_est) AS estimated_profit,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin
FROM v_sales_enriched
GROUP BY customer_segment, customer_type ORDER BY net_sales DESC;

-- Q09 | Who are the top 20 customers by net sales?
SELECT customer_id, customer_name, customer_segment,
       COUNT(DISTINCT order_id) AS distinct_orders,
       SUM(net_sales_after_returns_est) AS net_sales,
       SUM(profit_est) AS estimated_profit
FROM v_sales_enriched
GROUP BY customer_id, customer_name, customer_segment
ORDER BY net_sales DESC LIMIT 20;

-- Q10 | Which distributors have high sales but weaker profit margins?
SELECT distributor_id, distributor_name, distributor_tier,
       COUNT(DISTINCT order_id) AS distinct_orders,
       SUM(net_sales_after_returns_est) AS net_sales,
       SUM(profit_est) AS estimated_profit,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin,
       SUM(return_units) / NULLIF(SUM(quantity), 0) AS unit_return_rate
FROM v_sales_enriched
GROUP BY distributor_id, distributor_name, distributor_tier
ORDER BY net_sales DESC;

-- Q11 | How does profitability differ across discount bands?
WITH tagged AS (
 SELECT *, CASE
   WHEN discount_pct < 0.05 THEN '0–4.9%'
   WHEN discount_pct < 0.10 THEN '5–9.9%'
   WHEN discount_pct < 0.20 THEN '10–19.9%'
   ELSE '20%+'
 END AS discount_band
 FROM v_sales_enriched
)
SELECT discount_band, COUNT(DISTINCT order_id) AS distinct_orders,
       SUM(gross_sales) AS gross_sales,
       SUM(discount_amount) AS discount_amount,
       SUM(net_sales_after_returns_est) AS net_sales,
       SUM(profit_est) AS estimated_profit,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin
FROM tagged GROUP BY discount_band ORDER BY MIN(discount_pct);

-- Q12 | What are the most common/high-value recorded return reasons?
SELECT return_reason, COUNT(DISTINCT order_line_id) AS return_lines,
       COUNT(DISTINCT order_id) AS distinct_orders,
       SUM(return_units) AS returned_units,
       SUM(return_value_est) AS estimated_return_value
FROM v_sales_enriched WHERE return_units > 0
GROUP BY return_reason ORDER BY estimated_return_value DESC;

-- Q13 | Which channels show elevated unit-return rates?
SELECT channel_name, SUM(quantity) AS units_ordered,
       SUM(return_units) AS units_returned,
       SUM(return_units) / NULLIF(SUM(quantity), 0) AS unit_return_rate,
       SUM(return_value_est) AS estimated_return_value
FROM v_sales_enriched GROUP BY channel_name ORDER BY unit_return_rate DESC;

-- Q14 | Which products have above-average sales but below-average margin?
WITH overall AS (
  SELECT SUM(net_sales_after_returns_est) / COUNT(DISTINCT order_id) AS avg_sales_per_order,
         SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS overall_margin
  FROM v_sales_enriched
), product AS (
  SELECT product_id, product_name, category,
         SUM(net_sales_after_returns_est) AS net_sales,
         COUNT(DISTINCT order_id) AS orders,
         SUM(profit_est) AS estimated_profit,
         SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin
  FROM v_sales_enriched GROUP BY product_id, product_name, category
)
SELECT p.*, o.overall_margin
FROM product p CROSS JOIN overall o
WHERE p.net_sales / NULLIF(p.orders,0) > o.avg_sales_per_order
  AND p.estimated_margin < o.overall_margin
ORDER BY p.net_sales DESC;

-- Q15 | How many customers are repeat purchasers?
WITH customer_orders AS (
  SELECT customer_id, COUNT(DISTINCT order_id) AS order_count,
         SUM(net_sales_after_returns_est) AS net_sales
  FROM v_sales_enriched GROUP BY customer_id
)
SELECT CASE WHEN order_count >= 2 THEN 'Repeat customer' ELSE 'One-order customer' END AS customer_type_group,
       COUNT(*) AS customers,
       AVG(order_count) AS average_orders_per_customer,
       SUM(net_sales) AS net_sales
FROM customer_orders GROUP BY customer_type_group;

-- Q16 | Rank products within each category by estimated profit.
WITH p AS (
  SELECT product_id, product_name, category, SUM(profit_est) AS estimated_profit
  FROM v_sales_enriched GROUP BY product_id, product_name, category
)
SELECT p.*, DENSE_RANK() OVER (PARTITION BY category ORDER BY estimated_profit DESC) AS category_profit_rank
FROM p ORDER BY category, category_profit_rank;

-- Q17 | What is average order value using distinct order totals (not line averages)?
WITH order_totals AS (
  SELECT order_id, SUM(net_sales_after_returns_est) AS order_net_sales,
         SUM(profit_est) AS order_profit
  FROM v_sales_enriched GROUP BY order_id
)
SELECT COUNT(*) AS distinct_orders,
       SUM(order_net_sales) AS total_net_sales,
       AVG(order_net_sales) AS average_order_value,
       AVG(order_profit) AS average_order_profit
FROM order_totals;

-- Q18 | How do return rates and margins vary by product?
SELECT product_id, product_name, category,
       SUM(quantity) AS units_ordered,
       SUM(return_units) AS units_returned,
       SUM(return_units) / NULLIF(SUM(quantity),0) AS unit_return_rate,
       SUM(return_value_est) AS estimated_return_value,
       SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est),0) AS estimated_margin
FROM v_sales_enriched GROUP BY product_id, product_name, category
ORDER BY unit_return_rate DESC;

-- Q19 | Label region performance for review; this is a descriptive rule, not causation.
WITH r AS (
  SELECT region_name, SUM(net_sales_after_returns_est) AS net_sales,
         SUM(profit_est) / NULLIF(SUM(net_sales_after_returns_est), 0) AS estimated_margin
  FROM v_sales_enriched GROUP BY region_name
)
SELECT r.*,
       CASE WHEN estimated_margin < (SELECT AVG(estimated_margin) FROM r)
            THEN 'Review margin drivers' ELSE 'At/above region-average margin' END AS review_flag
FROM r ORDER BY net_sales DESC;

-- Q20 | Which distributor × product combinations drive return value?
SELECT distributor_name, product_name, category,
       SUM(return_units) AS returned_units,
       SUM(return_value_est) AS estimated_return_value,
       SUM(net_sales_after_returns_est) AS net_sales
FROM v_sales_enriched WHERE return_units > 0
GROUP BY distributor_name, product_name, category
ORDER BY estimated_return_value DESC LIMIT 25;
