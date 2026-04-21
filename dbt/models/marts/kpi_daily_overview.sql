with orders as (
  select * from {{ ref('fact_orders') }}
),
sessions as (
  select * from {{ ref('stg_sessions') }}
)
select
  o.order_date as metric_date,
  count(*) as orders,
  count(distinct o.customer_id) as customers,
  round(sum(o.net_revenue), 2) as net_revenue,
  round(sum(o.net_revenue) / count(*), 2) as average_order_value,
  round(safe_divide(countif(s.converted), count(s.session_id)), 4) as conversion_rate,
  round(
    safe_divide(count(distinct case when o.segment = 'repeat' then o.customer_id end), count(distinct o.customer_id)),
    4
  ) as repeat_customer_rate
from orders o
left join sessions s
  on o.order_date = s.event_date
group by 1
order by 1
