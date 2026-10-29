"""Aarohan Consumer Products — reproducible FMCG analytics pipeline.

Run from the repository root:
    python python/aarohan_analysis.py

Requires pandas and numpy. All source data is synthetic. Profit/return logic is an
explicit estimate, not audited accounting, because currency and inventory policy
were not provided with the learning dataset.
"""
from pathlib import Path
import json
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

orders_raw = pd.read_csv(DATA / "orders_raw.csv")
source_row_count = int(len(orders_raw))
exact_duplicate_count = int(orders_raw.duplicated().sum())
line_id_duplicate_count = int(orders_raw["order_line_id"].duplicated().sum())

# Load dimensions.
dims = {
    "products": pd.read_csv(DATA / "dim_products.csv"),
    "geography": pd.read_csv(DATA / "dim_geography.csv"),
    "channels": pd.read_csv(DATA / "dim_channels.csv"),
    "customers": pd.read_csv(DATA / "dim_customers.csv"),
    "distributors": pd.read_csv(DATA / "dim_distributors.csv"),
    "date": pd.read_csv(DATA / "dim_date.csv"),
}

# Preserve source: deduplicate only in the analytical copy.
orders = orders_raw.drop_duplicates().copy()
for c in ["order_date", "ship_date", "return_date"]:
    orders[c] = pd.to_datetime(orders[c], errors="coerce")

# Join descriptive attributes. Many-to-one validation prevents dimension fan-out.
df = orders.merge(dims["products"], on="product_id", how="left", validate="many_to_one")
df = df.merge(dims["geography"], on="geography_id", how="left", validate="many_to_one")
df = df.merge(dims["channels"], on="channel_id", how="left", validate="many_to_one")
df = df.merge(dims["customers"], on="customer_id", how="left", validate="many_to_one")
df = df.merge(dims["distributors"], on="distributor_id", how="left", validate="many_to_one")

# Commercial definitions. Returns reverse discounted selling price and returned
# units reduce estimated COGS; confirm this policy before using on real accounts.
df["gross_sales"] = df["quantity"] * df["unit_price"]
df["discount_amount"] = df["gross_sales"] * df["discount_pct"]
df["net_sales_pre_returns"] = df["gross_sales"] - df["discount_amount"]
df["return_value_est"] = df["return_units"] * df["unit_price"] * (1 - df["discount_pct"])
df["net_sales_after_returns_est"] = df["net_sales_pre_returns"] - df["return_value_est"]
df["net_units_est"] = df["quantity"] - df["return_units"]
df["cogs_net_units_est"] = df["net_units_est"] * df["unit_cost"]
df["profit_est"] = df["net_sales_after_returns_est"] - df["cogs_net_units_est"]
df["profit_margin_pct_est"] = np.where(
    df["net_sales_after_returns_est"] != 0,
    df["profit_est"] / df["net_sales_after_returns_est"], np.nan
)
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.month
df["year_month"] = df["order_date"].dt.to_period("M").astype(str)
df["discount_band"] = pd.cut(
    df["discount_pct"], bins=[-0.000001, 0.05, 0.10, 0.20, 1.000001],
    labels=["0–4.9%", "5–9.9%", "10–19.9%", "20%+"], right=False
).astype("string")

# Export analytical detail and Power BI fact (same 30,000-line grain).
df.to_csv(OUT / "analysis_detail.csv", index=False, date_format="%Y-%m-%d")
fact_cols = [
    "order_line_id", "order_id", "order_date", "ship_date", "product_id", "customer_id",
    "distributor_id", "geography_id", "channel_id", "quantity", "unit_price", "discount_pct",
    "return_units", "return_reason", "return_date", "gross_sales", "discount_amount",
    "net_sales_pre_returns", "return_value_est", "net_sales_after_returns_est", "net_units_est",
    "cogs_net_units_est", "profit_est", "profit_margin_pct_est"
]
df[fact_cols].to_csv(OUT / "fact_orders_clean.csv", index=False, date_format="%Y-%m-%d")

# Reusable grouped business output. Weighted margin is profit divided by net sales,
# not the unweighted average of line-level margins.
def grouped_summary(group_cols, filename):
    g = df.groupby(group_cols, dropna=False).agg(
        order_lines=("order_line_id", "nunique"),
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum"),
        returned_units=("return_units", "sum"),
        gross_sales=("gross_sales", "sum"),
        discount_amount=("discount_amount", "sum"),
        net_sales_pre_returns=("net_sales_pre_returns", "sum"),
        return_value_est=("return_value_est", "sum"),
        net_sales_after_returns_est=("net_sales_after_returns_est", "sum"),
        profit_est=("profit_est", "sum"),
    ).reset_index()
    g["profit_margin_pct_est"] = np.where(
        g["net_sales_after_returns_est"] != 0,
        g["profit_est"] / g["net_sales_after_returns_est"], np.nan
    )
    g["unit_return_rate"] = np.where(g["quantity"] != 0, g["returned_units"] / g["quantity"], np.nan)
    g.to_csv(OUT / filename, index=False)
    return g

