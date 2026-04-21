from __future__ import annotations

from ecommerce_analytics_platform.config import settings


def build_bigquery_refresh_job(
    report_date: str | None = None, dry_run: bool = True
) -> dict[str, object]:
    metric_date = report_date or settings.platform.demo_report_date
    analytics_table = (
        f"{settings.platform.google_cloud_project}."
        f"{settings.platform.bigquery_analytics_dataset}."
        f"{settings.platform.bigquery_kpi_table}"
    )
    query = (
        "DECLARE report_date DATE DEFAULT DATE(@report_date); "
        f"CREATE OR REPLACE TABLE `{analytics_table}` AS "
        "SELECT * FROM UNNEST([STRUCT(report_date AS metric_date)]);"
    )
    return {
        "configuration": {
            "query": {
                "query": query,
                "useLegacySql": False,
                "parameterMode": "NAMED",
                "queryParameters": [
                    {
                        "name": "report_date",
                        "parameterType": {"type": "DATE"},
                        "parameterValue": {"value": metric_date},
                    }
                ],
            }
        },
        "jobReference": {"projectId": settings.platform.google_cloud_project},
        "labels": {
            "pipeline": "ecommerce_analytics",
            "mode": "dry_run" if dry_run else "execute",
        },
    }


def build_dbt_command(select: str = "tag:daily", full_refresh: bool = False) -> list[str]:
    command = [
        "dbt",
        "build",
        "--project-dir",
        "dbt",
        "--profiles-dir",
        settings.platform.dbt_profile_dir,
        "--target",
        settings.platform.dbt_target,
        "--select",
        select,
    ]
    if full_refresh:
        command.append("--full-refresh")
    return command
