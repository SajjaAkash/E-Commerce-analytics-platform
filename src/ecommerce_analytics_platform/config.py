from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PlatformSettings:
    google_cloud_project: str = os.getenv("GOOGLE_CLOUD_PROJECT", "ecommerce-analytics-dev")
    gcp_region: str = os.getenv("GCP_REGION", "us-central1")
    bigquery_raw_dataset: str = os.getenv("BIGQUERY_RAW_DATASET", "ecommerce_raw")
    bigquery_analytics_dataset: str = os.getenv("BIGQUERY_ANALYTICS_DATASET", "ecommerce_analytics")
    bigquery_kpi_table: str = os.getenv("BIGQUERY_KPI_TABLE", "kpi_daily_overview")
    dbt_target: str = os.getenv("DBT_TARGET", "dev")
    dbt_profile_dir: str = os.getenv("DBT_PROFILE_DIR", "./dbt")
    dbt_job_name: str = os.getenv("DBT_JOB_NAME", "ecommerce_analytics_daily")
    local_data_dir: str = os.getenv("LOCAL_DATA_DIR", "./data")
    demo_report_date: str = os.getenv("DEMO_REPORT_DATE", "2026-04-20")

    @property
    def local_data_path(self) -> Path:
        return Path(self.local_data_dir)


@dataclass(frozen=True)
class Settings:
    platform: PlatformSettings = PlatformSettings()


settings = Settings()
