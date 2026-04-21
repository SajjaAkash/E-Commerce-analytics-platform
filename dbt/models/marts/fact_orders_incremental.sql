{{
  config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    partition_by={"field": "order_date", "data_type": "date"},
    cluster_by=["customer_id", "channel"]
  )
}}

select
  o.order_id,
  o.order_date,
  o.customer_id,
  c.segment,
  o.channel,
  o.product_id,
  p.product_name,
  p.category,
  o.units,
  o.order_status,
  o.gross_revenue,
  o.discount_amount,
  o.refund_amount,
  o.net_revenue - o.refund_amount as realized_revenue,
  o.session_id
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c using (customer_id)
join {{ ref('stg_products') }} p using (product_id)

{% if is_incremental() %}
where o.order_date >= date_sub(current_date(), interval 7 day)
{% endif %}
