from ecommerce_analytics_platform.jobs.marts import (
    build_attribution_summary,
    build_customer_retention,
    build_fact_orders,
    build_kpi_daily_overview,
)


def test_build_fact_orders_enriches_dimensions() -> None:
    facts = build_fact_orders(
        orders=[
            {
                "order_id": "O1",
                "order_date": "2026-01-01",
                "customer_id": "C1",
                "product_id": "P1",
                "session_id": "S1",
                "channel": "email",
                "units": 1,
                "gross_revenue": 10.0,
                "discount_amount": 0.0,
                "net_revenue": 10.0,
            }
        ],
        customers=[{"customer_id": "C1", "segment": "new"}],
        products=[{"product_id": "P1", "product_name": "Bottle", "category": "Gear"}],
        sessions=[
            {
                "session_id": "S1",
                "customer_id": "C1",
                "event_date": "2026-01-01",
                "session_started_at": "2026-01-01T10:00:00",
                "channel": "email",
                "campaign_name": "welcome",
                "device_type": "desktop",
                "pageviews": 3,
                "converted": True,
            }
        ],
    )
    assert facts[0]["segment"] == "new"
    assert facts[0]["category"] == "Gear"
    assert facts[0]["last_touch_channel"] == "email"


def test_build_kpi_daily_overview_calculates_metrics() -> None:
    metrics = build_kpi_daily_overview(
        fact_orders=[
            {
                "order_id": "O1",
                "order_date": "2026-01-01",
                "customer_id": "C1",
                "segment": "repeat",
                "channel": "email",
                "product_id": "P1",
                "product_name": "Bottle",
                "category": "Gear",
                "units": 1,
                "order_status": "completed",
                "gross_revenue": 10.0,
                "discount_amount": 0.0,
                "refund_amount": 0.0,
                "net_revenue": 10.0,
                "realized_revenue": 10.0,
                "first_touch_channel": "email",
                "last_touch_channel": "email",
                "session_id": "S1",
            }
        ],
        sessions=[
            {
                "session_id": "S1",
                "customer_id": "C1",
                "event_date": "2026-01-01",
                "session_started_at": "2026-01-01T10:00:00",
                "channel": "email",
                "campaign_name": "welcome",
                "device_type": "desktop",
                "pageviews": 3,
                "converted": True,
            }
        ],
    )
    assert metrics[0].average_order_value == 10.0
    assert metrics[0].conversion_rate == 1.0
    assert metrics[0].repeat_customer_rate == 1.0


def test_build_attribution_summary_groups_by_last_touch() -> None:
    summary = build_attribution_summary(
        [
            {"last_touch_channel": "email", "realized_revenue": 10.0, "refund_amount": 1.0},
            {"last_touch_channel": "email", "realized_revenue": 15.0, "refund_amount": 0.0},
        ]
    )
    assert summary[0]["orders"] == 2
    assert summary[0]["realized_revenue"] == 25.0


def test_build_customer_retention_marks_repeat_customers() -> None:
    retention = build_customer_retention(
        fact_orders=[
            {"customer_id": "C1", "order_date": "2026-01-01"},
            {"customer_id": "C1", "order_date": "2026-02-01"},
        ],
        customers=[{"customer_id": "C1", "signup_date": "2026-01-01"}],
    )
    assert retention[0]["retained_customer"] is True
