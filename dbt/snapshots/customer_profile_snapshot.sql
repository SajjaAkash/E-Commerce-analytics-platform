{% snapshot customer_profile_snapshot %}

{{
  config(
    target_schema='snapshots',
    unique_key='customer_id',
    strategy='check',
    check_cols=['country', 'segment', 'orders_count', 'lifetime_value']
  )
}}

select * from {{ ref('stg_customers') }}

{% endsnapshot %}
