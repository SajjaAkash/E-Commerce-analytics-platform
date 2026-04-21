select
  session_id,
  customer_id,
  cast(event_date as date) as event_date,
  cast(session_started_at as timestamp) as session_started_at,
  channel,
  campaign_name,
  device_type,
  cast(pageviews as int64) as pageviews,
  cast(converted as bool) as converted
from {{ ref('sessions_seed') }}
