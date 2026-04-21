from ecommerce_analytics_platform.orchestration import (
    build_backfill_command,
    build_bigquery_refresh_job,
    build_dbt_command,
)


def test_build_bigquery_refresh_job_contains_named_parameter() -> None:
    payload = build_bigquery_refresh_job(report_date="2026-04-20", dry_run=True)
    params = payload["configuration"]["query"]["queryParameters"]
    assert params[0]["parameterValue"]["value"] == "2026-04-20"
    assert payload["labels"]["mode"] == "dry_run"


def test_build_dbt_command_respects_flags() -> None:
    command = build_dbt_command(select="tag:daily", full_refresh=True)
    assert command[:2] == ["dbt", "build"]
    assert "--full-refresh" in command


def test_build_backfill_command_returns_batches() -> None:
    payload = build_backfill_command("2026-04-18", "2026-04-20")
    assert payload["batches"][0]["batch_id"] == 1
