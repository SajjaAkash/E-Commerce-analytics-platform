# Deployment Guide

## Prerequisites

- Google Cloud project with billing enabled
- Terraform 1.6+
- BigQuery, Cloud Run, Cloud Scheduler, and IAM APIs enabled
- Python 3.11+ for local development

## Suggested Deployment Sequence

1. Copy the Terraform variable template:

   ```powershell
   Copy-Item infrastructure/terraform/terraform.tfvars.example infrastructure/terraform/terraform.tfvars
   ```

2. Update the project, region, and naming inputs in `terraform.tfvars`.

3. Initialize and review the Terraform plan:

   ```powershell
   cd infrastructure/terraform
   terraform init
   terraform plan
   ```

4. Apply infrastructure when ready:

   ```powershell
   terraform apply
   ```

5. Configure BigQuery credentials and a matching `profiles.yml` for `dbt`.

6. Execute the transformation workflow:

   ```powershell
   dbt build --project-dir dbt --profiles-dir dbt --target dev
   ```

7. Deploy the Streamlit app to Cloud Run or use the included Docker strategy of your choice.

## Operational Notes

- The included Terraform provisions datasets, a storage bucket, a service account, scheduler wiring, and a Cloud Run service placeholder.
- The DAG and orchestration helpers are intentionally dry-run friendly for local repository validation.
- The local demo pipeline is separate from the warehouse deployment path so interviews and code reviews can still exercise the repo end to end.
