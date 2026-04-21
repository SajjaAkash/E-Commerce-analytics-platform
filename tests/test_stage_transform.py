from ecommerce_analytics_platform.jobs.stage_transform import (
    stage_customers,
    stage_orders,
)


def test_stage_customers_assigns_segment() -> None:
    staged = stage_customers(
        [
            {
                "customer_id": "C1",
                "email": "USER@EXAMPLE.COM",
                "signup_date": "2026-01-01",
                "country": "US",
                "orders_count": 2,
                "lifetime_value": 22.0,
            }
        ]
    )
    assert staged[0]["segment"] == "repeat"
    assert staged[0]["email"] == "user@example.com"


def test_stage_orders_calculates_revenue() -> None:
    staged = stage_orders(
        [
            {
                "order_id": "O1",
                "order_date": "2026-01-01",
                "customer_id": "C1",
                "product_id": "P1",
                "session_id": "S1",
                "channel": "email",
                "units": 2,
                "unit_price": 10,
                "discount_amount": 3,
            }
        ]
    )
    assert staged[0]["gross_revenue"] == 20.0
    assert staged[0]["net_revenue"] == 17.0
