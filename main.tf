# ==========================================================================
# PART 1: The Provider & Persistent Backend (Setting up the persistent brain)
# ==========================================================================
terraform {
  backend "gcs" {
    bucket  = "terraform-state-project-7f6ebc51-8bd3"
    prefix  = "silo-watch/state"
  }
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "project-7f6ebc51-8bd3-4490-bdd"
  region  = "us-central1"
}

# ==========================================================================
# PART 2 & 3: Building the Cloud Run Service (Setting up the container & specs)
# ==========================================================================
resource "google_cloud_run_v2_service" "silo_watch_service" {
  name     = "silo-watch"
  location = "us-central1"
  ingress  = "INGRESS_TRAFFIC_ALL"
  project  = "project-7f6ebc51-8bd3-4490-bdd"

  # UPDATED: Tells Terraform to ignore changes made by gcloud deploy
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
      client,
      client_version,
      template[0].labels,
      template[0].annotations
    ]
  }

  template {
    service_account = "project-7f6ebc51-8bd3-4490-bdd@appspot.gserviceaccount.com"
    
    containers {
      # This is a temporary placeholder image. GitHub Actions will overwrite this later.
      image = "us-docker.pkg.dev/cloudrun/container/hello" 

      # Memory and CPU limit settings
      resources {
        limits = {
          memory = "512Mi"
          cpu    = "1"
        }
      }

      # ==========================================================================
      # PART 4: Environment Variables (Grabbing passwords from Secret Manager)
      # ==========================================================================
      env {
        name = "MY_GMAIL"
        value_source {
          secret_key_ref {
            secret  = "MY_GMAIL"
            version = "latest"
          }
        }
      }

      env {
        name = "GMAIL_PASS"
        value_source {
          secret_key_ref {
            secret  = "GMAIL_PASS"
            version = "latest"
          }
        }
      }

      env {
        name = "OPENWEATHER_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "OPENWEATHER_API_KEY"
            version = "latest"
          }
        }
      }
    }
  }
}

# ==========================================================================
# PART 5: Public Access (Opening the front door to the internet)
# ==========================================================================
# ==========================================================================
# PART 6: IAM Permissions (Allowing Cloud Run to access secrets)
# ==========================================================================

# Get the default Cloud Run service account
data "google_client_config" "default" {}

# Grant the Cloud Run service account permission to access MY_GMAIL secret
resource "google_secret_manager_secret_iam_member" "gmail_secret_access" {
  secret_id = "MY_GMAIL"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:project-7f6ebc51-8bd3-4490-bdd@appspot.gserviceaccount.com"
}

# Grant the Cloud Run service account permission to access GMAIL_PASS secret
resource "google_secret_manager_secret_iam_member" "gmail_pass_secret_access" {
  secret_id = "GMAIL_PASS"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:project-7f6ebc51-8bd3-4490-bdd@appspot.gserviceaccount.com"
}

# Grant the Cloud Run service account permission to access OPENWEATHER_API_KEY secret
resource "google_secret_manager_secret_iam_member" "api_key_secret_access" {
  secret_id = "OPENWEATHER_API_KEY"
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:project-7f6ebc51-8bd3-4490-bdd@appspot.gserviceaccount.com"
}

# ==========================================================================
# PART 7: Public Access (Opening the front door to the internet)
# ==========================================================================
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = google_cloud_run_v2_service.silo_watch_service.project
  location = google_cloud_run_v2_service.silo_watch_service.location
  name     = google_cloud_run_v2_service.silo_watch_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