monthly = grouped_summary(["year_month"], "monthly_summary.csv")
yearly = grouped_summary(["year"], "yearly_summary.csv")
product = grouped_summary(["product_id", "product_name", "category"], "product_summary.csv")
region = grouped_summary(["region_name"], "region_summary.csv")
state = grouped_summary(["state_name", "region_name"], "state_summary.csv")
channel = grouped_summary(["channel_name"], "channel_summary.csv")
category = grouped_summary(["category"], "category_summary.csv")
distributor = grouped_summary(["distributor_id", "distributor_name", "distributor_tier"], "distributor_summary.csv")
segment = grouped_summary(["customer_segment", "customer_type"], "customer_segment_summary.csv")

discount = grouped_summary(["discount_band"], "discount_band_summary.csv")
returns_only = df[df["return_units"] > 0].copy()
return_reason = returns_only.groupby("return_reason", dropna=False).agg(
    returned_lines=("order_line_id", "nunique"), returned_units=("return_units", "sum"),
    estimated_return_value=("return_value_est", "sum"),
    distinct_orders=("order_id", "nunique")
).reset_index().sort_values("estimated_return_value", ascending=False)
return_reason.to_csv(OUT / "return_reason_summary.csv", index=False)

customer = grouped_summary(["customer_id", "customer_name", "customer_segment", "customer_type"], "customer_summary.csv")
customer.sort_values("net_sales_after_returns_est", ascending=False).head(25).to_csv(OUT / "top_25_customers.csv", index=False)

# Executive metric table.
net_sales = float(df["net_sales_after_returns_est"].sum())
profit = float(df["profit_est"].sum())
summary = pd.DataFrame([
    ["Raw order rows", source_row_count, "count"],
    ["Exact duplicate rows", exact_duplicate_count, "count"],
    ["Rows after exact duplicate removal", len(df), "count"],
    ["Unique orders", int(df["order_id"].nunique()), "count"],
    ["Unique order lines after deduplication", int(df["order_line_id"].nunique()), "count"],
    ["Gross sales", float(df["gross_sales"].sum()), "currency units"],
    ["Discount amount", float(df["discount_amount"].sum()), "currency units"],
    ["Net sales before returns", float(df["net_sales_pre_returns"].sum()), "currency units"],
    ["Estimated return value", float(df["return_value_est"].sum()), "currency units"],
    ["Estimated net sales after returns", net_sales, "currency units"],
    ["Estimated COGS after returns", float(df["cogs_net_units_est"].sum()), "currency units"],
    ["Estimated profit", profit, "currency units"],
    ["Estimated profit margin", profit / net_sales if net_sales else np.nan, "ratio"],
    ["Units ordered", float(df["quantity"].sum()), "units"],
    ["Units returned", float(df["return_units"].sum()), "units"],
    ["Unit return rate", float(df["return_units"].sum() / df["quantity"].sum()), "ratio"],
    ["Average line discount", float(df["discount_pct"].mean()), "ratio"],
], columns=["metric", "value", "unit"])
summary.to_csv(OUT / "executive_summary.csv", index=False)

# Automated data-quality checks. These validate conditions; issue counts are not
# silently edited beyond the documented exact duplicate removal.
checks = []
def add_check(name, actual, expected, status, note=""):
    checks.append({"check": name, "actual": actual, "expected": expected, "status": status, "note": note})

add_check("Raw rows", source_row_count, 30060, "PASS" if source_row_count == 30060 else "REVIEW", "Expected synthetic baseline row count")
add_check("Exact duplicate rows", exact_duplicate_count, 60, "PASS" if exact_duplicate_count == 60 else "REVIEW", "Only exact duplicates are removed")
add_check("Clean rows", int(len(df)), source_row_count-exact_duplicate_count, "PASS" if len(df)==source_row_count-exact_duplicate_count else "FAIL", "Analytical copy after deduplication")
add_check("Unique order_line_id after deduplication", int(df["order_line_id"].nunique()), int(len(df)), "PASS" if df["order_line_id"].is_unique else "FAIL", "Business key should be unique")
for col in ["order_id", "order_date", "product_id", "customer_id", "quantity", "unit_price", "discount_pct"]:
    missing = int(df[col].isna().sum())
    add_check(f"Missing required {col}", missing, 0, "PASS" if missing == 0 else "FAIL", "Required field")
