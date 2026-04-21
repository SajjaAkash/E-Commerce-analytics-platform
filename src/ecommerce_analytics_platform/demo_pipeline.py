from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from ecommerce_analytics_platform.config import settings
from ecommerce_analytics_platform.io_utils import read_json_file, write_json_file
from ecommerce_analytics_platform.jobs.marts import (
    build_attribution_summary,
    build_customer_retention,
    build_dim_customer,
    build_dim_product,
    build_fact_orders,
    build_kpi_daily_overview,
)
from ecommerce_analytics_platform.jobs.quality_checks import run_quality_suite
from ecommerce_analytics_platform.jobs.stage_transform import (
    stage_customers,
    stage_orders,
    stage_products,
    stage_sessions,
)


def _sample_dir(base_dir: str | Path | None = None) -> Path:
    root = Path(base_dir or settings.platform.local_data_dir)
    return root / "sample" / "raw"


def _output_dir(base_dir: str | Path | None = None) -> Path:
    root = Path(base_dir or settings.platform.local_data_dir)
    return root / "demo_output"


def run_demo_pipeline(base_dir: str | Path | None = None) -> dict[str, object]:
    sample_dir = _sample_dir(base_dir)
    output_dir = _output_dir(base_dir)

    raw_customers = read_json_file(sample_dir / "customers.json")
    raw_products = read_json_file(sample_dir / "products.json")
    raw_orders = read_json_file(sample_dir / "orders.json")
    raw_sessions = read_json_file(sample_dir / "sessions.json")

    staged_customers = stage_customers(raw_customers)
    staged_products = stage_products(raw_products)
    staged_orders = stage_orders(raw_orders)
    staged_sessions = stage_sessions(raw_sessions)

    dim_customer = build_dim_customer(staged_customers)
    dim_product = build_dim_product(staged_products)
    fact_orders = build_fact_orders(
        staged_orders, staged_customers, staged_products, staged_sessions
    )
    kpi_metrics = [
        asdict(metric)
        for metric in build_kpi_daily_overview(fact_orders, staged_sessions)
    ]
    attribution_summary = build_attribution_summary(fact_orders)
    customer_retention = build_customer_retention(fact_orders, staged_customers)
    quality_results = [
        asdict(result)
        for result in run_quality_suite(
            customers=staged_customers,
            products=staged_products,
            orders=staged_orders,
            sessions=staged_sessions,
        )
    ]

    write_json_file(output_dir / "stage" / "customers.json", staged_customers)
    write_json_file(output_dir / "stage" / "products.json", staged_products)
    write_json_file(output_dir / "stage" / "orders.json", staged_orders)
    write_json_file(output_dir / "stage" / "sessions.json", staged_sessions)
    write_json_file(output_dir / "mart" / "dim_customer.json", dim_customer)
    write_json_file(output_dir / "mart" / "dim_product.json", dim_product)
    write_json_file(output_dir / "mart" / "fact_orders.json", fact_orders)
    write_json_file(output_dir / "mart" / "kpi_daily_overview.json", kpi_metrics)
    write_json_file(output_dir / "mart" / "attribution_summary.json", attribution_summary)
    write_json_file(output_dir / "mart" / "customer_retention.json", customer_retention)
    write_json_file(output_dir / "quality" / "quality_results.json", quality_results)

    return {
        "staged_customers": staged_customers,
        "staged_products": staged_products,
        "staged_orders": staged_orders,
        "staged_sessions": staged_sessions,
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "fact_orders": fact_orders,
        "kpi_metrics": kpi_metrics,
        "attribution_summary": attribution_summary,
        "customer_retention": customer_retention,
        "quality_results": quality_results,
        "output_dir": str(output_dir),
    }


if __name__ == "__main__":
    result = run_demo_pipeline()
    print(f"Demo pipeline complete. Outputs written to {result['output_dir']}")
