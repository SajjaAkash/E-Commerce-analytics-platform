# Architecture Notes

## Platform Goals

This project models an ecommerce analytics delivery stack that supports:

- governed KPI publication for business reporting,
- reusable customer and product marts for downstream analysis,
- scheduled refreshes with predictable warehouse behavior,
- stakeholder access through a lightweight Streamlit analytics interface.

## Data Flow

1. Operational exports land as raw ecommerce entities such as customers, products, orders, and sessions.
2. BigQuery raw datasets retain source-grain history.
3. `dbt` staging models standardize naming, typing, and revenue calculations.
4. `dbt` mart models publish conformed dimensions and KPI tables for shared consumption.
5. Scheduled orchestration triggers warehouse refreshes and downstream dashboard availability checks.
6. Streamlit reads curated outputs to expose revenue, conversion, and retention trends.

## Key Analytical Entities

- `dim_customer`: signup cohort, geography, segment, and lifetime value context.
- `dim_product`: category, brand, pricing, and inventory status.
- `fact_orders`: order-level revenue activity with customer, product, session, and marketing channel context.
- `kpi_daily_overview`: headline revenue and conversion metrics aligned to business reporting.

## Why This Maps Well To The Resume Entry

- GCP is represented through BigQuery-first modeling and deployable infrastructure assets.
- BigQuery patterns are visible in the SQL model design and scheduled refresh payloads.
- `dbt` centralizes business logic in reusable staging and mart transformations.
- Streamlit provides the self-serve delivery surface for non-engineering stakeholders.
