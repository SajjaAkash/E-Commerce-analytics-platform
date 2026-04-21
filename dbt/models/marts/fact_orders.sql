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
  o.gross_revenue,
  o.discount_amount,
  o.net_revenue,
  o.session_id
from {{ ref('stg_orders') }} o
join {{ ref('stg_customers') }} c using (customer_id)
join {{ ref('stg_products') }} p using (product_id)
