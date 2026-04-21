select
  order_id,
  cast(order_date as date) as order_date,
  customer_id,
  product_id,
  session_id,
  channel,
  cast(units as int64) as units,
  cast(unit_price as numeric) as unit_price,
  cast(discount_amount as numeric) as discount_amount,
  cast(units as numeric) * cast(unit_price as numeric) as gross_revenue,
  cast(units as numeric) * cast(unit_price as numeric) - cast(discount_amount as numeric) as net_revenue
from {{ ref('orders_seed') }}
