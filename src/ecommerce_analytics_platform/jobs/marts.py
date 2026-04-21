from __future__ import annotations

from collections import defaultdict

from ecommerce_analytics_platform.models import KpiMetric


def build_dim_customer(customers: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "customer_id": customer["customer_id"],
            "email": customer["email"],
            "country": customer["country"],
            "signup_date": customer["signup_date"],
            "segment": customer["segment"],
            "orders_count": customer["orders_count"],
            "lifetime_value": customer["lifetime_value"],
        }
        for customer in customers
    ]


def build_dim_product(products: list[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "brand": product["brand"],
            "list_price": product["list_price"],
            "inventory_status": product["inventory_status"],
        }
        for product in products
    ]


def build_fact_orders(
    orders: list[dict[str, object]],
    customers: list[dict[str, object]],
    products: list[dict[str, object]],
) -> list[dict[str, object]]:
    customer_index = {customer["customer_id"]: customer for customer in customers}
    product_index = {product["product_id"]: product for product in products}
    facts = []
    for order in orders:
        customer = customer_index[order["customer_id"]]
        product = product_index[order["product_id"]]
        facts.append(
            {
                "order_id": order["order_id"],
                "order_date": order["order_date"],
                "customer_id": order["customer_id"],
                "segment": customer["segment"],
                "channel": order["channel"],
                "product_id": order["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "units": order["units"],
                "gross_revenue": order["gross_revenue"],
                "discount_amount": order["discount_amount"],
                "net_revenue": order["net_revenue"],
                "session_id": order["session_id"],
            }
        )
    return facts


def build_kpi_daily_overview(
    fact_orders: list[dict[str, object]],
    sessions: list[dict[str, object]],
) -> list[KpiMetric]:
    sessions_by_date: dict[str, list[dict[str, object]]] = defaultdict(list)
    for session in sessions:
        sessions_by_date[str(session["event_date"])].append(session)

    orders_by_date: dict[str, list[dict[str, object]]] = defaultdict(list)
    for order in fact_orders:
        orders_by_date[str(order["order_date"])].append(order)

    metrics: list[KpiMetric] = []
    for metric_date in sorted(orders_by_date):
        daily_orders = orders_by_date[metric_date]
        daily_sessions = sessions_by_date.get(metric_date, [])
        unique_customers = {order["customer_id"] for order in daily_orders}
        repeat_customers = {
            order["customer_id"] for order in daily_orders if str(order["segment"]) == "repeat"
        }
        orders_count = len(daily_orders)
        net_revenue = round(sum(float(order["net_revenue"]) for order in daily_orders), 2)
        average_order_value = round(net_revenue / orders_count, 2) if orders_count else 0.0
        converted_sessions = sum(1 for session in daily_sessions if bool(session["converted"]))
        total_sessions = len(daily_sessions)
        conversion_rate = round(converted_sessions / total_sessions, 4) if total_sessions else 0.0
        repeat_rate = (
            round(len(repeat_customers) / len(unique_customers), 4)
            if unique_customers
            else 0.0
        )
        metrics.append(
            KpiMetric(
                metric_date=metric_date,
                orders=orders_count,
                customers=len(unique_customers),
                net_revenue=net_revenue,
                average_order_value=average_order_value,
                conversion_rate=conversion_rate,
                repeat_customer_rate=repeat_rate,
            )
        )
    return metrics
