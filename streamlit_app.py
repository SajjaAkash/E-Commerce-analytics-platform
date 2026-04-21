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
        "order_status": "completed",
        "gross_revenue": 128.0,
        "discount_amount": 12.0,
        "refund_amount": 0.0,
        "net_revenue": 116.0,
        "realized_revenue": 116.0,
        "first_touch_channel": "organic_search",
        "last_touch_channel": "paid_search",
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
        "order_status": "refunded",
        "gross_revenue": 180.0,
        "discount_amount": 20.0,
        "refund_amount": 40.0,
        "net_revenue": 160.0,
        "realized_revenue": 120.0,
        "first_touch_channel": "email",
        "last_touch_channel": "email",
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

SAMPLE_ATTRIBUTION = [
    {"channel": "email", "orders": 1, "realized_revenue": 120.0, "refund_amount": 40.0},
    {"channel": "paid_search", "orders": 1, "realized_revenue": 116.0, "refund_amount": 0.0},
]

SAMPLE_RETENTION = [
    {
        "customer_id": "C101",
        "cohort_month": "2026-04",
        "orders_count": 2,
        "retained_customer": True,
    },
    {
        "customer_id": "C102",
        "cohort_month": "2026-04",
        "orders_count": 1,
        "retained_customer": False,
    },
]

SAMPLE_GOVERNANCE = {
    "metric_contracts": [
        {"metric_name": "realized_revenue", "owner": "finance_analytics", "release_tier": "gold"}
    ],
    "finance_marketing_reconciliation": {
        "finance_revenue": 276.0,
        "marketing_revenue": 236.0,
        "variance": 40.0,
        "variance_status": "investigate",
    },
    "backfill_plan": [{"batch_id": 1, "window_start": "2026-04-18", "window_end": "2026-04-20"}],
}


def main() -> None:
    st.set_page_config(page_title="Revenue Signal Studio", layout="wide")
    payload = load_dashboard_payload()
    if payload is None:
        payload = build_dashboard_payload(
            SAMPLE_FACTS,
            SAMPLE_KPIS,
            SAMPLE_QUALITY,
            SAMPLE_ATTRIBUTION,
            SAMPLE_RETENTION,
            SAMPLE_GOVERNANCE,
        )
        st.info(
            "Showing bundled sample data. "
            "Run `python -m ecommerce_analytics_platform.demo_pipeline` "
            "to generate local analytics outputs for the dashboard."
        )
    else:
        st.success("Loaded dashboard data from local demo pipeline outputs.")

    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(255, 125, 0, 0.14), transparent 24%),
                radial-gradient(circle at top right, rgba(34, 165, 114, 0.12), transparent 22%),
                linear-gradient(180deg, #fff7ef 0%, #fffdf9 100%);
        }
        .hero {
            background: linear-gradient(135deg, #ff8c42 0%, #f15b2a 50%, #0f6c5c 100%);
            color: white;
            border-radius: 22px;
            padding: 1.6rem 1.8rem;
            margin-bottom: 1rem;
            box-shadow: 0 18px 40px rgba(211, 96, 40, 0.18);
        }
        .glass {
            background: rgba(255,255,255,0.84);
            border: 1px solid rgba(241, 91, 42, 0.10);
            border-radius: 18px;
            padding: 1rem 1.1rem;
            box-shadow: 0 10px 32px rgba(211, 96, 40, 0.08);
        }
        </style>
        <div class="hero">
            <h1 style="margin:0;">Revenue Signal Studio</h1>
            <p style="margin:0.4rem 0 0 0; max-width: 48rem;">
                A commercial analytics cockpit for revenue quality, channel attribution,
                and cohort retention rather than a generic BI dashboard.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metrics = payload["headline_metrics"]

    selected_statuses = st.sidebar.multiselect(
        "Order Status Filter",
        sorted({str(order["order_status"]) for order in payload["orders"]}),
        default=sorted({str(order["order_status"]) for order in payload["orders"]}),
    )
    filtered_orders = [
        order for order in payload["orders"] if str(order["order_status"]) in selected_statuses
    ]
    filtered_revenue_by_category: dict[str, float] = {}
    for order in filtered_orders:
        category = str(order["category"])
        filtered_revenue_by_category[category] = (
            filtered_revenue_by_category.get(category, 0.0)
            + float(order["realized_revenue"])
        )

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    metric_col1.metric("Realized Revenue", f"${metrics['net_revenue']:.2f}")
    metric_col2.metric("Orders", len(filtered_orders))
    metric_col3.metric("Refund Rate", f"{metrics['refund_rate'] * 100:.1f}%")
    metric_col4.metric("Top Channel", metrics["top_channel"])
    if metrics["variance_status"] != "aligned":
        st.warning(
            "Finance and marketing views are not fully aligned for the current batch. "
            "Review reconciliation before publication."
        )

    spotlight, controls = st.columns([1.35, 1])
    with spotlight:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Revenue by Category")
        st.bar_chart(filtered_revenue_by_category)
        st.subheader("KPI Trend")
        st.line_chart(payload["kpi_timeseries"], x="metric_date")
        st.markdown("</div>", unsafe_allow_html=True)
    with controls:
        st.markdown('<div class="glass">', unsafe_allow_html=True)
        st.subheader("Attribution Table")
        st.dataframe(payload["attribution_summary"], use_container_width=True, hide_index=True)
        st.subheader("Cohort Summary")
        st.dataframe(payload["cohort_summary"], use_container_width=True, hide_index=True)
        st.markdown("</div>", unsafe_allow_html=True)

    detail_tab, retention_tab, quality_tab, governance_tab = st.tabs(
        ["Order Ledger", "Retention Detail", "Quality Guardrails", "Metric Governance"]
    )
    with detail_tab:
        st.dataframe(filtered_orders, use_container_width=True)
    with retention_tab:
        st.dataframe(payload["customer_retention"], use_container_width=True)
    with quality_tab:
        st.dataframe(payload["quality_results"], use_container_width=True)
    with governance_tab:
        st.subheader("Metric Contracts")
        st.dataframe(payload["governance"]["metric_contracts"], use_container_width=True)
        st.subheader("Finance vs Marketing Reconciliation")
        st.json(payload["governance"]["finance_marketing_reconciliation"])
        st.subheader("Backfill Plan")
        st.dataframe(payload["governance"]["backfill_plan"], use_container_width=True)


if __name__ == "__main__":
    main()
