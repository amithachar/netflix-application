<img width="1593" height="519" alt="image" src="https://github.com/user-attachments/assets/bcd56313-dd68-49fb-8af8-226698336993" /># netflix-application
netflix-application


### Pipeline Architecture

<img width="1593" height="519" alt="image" src="https://github.com/user-attachments/assets/8894252b-92d3-4282-b93e-ca509aac5a89" />

## ✅ Step 1 — Create GKE Cluster via UI (Minimal Setup)  ( Due to GCP restrictions )

### Go to:

### GCP Console → Kubernetes Engine → Create Cluster

### Choose:

### Standard cluster (not Autopilot for now)

### Important settings:

### Location type: Zonal

### Zone: us-central1-a (or whichever works)

### Node count: 1

### Machine type: e2-micro

### Disk type: Standard persistent disk

### Disk size: 10GB

### Disable autoscaling

### No extra node pools

## ✅ Step 2 — Connect to Cluster

### In GCP Console, click:

### “Connect”

### It will give command like:

bash```
gcloud container clusters get-credentials ott-cluster --zone us-central1-a


### Run that on:

### Your Jenkins VM

### OR your local machine

### Then test:

bash```
kubectl get nodes

## ✅ Step 3 — Build Docker Image

bash```

docker build -t yourdockerhubusername/ott-app:latest .



