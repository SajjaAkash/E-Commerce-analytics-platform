from ecommerce_analytics_platform.dashboard import build_dashboard_payload


def test_build_dashboard_payload_shapes_metrics() -> None:
    payload = build_dashboard_payload(
        fact_orders=[
            {"category": "Gear", "net_revenue": 20.0},
            {"category": "Gear", "net_revenue": 10.0},
        ],
        kpi_metrics=[
            {
                "metric_date": "2026-01-01",
                "orders": 2,
                "customers": 2,
                "net_revenue": 30.0,
                "average_order_value": 15.0,
                "conversion_rate": 0.5,
                "repeat_customer_rate": 0.5,
            }
        ],
        attribution_summary=[{"channel": "email"}],
        customer_retention=[{"retained_customer": True, "cohort_month": "2026-01"}],
        governance_payload={
            "finance_marketing_reconciliation": {"variance_status": "aligned"},
            "metric_contracts": [],
            "backfill_plan": [],
        },
        quality_results=[{"rule_name": "rule", "passed": True, "detail": "ok"}],
    )
    assert payload["headline_metrics"]["orders"] == 2
    assert payload["revenue_by_category"]["Gear"] == 30.0
    assert payload["headline_metrics"]["retained_customers"] == 1
    assert payload["headline_metrics"]["variance_status"] == "aligned"
