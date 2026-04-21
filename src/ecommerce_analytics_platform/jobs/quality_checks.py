from __future__ import annotations

from ecommerce_analytics_platform.models import QualityResult


def run_quality_suite(
    customers: list[dict[str, object]],
    products: list[dict[str, object]],
    orders: list[dict[str, object]],
    sessions: list[dict[str, object]],
) -> list[QualityResult]:
    customer_ids = {customer["customer_id"] for customer in customers}
    product_prices = [float(product["list_price"]) for product in products]
    orders_have_customer_keys = all(order["customer_id"] in customer_ids for order in orders)
    products_have_positive_price = all(price > 0 for price in product_prices)
    sessions_have_dates = all(bool(session.get("event_date")) for session in sessions)
    unique_order_ids = len({order["order_id"] for order in orders}) == len(orders)
    refunds_within_revenue = all(
        float(order["refund_amount"]) <= float(order["net_revenue"]) for order in orders
    )
    valid_order_statuses = all(
        str(order["order_status"]) in {"completed", "cancelled", "refunded"} for order in orders
    )

    return [
        QualityResult(
            rule_name="orders_have_customer_keys",
            passed=orders_have_customer_keys,
            detail="All orders map to valid customers."
            if orders_have_customer_keys
            else "Found orders without valid customers.",
        ),
        QualityResult(
            rule_name="products_have_positive_price",
            passed=products_have_positive_price,
            detail="All products have positive list price."
            if products_have_positive_price
            else "Found products with non-positive list price.",
        ),
        QualityResult(
            rule_name="sessions_have_dates",
            passed=sessions_have_dates,
            detail="All sessions include event dates."
            if sessions_have_dates
            else "Found sessions without event dates.",
        ),
        QualityResult(
            rule_name="order_ids_unique",
            passed=unique_order_ids,
            detail="Order identifiers are unique."
            if unique_order_ids
            else "Duplicate order identifiers detected.",
        ),
        QualityResult(
            rule_name="refunds_within_revenue",
            passed=refunds_within_revenue,
            detail="Refund amounts are bounded by booked revenue."
            if refunds_within_revenue
            else "Found refund amounts greater than booked revenue.",
        ),
        QualityResult(
            rule_name="order_statuses_valid",
            passed=valid_order_statuses,
            detail="All order statuses are within accepted values."
            if valid_order_statuses
            else "Found unsupported order statuses.",
        ),
    ]
