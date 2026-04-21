from __future__ import annotations

from datetime import datetime

from ecommerce_analytics_platform.orchestration import build_bigquery_refresh_job, build_dbt_command

DEFAULT_ARGS = {
    "owner": "analytics-engineering",
    "depends_on_past": False,
    "start_date": datetime(2026, 1, 1),
}

DAG_METADATA = {
    "dag_id": "ecommerce_analytics_daily",
    "schedule": "0 6 * * *",
    "catchup": False,
    "default_args": DEFAULT_ARGS,
}

TASK_PAYLOADS = {
    "refresh_kpi_table": build_bigquery_refresh_job(dry_run=True),
    "run_dbt_build": build_dbt_command(select="tag:daily", full_refresh=False),
}
