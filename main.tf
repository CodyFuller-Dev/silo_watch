# terraform needs to track what its built before aka a "state file"
#1 here it is being told to use google cloud storage bucket aka "gcs"
#2 the bucket info comes from setting up the physical gcp service
#3 this is the filepath that houses the state file
terraform {
  backend "gcs" {
    bucket  = "terraform-state-project-7f6ebc51-8bd3"
    prefix  = "silo-watch/state"
  }

  #here we are telling terraform (which also allows the deploy file) what plugin / service we are needing aka google
  #the version number is important because it means we can use any release of version 5 aka 5.1 5.2 etc. Known non-buggy releases
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

#this sets the standard for all project and region fields needed below 
#gives the project name from gcp and the region I want to host it in
provider "google" {
  project = "project-7f6ebc51-8bd3-4490-bdd"
  region  = "us-central1"
}

#this tells terraform what we actually want to create in gcp and then give it the name designator aka silo_watch_service
#1 what its actually called in gcp
#2 what region and project (as noted from above unless specified different)
#3 lets the public internet interface with it
resource "google_cloud_run_v2_service" "silo_watch_service" {
  name     = "silo-watch"
  location = "us-central1"
  ingress  = "INGRESS_TRAFFIC_ALL"
  project  = "project-7f6ebc51-8bd3-4490-bdd"

#this is important because its telling terraform that these specific items are being managed by something else
#in this case its actually step 6 of the deploy.yml file  
  lifecycle {
    ignore_changes = [
      template[0].containers[0].image,
      client,
      client_version,
      template[0].labels,
      template[0].annotations
    ]
  }
#1 sets the blueprint for the upcoming build of the container
#2 this is the block that holds things like memory limits the actual image for the container and the env variables
#3 the image actually starts life as a generic container then gets "remodled" to what we actually want it in
  template {
    containers {
      
      image = "us-docker.pkg.dev/cloudrun/container/hello" 

      #this sets the maximum hardware limits for the container so that costs do not spiral out of control
      #here no more than half a gig of ram and 1 cpu core
      resources {
        limits = {
          memory = "512Mi"
          cpu    = "1"
        }
      }

      #this is pulling the env var from the google secrets manager when the container starts up so the plain text is never leaked
      #its also told the path to retrieve it and to grab what ever is designated as the latest
      #1-3
      env {
        name = "MY_GMAIL"
        value_source {
          secret_key_ref {
            secret  = "projects/project-7f6ebc51-8bd3-4490-bdd/secrets/MY_GMAIL"
            version = "latest"
          }
        }
      }
      
      #this is pulling the env var from the google secrets manager when the container starts up so the plain text is never leaked
      #its also told the path to retrieve it and to grab what ever is designated as the latest
      #2-3
      env {
        name = "GMAIL_PASS"
        value_source {
          secret_key_ref {
            secret  = "projects/project-7f6ebc51-8bd3-4490-bdd/secrets/GMAIL_PASS"
            version = "latest"
          }
        }
      }

      #this is pulling the env var from the google secrets manager when the container starts up so the plain text is never leaked
      #its also told the path to retrieve it and to grab what ever is designated as the latest
      #3-3
      env {
        name = "OPENWEATHER_API_KEY"
        value_source {
          secret_key_ref {
            secret  = "projects/project-7f6ebc51-8bd3-4490-bdd/secrets/OPENWEATHER_API_KEY"
            version = "latest"
          }
        }
      }
    }
  }
}

#this changes everything from being super locked down to able to be accessed by the public internet
#pro/loc/name are already defined at the begining and being refrenced
#role is saying permission is being granted to invoke the service
#removes restrictions and allows anyone to invoke
#role=what member=who
resource "google_cloud_run_v2_service_iam_member" "public_access" {
  project  = google_cloud_run_v2_service.silo_watch_service.project
  location = google_cloud_run_v2_service.silo_watch_service.location
  name     = google_cloud_run_v2_service.silo_watch_service.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
