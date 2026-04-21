from ecommerce_analytics_platform.jobs.quality_checks import run_quality_suite


def test_run_quality_suite_passes_for_valid_records() -> None:
    results = run_quality_suite(
        customers=[{"customer_id": "C1"}],
        products=[{"list_price": 5.0}],
        orders=[{"order_id": "O1", "customer_id": "C1"}],
        sessions=[{"event_date": "2026-01-01"}],
    )
    assert all(result.passed for result in results)
