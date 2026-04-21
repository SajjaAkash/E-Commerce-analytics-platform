from __future__ import annotations

from pathlib import Path

from ecommerce_analytics_platform.config import settings
from ecommerce_analytics_platform.io_utils import read_json_file


def build_dashboard_payload(
    fact_orders: list[dict[str, object]],
    kpi_metrics: list[dict[str, object]],
    quality_results: list[dict[str, object]],
    attribution_summary: list[dict[str, object]] | None = None,
    customer_retention: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    latest_kpi = kpi_metrics[-1] if kpi_metrics else {}
    revenue_by_category: dict[str, float] = {}
    for order in fact_orders:
        category = str(order["category"])
        revenue_by_category[category] = revenue_by_category.get(category, 0.0) + float(
            order["net_revenue"]
        )

    attribution_summary = attribution_summary or []
    customer_retention = customer_retention or []
    retained_customers = sum(
        1 for row in customer_retention if bool(row.get("retained_customer"))
    )
    total_refunds = round(
        sum(float(order.get("refund_amount", 0.0)) for order in fact_orders), 2
    )
    booked_revenue = sum(float(order.get("net_revenue", 0.0)) for order in fact_orders)
    refund_rate = round(
        total_refunds / max(booked_revenue, 1.0),
        4,
    )
    top_channel = (
        max(
            attribution_summary,
            key=lambda row: float(row.get("realized_revenue", 0.0)),
        )["channel"]
        if attribution_summary
        else "n/a"
    )
    cohort_summary: dict[str, dict[str, int]] = {}
    for row in customer_retention:
        cohort_month = str(row.get("cohort_month", "unknown"))
        current = cohort_summary.setdefault(
            cohort_month, {"cohort_month": cohort_month, "customers": 0, "retained": 0}
        )
        current["customers"] += 1
        current["retained"] += 1 if bool(row.get("retained_customer")) else 0

    return {
        "headline_metrics": {
            "net_revenue": float(latest_kpi.get("net_revenue", 0.0)),
            "orders": int(latest_kpi.get("orders", len(fact_orders))),
            "average_order_value": float(latest_kpi.get("average_order_value", 0.0)),
            "conversion_rate": float(latest_kpi.get("conversion_rate", 0.0)),
            "retained_customers": retained_customers,
            "refund_rate": refund_rate,
            "top_channel": top_channel,
        },
        "revenue_by_category": revenue_by_category,
        "kpi_timeseries": kpi_metrics,
        "attribution_summary": attribution_summary,
        "customer_retention": customer_retention,
        "cohort_summary": list(cohort_summary.values()),
        "orders": fact_orders,
        "quality_results": quality_results,
    }


def load_dashboard_payload(base_dir: str | Path | None = None) -> dict[str, object] | None:
    root = Path(base_dir or settings.platform.local_data_dir) / "demo_output"
    mart_path = root / "mart" / "fact_orders.json"
    kpi_path = root / "mart" / "kpi_daily_overview.json"
    attribution_path = root / "mart" / "attribution_summary.json"
    retention_path = root / "mart" / "customer_retention.json"
    quality_path = root / "quality" / "quality_results.json"
    if not mart_path.exists() or not kpi_path.exists() or not quality_path.exists():
        return None
    return build_dashboard_payload(
        read_json_file(mart_path),
        read_json_file(kpi_path),
        read_json_file(quality_path),
        read_json_file(attribution_path) if attribution_path.exists() else [],
        read_json_file(retention_path) if retention_path.exists() else [],
    )
