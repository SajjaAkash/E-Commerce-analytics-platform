select
  product_id,
  product_name,
  category,
  brand,
  cast(list_price as numeric) as list_price,
  inventory_status
from {{ ref('products_seed') }}
