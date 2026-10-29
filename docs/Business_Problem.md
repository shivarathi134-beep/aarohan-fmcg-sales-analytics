# Business Problem and Analysis Scope

## Scenario

Aarohan Consumer Products is a fictional FMCG company distributing packaged beverages, staples, home-care, personal-care and snacks products through multiple channels, distributors, states and regions.

## Business problem

Management wants a consistent view of sales, estimated profitability, discount patterns and return activity. The source export contains exact duplicate rows, product/customer/geography/channel keys, and transaction lines that roll up to order-level KPIs. A useful analysis must establish a defensible data grain and metric definitions before creating visuals.

## Questions to answer

1. What are gross sales, discounts, estimated return value, net sales, estimated COGS, estimated profit and weighted margin?
2. How are sales/profit moving by year and month?
3. Which products/categories contribute most/least to profit and margin?
4. Which regions/states and channels perform best by sales/profit/margin/return rate?
5. Which customer segments and customers contribute to net sales?
6. How do discount bands correlate with observed margin and profit?
7. What return reasons, products or channels deserve investigation?
8. Which metrics reconcile between independent outputs, and which tools still need execution verification?

## In scope

Python data cleaning/EDA and output generation; Excel KPI review and formulas; MySQL 8 schema and business-analysis query assets; Power BI model, DAX and interactive report build; validation documentation and interview preparation.

## Out of scope / unavailable in source

Actual inventory balances/stock-outs, shipments/delivery SLA, actual returns/refunds ledger, promotions with a control group, costs beyond unit cost, taxes, freight, payroll, overhead, and a specified currency. Predictive or causal claims are therefore not justified.