add_check("Non-positive quantity rows", int((df["quantity"] <= 0).sum()), 0, "PASS" if (df["quantity"] > 0).all() else "FAIL", "Quantity must be positive")
add_check("Non-positive unit price rows", int((df["unit_price"] <= 0).sum()), 0, "PASS" if (df["unit_price"] > 0).all() else "FAIL", "Unit price must be positive")
add_check("Discount outside 0–25%", int((~df["discount_pct"].between(0, 0.25)).sum()), 0, "PASS" if df["discount_pct"].between(0,0.25).all() else "FAIL", "Synthetic business rule")
add_check("Return units below zero", int((df["return_units"] < 0).sum()), 0, "PASS" if (df["return_units"] >= 0).all() else "FAIL", "Returned units cannot be negative")
add_check("Return units exceed quantity", int((df["return_units"] > df["quantity"]).sum()), 0, "PASS" if (df["return_units"] <= df["quantity"]).all() else "FAIL", "Returned units cannot exceed line quantity")
add_check("Returned rows missing reason/date", int(((df["return_units"] > 0) & (df["return_reason"].isna() | df["return_date"].isna())).sum()), 0,
          "PASS" if not (((df["return_units"] > 0) & (df["return_reason"].isna() | df["return_date"].isna())).any()) else "REVIEW",
          "Conditional fields required when returns exist")
for col, dimname, key in [
    ("product_id", "products", "product_id"),
    ("customer_id", "customers", "customer_id"),
    ("distributor_id", "distributors", "distributor_id"),
    ("geography_id", "geography", "geography_id"),
    ("channel_id", "channels", "channel_id"),
]:
    unmatched = int((~df[col].isin(dims[dimname][key])).sum())
    add_check(f"Unmatched {col}", unmatched, 0, "PASS" if unmatched == 0 else "FAIL", "Foreign-key lookup to dimension")
add_check("Sales math consistency", float(abs((df["gross_sales"] - df["quantity"]*df["unit_price"]).sum())), 0.0, "PASS" if np.allclose(df["gross_sales"], df["quantity"]*df["unit_price"]) else "FAIL", "Gross sales = quantity × unit price")
add_check("Net sales reconciliation", float(abs(net_sales - (df["net_sales_pre_returns"].sum()-df["return_value_est"].sum()))), 0.0, "PASS" if np.isclose(net_sales, df["net_sales_pre_returns"].sum()-df["return_value_est"].sum()) else "FAIL", "Net sales after returns reconciliation")
checks_df = pd.DataFrame(checks)
checks_df.to_csv(OUT / "validation_checks.csv", index=False)
# Backwards-compatible short profile.
checks_df[["check", "actual", "status"]].rename(columns={"actual":"result"}).to_csv(OUT / "data_quality_checks.csv", index=False)

kpi_json = {row.metric: (int(row.value) if row.unit == "count" else float(row.value)) for row in summary.itertuples(index=False)}
kpi_json["data_notice"] = "Synthetic portfolio data; amounts are unspecified currency units; profit is estimated."
kpi_json["validation_pass_count"] = int((checks_df["status"] == "PASS").sum())
kpi_json["validation_review_count"] = int((checks_df["status"] == "REVIEW").sum())
kpi_json["validation_fail_count"] = int((checks_df["status"] == "FAIL").sum())
(OUT / "kpi_summary.json").write_text(json.dumps(kpi_json, indent=2), encoding="utf-8")

# Console output helps the learner see key results immediately.
print("Analysis complete. Outputs were refreshed from the bundled synthetic source data.")
print(f"Raw rows={source_row_count:,}; exact duplicates={exact_duplicate_count:,}; clean lines={len(df):,}; unique orders={df['order_id'].nunique():,}")
print(f"Estimated net sales={net_sales:,.2f}; estimated profit={profit:,.2f}; estimated margin={profit/net_sales:.2%}; unit return rate={df['return_units'].sum()/df['quantity'].sum():.2%}")
print(f"Validation checks: {(checks_df['status']=='PASS').sum()} PASS, {(checks_df['status']=='REVIEW').sum()} REVIEW, {(checks_df['status']=='FAIL').sum()} FAIL")
print("Top 5 products by estimated profit:")
print(product.sort_values("profit_est", ascending=False)[["product_name", "net_sales_after_returns_est", "profit_est"]].head(5).to_string(index=False))
print("Bottom 5 products by estimated profit (not loss-making in this dataset):")
print(product.sort_values("profit_est")[["product_name", "net_sales_after_returns_est", "profit_est"]].head(5).to_string(index=False))
