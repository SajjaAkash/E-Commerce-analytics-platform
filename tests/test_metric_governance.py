import pytest

from ecommerce_analytics_platform.metric_governance import (
    build_backfill_plan,
    build_finance_marketing_reconciliation,
    build_metric_contracts,
)


def test_build_metric_contracts_returns_named_metrics() -> None:
    contracts = build_metric_contracts()
    assert contracts[0]["metric_name"] == "realized_revenue"


def test_build_finance_marketing_reconciliation_flags_variance() -> None:
    reconciliation = build_finance_marketing_reconciliation(
        [{"net_revenue": 100.0}],
        [{"realized_revenue": 80.0}],
    )
    assert reconciliation["variance_status"] == "investigate"


def test_build_backfill_plan_validates_date_window() -> None:
    with pytest.raises(ValueError):
        build_backfill_plan("2026-04-20", "2026-04-18")
