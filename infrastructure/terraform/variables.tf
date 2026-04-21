variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "bigquery_location" {
  type    = string
  default = "US"
}

variable "raw_dataset_id" {
  type    = string
  default = "ecommerce_raw"
}

variable "analytics_dataset_id" {
  type    = string
  default = "ecommerce_analytics"
}

variable "artifact_bucket_name" {
  type = string
}

variable "service_account_id" {
  type    = string
  default = "ecommerce-analytics-runner"
}

variable "cloud_run_service_name" {
  type    = string
  default = "ecommerce-analytics-dashboard"
}

variable "dashboard_container_image" {
  type    = string
  default = "us-docker.pkg.dev/cloudrun/container/hello"
}

variable "daily_schedule" {
  type    = string
  default = "0 6 * * *"
}

variable "time_zone" {
  type    = string
  default = "America/Chicago"
}

variable "name_prefix" {
  type    = string
  default = "ecommerce-analytics"
}
