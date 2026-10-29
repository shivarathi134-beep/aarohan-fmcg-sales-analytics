-- Aarohan Consumer Products | MySQL 8.0+
-- Fictional synthetic case study. Keep the raw table unchanged for traceability.
CREATE DATABASE IF NOT EXISTS aarohan_analytics
  CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
USE aarohan_analytics;

-- Drop dependent objects first so a deliberate rebuild does not fail on FK references.
DROP VIEW IF EXISTS v_sales_enriched;
DROP TABLE IF EXISTS fact_sales_clean;
DROP TABLE IF EXISTS orders_raw;
DROP TABLE IF EXISTS dim_products;
DROP TABLE IF EXISTS dim_geography;
DROP TABLE IF EXISTS dim_channels;
DROP TABLE IF EXISTS dim_customers;
DROP TABLE IF EXISTS dim_distributors;
DROP TABLE IF EXISTS dim_date;

-- Do not add a primary key to orders_raw: the source intentionally contains
-- 60 exact duplicate rows for the learner to identify and remove analytically.
CREATE TABLE orders_raw (
  order_line_id VARCHAR(32) NOT NULL,
  order_id VARCHAR(32) NOT NULL,
  order_date DATE NOT NULL,
  ship_date DATE NULL,
  product_id VARCHAR(24) NOT NULL,
  customer_id VARCHAR(24) NOT NULL,
  distributor_id VARCHAR(24) NOT NULL,
  geography_id VARCHAR(24) NOT NULL,
  channel_id VARCHAR(24) NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(12,2) NOT NULL,
  discount_pct DECIMAL(6,4) NOT NULL,
  return_units INT NOT NULL DEFAULT 0,
  return_reason VARCHAR(100) NULL,
  return_date DATE NULL,
  INDEX idx_raw_order_id(order_id),
  INDEX idx_raw_order_date(order_date),
  INDEX idx_raw_product_id(product_id),
  INDEX idx_raw_customer_id(customer_id)
);

CREATE TABLE dim_products (
  product_id VARCHAR(24) PRIMARY KEY,
  product_name VARCHAR(120) NOT NULL,
  category VARCHAR(80) NOT NULL,
  brand VARCHAR(80) NOT NULL,
  pack_size VARCHAR(40) NOT NULL,
  unit_cost DECIMAL(12,2) NOT NULL,
  list_price DECIMAL(12,2) NOT NULL
);
CREATE TABLE dim_geography (
  geography_id VARCHAR(24) PRIMARY KEY,
  state_name VARCHAR(80) NOT NULL,
  region_name VARCHAR(40) NOT NULL
);
CREATE TABLE dim_channels (
  channel_id VARCHAR(24) PRIMARY KEY,
  channel_name VARCHAR(60) NOT NULL
);
CREATE TABLE dim_customers (
  customer_id VARCHAR(24) PRIMARY KEY,
  customer_name VARCHAR(120) NOT NULL,
  customer_segment VARCHAR(60) NOT NULL,
  customer_type VARCHAR(60) NOT NULL
);
CREATE TABLE dim_distributors (
  distributor_id VARCHAR(24) PRIMARY KEY,
  distributor_name VARCHAR(120) NOT NULL,
  distributor_tier VARCHAR(60) NOT NULL
);
CREATE TABLE dim_date (
  date_value DATE PRIMARY KEY,
  year_num SMALLINT NOT NULL,
  quarter_num TINYINT NOT NULL,
  month_num TINYINT NOT NULL,
  month_name VARCHAR(20) NOT NULL,
  year_month CHAR(7) NOT NULL,
  day_num TINYINT NOT NULL,
  day_name VARCHAR(20) NOT NULL,
  INDEX idx_date_year_month(year_num, month_num)
);

-- Import the seven matching CSVs through MySQL Workbench's Table Data Import Wizard.
-- Target table names must match the CSV names (without .csv). Import dimensions first,
-- then orders_raw. If re-importing, clear the destination table before import.
