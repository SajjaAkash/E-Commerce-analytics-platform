output "raw_dataset_id" {
  value = google_bigquery_dataset.raw.dataset_id
}

output "analytics_dataset_id" {
  value = google_bigquery_dataset.analytics.dataset_id
}

output "service_account_email" {
  value = google_service_account.analytics_runner.email
}

output "dashboard_uri" {
  value = google_cloud_run_v2_service.dashboard.uri
}
