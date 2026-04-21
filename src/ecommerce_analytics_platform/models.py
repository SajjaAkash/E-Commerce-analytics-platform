from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class QualityResult:
    rule_name: str
    passed: bool
    detail: str


@dataclass(frozen=True)
class KpiMetric:
    metric_date: str
    orders: int
    customers: int
    net_revenue: float
    average_order_value: float
    conversion_rate: float
    repeat_customer_rate: float
