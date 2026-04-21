from __future__ import annotations

from datetime import date, timedelta


def build_metric_contracts() -> list[dict[str, object]]:
    return [
        {
            "metric_name": "realized_revenue",
            "owner": "finance_analytics",
            "definition": "Net order revenue after discounts and refunds.",
            "consumer_group": "executive_reporting",
            "release_tier": "gold",
        },
        {
            "metric_name": "last_touch_revenue",
            "owner": "growth_analytics",
            "definition": "Revenue attributed to the final pre-conversion marketing touch.",
            "consumer_group": "performance_marketing",
            "release_tier": "gold",
        },
        {
            "metric_name": "retained_customer_rate",
            "owner": "lifecycle_analytics",
            "definition": "Share of customers with more than one completed order.",
            "consumer_group": "crm",
            "release_tier": "gold",
        },
    ]


def build_finance_marketing_reconciliation(
    kpi_metrics: list[dict[str, object]],
    attribution_summary: list[dict[str, object]],
) -> dict[str, object]:
    finance_revenue = round(sum(float(row.get("net_revenue", 0.0)) for row in kpi_metrics), 2)
    marketing_revenue = round(
        sum(float(row.get("realized_revenue", 0.0)) for row in attribution_summary), 2
    )
    variance = round(finance_revenue - marketing_revenue, 2)
    return {
        "finance_revenue": finance_revenue,
        "marketing_revenue": marketing_revenue,
        "variance": variance,
        "variance_status": "aligned" if abs(variance) < 0.01 else "investigate",
    }


def build_backfill_plan(
    start_date: str, end_date: str, step_days: int = 3
) -> list[dict[str, object]]:
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if end < start:
        raise ValueError("end_date must be on or after start_date")
    if step_days <= 0:
        raise ValueError("step_days must be positive")
    plan = []
    batch_id = 1
    current = start
    while current <= end:
        batch_end = min(current + timedelta(days=step_days - 1), end)
        plan.append(
            {
                "batch_id": batch_id,
                "window_start": current.isoformat(),
                "window_end": batch_end.isoformat(),
                "dbt_select": "tag:daily",
            }
        )
        batch_id += 1
        current = batch_end + timedelta(days=1)
    return plan
