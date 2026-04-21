select
  customer_id,
  email,
  country,
  signup_date,
  segment,
  orders_count,
  lifetime_value
from {{ ref('stg_customers') }}
