from __future__ import annotations

from pathlib import Path

from ecommerce_analytics_platform.config import settings
from ecommerce_analytics_platform.io_utils import read_json_file


def build_dashboard_payload(
    fact_orders: list[dict[str, object]],
    kpi_metrics: list[dict[str, object]],
    quality_results: list[dict[str, object]],
) -> dict[str, object]:
    latest_kpi = kpi_metrics[-1] if kpi_metrics else {}
    revenue_by_category: dict[str, float] = {}
    for order in fact_orders:
        category = str(order["category"])
        revenue_by_category[category] = revenue_by_category.get(category, 0.0) + float(
            order["net_revenue"]
        )

    return {
        "headline_metrics": {
            "net_revenue": float(latest_kpi.get("net_revenue", 0.0)),
            "orders": int(latest_kpi.get("orders", len(fact_orders))),
            "average_order_value": float(latest_kpi.get("average_order_value", 0.0)),
            "conversion_rate": float(latest_kpi.get("conversion_rate", 0.0)),
        },
        "revenue_by_category": revenue_by_category,
        "kpi_timeseries": kpi_metrics,
        "orders": fact_orders,
        "quality_results": quality_results,
    }


def load_dashboard_payload(base_dir: str | Path | None = None) -> dict[str, object] | None:
    root = Path(base_dir or settings.platform.local_data_dir) / "demo_output"
    mart_path = root / "mart" / "fact_orders.json"
    kpi_path = root / "mart" / "kpi_daily_overview.json"
    quality_path = root / "quality" / "quality_results.json"
    if not mart_path.exists() or not kpi_path.exists() or not quality_path.exists():
        return None
    return build_dashboard_payload(
        read_json_file(mart_path),
        read_json_file(kpi_path),
        read_json_file(quality_path),
    )
