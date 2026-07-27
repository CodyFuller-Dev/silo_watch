# Corrected main.tf with the proper Project ID

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = "project-7f6ebc51-8bd3-4490-bdd" # CORRECTED
  region  = "us-central1"
}

resource "google_cloud_run_v2_service" "silo_watch_service" {
  name     = "silo-watch"
  location = "us-central1"
  ingress  = "INGRESS_TRAFFIC_ALL"
  project  = "project-7f6ebc51-8bd3-4490-bdd" # CORRECTED

  template {
    containers {
      image = "us-docker.pkg.dev/cloudrun/container/hello" 

      resources {
        limits = {
          memory = "512Mi"
          cpu    = "1"
        }
      }
      
      env {
        name = "MY_GMAIL"
        value_source {
          secret_key_ref {
            secret  = "projects/project-7f6ebc51-8bd3-4490-bdd/secrets/MY_GMAIL" # CORRECTED
            version = "latest"
          }
        }
      }

      env {
        name = "GMAIL_PASS"
        value_source {
          secret_key_ref {
            secret  = "projects/project-7f6ebc51-8bd3-4490-bdd/secrets/GMAIL_PASS" # CORRECTED
            version = "latest"
          }
        }
      }

      env {
        name = "OPENWEATHER_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "projects/project-7f6ebc51-8bd3-4490-bdd/secrets/OPENWEATHER_API_KEY" # CORRECTED
            version = "latest"
          }
        }
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = google_cloud_run_v2_service.silo_watch_service.project
  location = google_cloud_run_v2_service.silo_watch_service.location
  name     = google_cloud_run_v2_service.silo_watch_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
