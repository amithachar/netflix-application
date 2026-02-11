
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

gcloud container clusters get-credentials ott-cluster --zone us-central1-a

### Run that on:

### Your Jenkins VM

### OR your local machine

### Then test:

kubectl get nodes

## ✅ Step 3 — Build Docker Image

### Inside your project:

### docker build -t yourdockerhubusername/ott-app:latest .

## ✅ Step 4 — Push to Docker Hub

### Login: Docker login  
you will a link paste that link in browser -> login to docker with code -> copy the verfication code and paste in jenkins server.

## Push:

## docker push yourdockerhubusername/ott-app:latest

## ✅ Step 5 — Create Kubernetes Deployment YAML

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ott-app
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ott-app
  template:
    metadata:
      labels:
        app: ott-app
    spec:
      containers:
        - name: ott-container
          image: yourdockerhubusername/ott-app:latest
          ports:
            - containerPort: 5000
```

## ✅ Step 6 — Expose Using NodePort (Free Tier Safe)

```
apiVersion: v1
kind: Service
metadata:
  name: ott-service
spec:
  type: NodePort
  selector:
    app: ott-app
  ports:
    - port: 80
      targetPort: 5000
      nodePort: 30007
```

## ✅ Step 7 — Deploy to GKE

```
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
```
kubectl get pods
kubectl get svc
```

## ✅ Step 8 — Access App

## Find node external IP:

##  kubectl get nodes -o wide

http://NODE_EXTERNAL_IP:30007








