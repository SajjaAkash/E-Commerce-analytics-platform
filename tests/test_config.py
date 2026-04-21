from ecommerce_analytics_platform.config import settings


def test_default_settings_present() -> None:
    assert settings.platform.google_cloud_project
    assert settings.platform.bigquery_analytics_dataset == "ecommerce_analytics"
