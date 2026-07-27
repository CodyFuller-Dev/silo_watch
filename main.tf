# ==========================================================================
# PART 1: The Provider (Handing over your ID badge to Google Cloud)
# ==========================================================================
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "silo-watch-902081503325"
  region  = "us-central1"
}

# ==========================================================================
# PART 2 & 3: Building the Cloud Run Service (Setting up the container & specs)
# ==========================================================================
resource "google_cloud_run_v2_service" "silo_watch_service" {
  name     = "silo-watch"
  location = "us-central1"
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {
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
      
      # Secret 1: Your Gmail Address
      env {
        name = "MY_GMAIL"
        value_source {
          secret_key_ref {
            secret  = "projects/silo-watch-902081503325/secrets/MY_GMAIL"
            version = "latest"
          }
        }
      }

      # Secret 2: Your Gmail App Password
      env {
        name = "GMAIL_PASS"
        value_source {
          secret_key_ref {
            secret  = "projects/silo-watch-902081503325/secrets/GMAIL_PASS"
            version = "latest"
          }
        }
      }

      # Secret 3: Your OpenWeather API Key
      env {
        name = "OPENWEATHER_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "projects/silo-watch-902081503325/secrets/OPENWEATHER_API_KEY"
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
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = google_cloud_run_v2_service.silo_watch_service.project
  location = google_cloud_run_v2_service.silo_watch_service.location
  name     = google_cloud_run_v2_service.silo_watch_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
