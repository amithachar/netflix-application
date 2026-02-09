resource "google_container_cluster" "gke" {
  name     = "ott-gke-cluster"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name     = "primary-node-pool"
  location = var.region
  cluster  = google_container_cluster.gke.name

  node_config {
    machine_type = "e2-medium"
    disk_size_gb = 30
  }

  node_count = 2
}
