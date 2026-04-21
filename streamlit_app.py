from __future__ import annotations

import streamlit as st

from ecommerce_analytics_platform.dashboard import (
    build_dashboard_payload,
    load_dashboard_payload,
)

SAMPLE_FACTS = [
    {
        "order_id": "O1001",
        "order_date": "2026-04-18",
        "customer_id": "C101",
        "segment": "repeat",
        "channel": "paid_search",
        "product_id": "P100",
        "product_name": "AeroFit Running Shoes",
        "category": "Footwear",
        "units": 1,
        "gross_revenue": 128.0,
        "discount_amount": 12.0,
        "net_revenue": 116.0,
        "session_id": "S1001",
    },
    {
        "order_id": "O1002",
        "order_date": "2026-04-18",
        "customer_id": "C102",
        "segment": "new",
        "channel": "email",
        "product_id": "P102",
        "product_name": "Trail Hydration Pack",
        "category": "Accessories",
        "units": 2,
        "gross_revenue": 180.0,
        "discount_amount": 20.0,
        "net_revenue": 160.0,
        "session_id": "S1002",
    },
]

SAMPLE_KPIS = [
    {
        "metric_date": "2026-04-18",
        "orders": 2,
        "customers": 2,
        "net_revenue": 276.0,
        "average_order_value": 138.0,
        "conversion_rate": 0.095,
        "repeat_customer_rate": 0.5,
    }
]

SAMPLE_QUALITY = [
    {
        "rule_name": "orders_have_customer_keys",
        "passed": True,
        "detail": "All orders map to customers.",
    },
    {
        "rule_name": "products_have_positive_price",
        "passed": True,
        "detail": "No non-positive list prices found.",
    },
    {
        "rule_name": "sessions_have_dates",
        "passed": True,
        "detail": "All session rows include event dates.",
    },
]


def main() -> None:
    st.set_page_config(page_title="E-Commerce Analytics Platform", layout="wide")
    payload = load_dashboard_payload()
    if payload is None:
        payload = build_dashboard_payload(SAMPLE_FACTS, SAMPLE_KPIS, SAMPLE_QUALITY)
        st.info(
            "Showing bundled sample data. "
            "Run `python -m ecommerce_analytics_platform.demo_pipeline` "
            "to generate local analytics outputs for the dashboard."
        )
    else:
        st.success("Loaded dashboard data from local demo pipeline outputs.")

    metrics = payload["headline_metrics"]
    st.title("E-Commerce Analytics KPI Dashboard")
    st.caption("Governed business metrics delivered through BigQuery, dbt, and Streamlit patterns.")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Net Revenue", f"${metrics['net_revenue']:.2f}")
    col2.metric("Orders", metrics["orders"])
    col3.metric("AOV", f"${metrics['average_order_value']:.2f}")
    col4.metric("Conversion Rate", f"{metrics['conversion_rate'] * 100:.1f}%")

    st.subheader("Revenue by Category")
    st.bar_chart(payload["revenue_by_category"])

    st.subheader("KPI Trend")
    st.line_chart(payload["kpi_timeseries"], x="metric_date")

    st.subheader("Order Detail")
    st.dataframe(payload["orders"], use_container_width=True)

    st.subheader("Quality Checks")
    st.dataframe(payload["quality_results"], use_container_width=True)


if __name__ == "__main__":
    main()
