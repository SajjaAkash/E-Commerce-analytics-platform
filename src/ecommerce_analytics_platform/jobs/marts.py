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
    sessions: list[dict[str, object]],
) -> list[dict[str, object]]:
    customer_index = {customer["customer_id"]: customer for customer in customers}
    product_index = {product["product_id"]: product for product in products}
    sessions_by_customer: dict[str, list[dict[str, object]]] = defaultdict(list)
    sessions_by_id = {str(session["session_id"]): session for session in sessions}
    for session in sessions:
        sessions_by_customer[str(session["customer_id"])].append(session)
    for session_list in sessions_by_customer.values():
        session_list.sort(key=lambda row: str(row["session_started_at"]))
    facts = []
    for order in orders:
        customer = customer_index[order["customer_id"]]
        product = product_index[order["product_id"]]
        customer_sessions = sessions_by_customer.get(str(order["customer_id"]), [])
        first_touch = customer_sessions[0]["channel"] if customer_sessions else order["channel"]
        order_session = sessions_by_id.get(str(order["session_id"]), {})
        facts.append(
            {
                "order_id": order["order_id"],
                "order_date": order["order_date"],
                "customer_id": order["customer_id"],
                "segment": customer["segment"],
                "channel": order["channel"],
                "first_touch_channel": first_touch,
                "last_touch_channel": order_session.get("channel", order["channel"]),
                "product_id": order["product_id"],
                "product_name": product["product_name"],
                "category": product["category"],
                "units": order["units"],
                "order_status": order.get("order_status", "completed"),
                "gross_revenue": order["gross_revenue"],
                "discount_amount": order["discount_amount"],
                "refund_amount": order.get("refund_amount", 0.0),
                "net_revenue": order["net_revenue"],
                "realized_revenue": order.get("realized_revenue", order["net_revenue"]),
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
        realized_revenue = round(
            sum(float(order["realized_revenue"]) for order in daily_orders), 2
        )
        average_order_value = round(realized_revenue / orders_count, 2) if orders_count else 0.0
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
                net_revenue=realized_revenue,
                average_order_value=average_order_value,
                conversion_rate=conversion_rate,
                repeat_customer_rate=repeat_rate,
            )
        )
    return metrics


def build_attribution_summary(fact_orders: list[dict[str, object]]) -> list[dict[str, object]]:
    by_channel: dict[str, dict[str, object]] = {}
    for order in fact_orders:
        channel = str(order["last_touch_channel"])
        current = by_channel.setdefault(
            channel,
            {"channel": channel, "orders": 0, "realized_revenue": 0.0, "refund_amount": 0.0},
        )
        current["orders"] += 1
        current["realized_revenue"] = round(
            float(current["realized_revenue"]) + float(order["realized_revenue"]), 2
        )
        current["refund_amount"] = round(
            float(current["refund_amount"]) + float(order["refund_amount"]), 2
        )
    return sorted(by_channel.values(), key=lambda row: str(row["channel"]))


def build_customer_retention(
    fact_orders: list[dict[str, object]],
    customers: list[dict[str, object]],
) -> list[dict[str, object]]:
    first_order_by_customer: dict[str, str] = {}
    order_count_by_customer: dict[str, int] = defaultdict(int)
    for order in sorted(fact_orders, key=lambda row: str(row["order_date"])):
        customer_id = str(order["customer_id"])
        order_count_by_customer[customer_id] += 1
        first_order_by_customer.setdefault(customer_id, str(order["order_date"]))

    retention_rows = []
    for customer in customers:
        customer_id = str(customer["customer_id"])
        cohort_month = first_order_by_customer.get(customer_id, str(customer["signup_date"])[:7])
        repeat_flag = order_count_by_customer.get(customer_id, 0) > 1
        retention_rows.append(
            {
                "customer_id": customer_id,
                "cohort_month": cohort_month[:7],
                "orders_count": order_count_by_customer.get(customer_id, 0),
                "retained_customer": repeat_flag,
            }
        )
    return retention_rows
