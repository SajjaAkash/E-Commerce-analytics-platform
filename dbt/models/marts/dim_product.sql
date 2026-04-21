select
  product_id,
  product_name,
  category,
  brand,
  list_price,
  inventory_status
from {{ ref('stg_products') }}
