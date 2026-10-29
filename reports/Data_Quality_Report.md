# Data Quality Report

**Data provenance:** fictional company and synthetic records. No external/public or employer dataset is used.

## Row-count reconciliation

- **Raw rows** — actual: `30060.0`; expected/rule: `30060.0`; status: **PASS**. Expected synthetic baseline row count
- **Exact duplicate rows** — actual: `60.0`; expected/rule: `60.0`; status: **PASS**. Only exact duplicates are removed
- **Clean rows** — actual: `30000.0`; expected/rule: `30000.0`; status: **PASS**. Analytical copy after deduplication
- **Unique order_line_id after deduplication** — actual: `30000.0`; expected/rule: `30000.0`; status: **PASS**. Business key should be unique
- **Missing required order_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Required field
- **Missing required order_date** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Required field
- **Missing required product_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Required field
- **Missing required customer_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Required field
- **Missing required quantity** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Required field
- **Missing required unit_price** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Required field
- **Missing required discount_pct** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Required field
- **Non-positive quantity rows** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Quantity must be positive
- **Non-positive unit price rows** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Unit price must be positive
- **Discount outside 0–25%** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Synthetic business rule
- **Return units below zero** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Returned units cannot be negative
- **Return units exceed quantity** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Returned units cannot exceed line quantity
- **Returned rows missing reason/date** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Conditional fields required when returns exist
- **Unmatched product_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Foreign-key lookup to dimension
- **Unmatched customer_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Foreign-key lookup to dimension
- **Unmatched distributor_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Foreign-key lookup to dimension
- **Unmatched geography_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Foreign-key lookup to dimension
- **Unmatched channel_id** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Foreign-key lookup to dimension
- **Sales math consistency** — actual: `0.0`; expected/rule: `0.0`; status: **PASS**. Gross sales = quantity × unit price
- **Net sales reconciliation** — actual: `7.450580596923828e-09`; expected/rule: `0.0`; status: **PASS**. Net sales after returns reconciliation

## Detailed data-quality summary

| Check | Result | Status |
|---|---:|---|
| Raw rows | 30060.0 | PASS |
| Exact duplicate rows | 60.0 | PASS |
| Clean rows | 30000.0 | PASS |
| Unique order_line_id after deduplication | 30000.0 | PASS |
| Missing required order_id | 0.0 | PASS |
| Missing required order_date | 0.0 | PASS |
| Missing required product_id | 0.0 | PASS |
| Missing required customer_id | 0.0 | PASS |
| Missing required quantity | 0.0 | PASS |
| Missing required unit_price | 0.0 | PASS |
| Missing required discount_pct | 0.0 | PASS |
| Non-positive quantity rows | 0.0 | PASS |
| Non-positive unit price rows | 0.0 | PASS |
| Discount outside 0–25% | 0.0 | PASS |
| Return units below zero | 0.0 | PASS |
| Return units exceed quantity | 0.0 | PASS |
| Returned rows missing reason/date | 0.0 | PASS |
| Unmatched product_id | 0.0 | PASS |
| Unmatched customer_id | 0.0 | PASS |
| Unmatched distributor_id | 0.0 | PASS |
| Unmatched geography_id | 0.0 | PASS |
| Unmatched channel_id | 0.0 | PASS |
| Sales math consistency | 0.0 | PASS |
| Net sales reconciliation | 7.450580596923828e-09 | PASS |

## Cleaning decisions

- Source data remains in `data/orders_raw.csv` and is not overwritten by the Python analysis.
- Exactly duplicated transaction rows are dropped from the analytical copy only.
- Date fields are parsed; required fields, positive quantity and price, discount bounds, returned-unit bounds and dimension join coverage are validated.
- Missing business details are not guessed or imputed; a validation failure should be reviewed instead.

## Result

The packaged Python run records **24 PASS, 0 REVIEW, 0 FAIL** in `outputs/validation_checks.csv`. See `docs/Methodology.md` for formula assumptions and limits.

## Limitations

- The validation checks confirm internal consistency of the synthetic data and the stated formulas; they do not validate real financial accounting.
- MySQL execution, Excel Desktop formula recalculation and Power BI Desktop interaction testing require manual verification.