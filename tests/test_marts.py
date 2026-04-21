from ecommerce_analytics_platform.jobs.marts import build_fact_orders, build_kpi_daily_overview


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
    )
    assert facts[0]["segment"] == "new"
    assert facts[0]["category"] == "Gear"


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
                "gross_revenue": 10.0,
                "discount_amount": 0.0,
                "net_revenue": 10.0,
                "session_id": "S1",
            }
        ],
        sessions=[
            {
                "session_id": "S1",
                "customer_id": "C1",
                "event_date": "2026-01-01",
                "channel": "email",
                "device_type": "desktop",
                "pageviews": 3,
                "converted": True,
            }
        ],
    )
    assert metrics[0].average_order_value == 10.0
    assert metrics[0].conversion_rate == 1.0
    assert metrics[0].repeat_customer_rate == 1.0
