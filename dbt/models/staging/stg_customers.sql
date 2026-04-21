select
  customer_id,
  lower(trim(email)) as email,
  cast(signup_date as date) as signup_date,
  country,
  case when orders_count > 1 then 'repeat' else 'new' end as segment,
  cast(orders_count as int64) as orders_count,
  cast(lifetime_value as numeric) as lifetime_value
from {{ ref('customers_seed') }}
