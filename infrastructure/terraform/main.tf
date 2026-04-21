terraform {
  required_version = ">= 1.6.0"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.30"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_bigquery_dataset" "raw" {
  dataset_id = var.raw_dataset_id
  location   = var.bigquery_location
}

resource "google_bigquery_dataset" "analytics" {
  dataset_id = var.analytics_dataset_id
  location   = var.bigquery_location
}

resource "google_storage_bucket" "artifacts" {
  name                        = var.artifact_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
}

resource "google_service_account" "analytics_runner" {
  account_id   = var.service_account_id
  display_name = "Ecommerce Analytics Runner"
}

resource "google_project_iam_member" "bigquery_admin" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  member  = "serviceAccount:${google_service_account.analytics_runner.email}"
}

resource "google_project_iam_member" "run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${google_service_account.analytics_runner.email}"
}

resource "google_cloud_run_v2_service" "dashboard" {
  name     = var.cloud_run_service_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
    service_account = google_service_account.analytics_runner.email
    containers {
      image = var.dashboard_container_image
    }
  }
}

resource "google_cloud_scheduler_job" "daily_refresh" {
  name        = "${var.name_prefix}-daily-refresh"
  description = "Daily ecommerce analytics refresh trigger"
  schedule    = var.daily_schedule
  region      = var.region
  time_zone   = var.time_zone

  http_target {
    http_method = "POST"
    uri         = google_cloud_run_v2_service.dashboard.uri

    oidc_token {
      service_account_email = google_service_account.analytics_runner.email
    }
  }
}
