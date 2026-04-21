from __future__ import annotations

from collections.abc import Iterable


def stage_customers(customers: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    staged = []
    for customer in customers:
        orders_count = int(customer.get("orders_count", 0))
        staged.append(
            {
                "customer_id": customer["customer_id"],
                "email": str(customer["email"]).strip().lower(),
                "signup_date": customer["signup_date"],
                "country": customer["country"],
                "segment": "repeat" if orders_count > 1 else "new",
                "orders_count": orders_count,
                "lifetime_value": float(customer.get("lifetime_value", 0.0)),
            }
        )
    return staged


def stage_products(products: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "brand": product["brand"],
            "list_price": float(product["list_price"]),
            "inventory_status": product["inventory_status"],
        }
        for product in products
    ]


def stage_orders(orders: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    staged = []
    for order in orders:
        units = int(order["units"])
        unit_price = float(order["unit_price"])
        discount_amount = float(order.get("discount_amount", 0.0))
        gross_revenue = round(units * unit_price, 2)
        net_revenue = round(gross_revenue - discount_amount, 2)
        staged.append(
            {
                "order_id": order["order_id"],
                "order_date": order["order_date"],
                "customer_id": order["customer_id"],
                "product_id": order["product_id"],
                "session_id": order["session_id"],
                "channel": order["channel"],
                "units": units,
                "unit_price": unit_price,
                "gross_revenue": gross_revenue,
                "discount_amount": discount_amount,
                "net_revenue": net_revenue,
            }
        )
    return staged


def stage_sessions(sessions: Iterable[dict[str, object]]) -> list[dict[str, object]]:
    return [
        {
            "session_id": session["session_id"],
            "customer_id": session["customer_id"],
            "event_date": session["event_date"],
            "channel": session["channel"],
            "device_type": session["device_type"],
            "pageviews": int(session["pageviews"]),
            "converted": bool(session["converted"]),
        }
        for session in sessions
    ]
