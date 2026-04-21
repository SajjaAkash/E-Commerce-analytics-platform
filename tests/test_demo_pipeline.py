from ecommerce_analytics_platform.demo_pipeline import run_demo_pipeline


def test_run_demo_pipeline_creates_outputs(tmp_path) -> None:
    sample_root = tmp_path / "sample" / "raw"
    sample_root.mkdir(parents=True)
    (sample_root / "customers.json").write_text(
        '[{"customer_id":"C1","email":"a@example.com","signup_date":"2026-01-01","country":"US","orders_count":1,"lifetime_value":10}]',
        encoding="utf-8",
    )
    (sample_root / "products.json").write_text(
        '[{"product_id":"P1","product_name":"Bottle","category":"Gear","brand":"Brand","list_price":10,"inventory_status":"in_stock"}]',
        encoding="utf-8",
    )
    (sample_root / "orders.json").write_text(
        '[{"order_id":"O1","order_date":"2026-01-01","customer_id":"C1","product_id":"P1","session_id":"S1","channel":"email","units":1,"unit_price":10,"discount_amount":0}]',
        encoding="utf-8",
    )
    (sample_root / "sessions.json").write_text(
        '[{"session_id":"S1","customer_id":"C1","event_date":"2026-01-01","channel":"email","device_type":"desktop","pageviews":3,"converted":true}]',
        encoding="utf-8",
    )

    result = run_demo_pipeline(tmp_path)
    assert result["fact_orders"][0]["order_id"] == "O1"
    assert (tmp_path / "demo_output" / "mart" / "fact_orders.json").exists()
