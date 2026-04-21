{% snapshot product_pricing_snapshot %}

{{
  config(
    target_schema='snapshots',
    unique_key='product_id',
    strategy='check',
    check_cols=['list_price', 'inventory_status']
  )
}}

select * from {{ ref('stg_products') }}

{% endsnapshot %}
