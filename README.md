
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




🚀 CLEAN, CORRECT INSTALL (Step-by-Step)

Run these commands exactly as written.

## ✅ STEP 1 — Install Required Base Packages

```
sudo apt-get update
sudo apt-get install -y apt-transport-https ca-certificates gnupg curl
```

## ✅ STEP 2 — Add Google Cloud Official Key

```
curl -fsSL https://packages.cloud.google.com/apt/doc/apt-key.gpg | \
sudo gpg --dearmor -o /usr/share/keyrings/cloud.google.gpg
```

## ✅ STEP 3 — Add Google Cloud Repository

```
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | \
sudo tee /etc/apt/sources.list.d/google-cloud-sdk.list
```

## ✅ STEP 4 — Update APT

```
sudo apt-get update
```

Important:
You must see something like:

https://packages.cloud.google.com/apt cloud-sdk InRelease


If you don't see that line, repository was not added correctly.

## ✅ STEP 5 — Install SDK + Plugin + kubectl

```
sudo apt-get install -y google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin kubectl
```


## 🔍 Verify Installation

Run:
```
which gcloud
which kubectl
which gke-gcloud-auth-plugin
```

All three must return paths.

## 🔥 Then Enable Plugin

```
echo 'export USE_GKE_GCLOUD_AUTH_PLUGIN=True' >> ~/.bashrc
source ~/.bashrc
```
## 🔁 Then Authenticate

```
gcloud auth login
gcloud config set project project-3a9d1629-f247-457c-ae4
```

## 🔁 Then Get Credentials

```
gcloud container clusters get-credentials cluster-1 --zone us-central1-a
```

## 🚀 FIX — Install kubectl Properly

### Since your gcloud is installed via APT, do:

```
sudo apt-get update
sudo apt-get install -y kubectl
```

### Then verify:

```
which kubectl
```

### It should return something like:
```
/usr/bin/kubectl
```

Now run:

kubectl get nodes

## 🧠 Why This Happened

### When you ran:
```
gcloud container clusters get-credentials
```

That only:

### Updated kubeconfig

### Saved cluster auth info

### It does NOT install kubectl.

### kubectl is a separate binary.

### Cloud SDK ≠ kubectl automatically (depending on install method).

## 🧠 Important Check After Installing

### If kubectl get nodes shows:

### No resources found


### That means cluster has zero nodes (quota issue earlier).

If it shows:

<img width="1068" height="182" alt="image" src="https://github.com/user-attachments/assets/ab00630a-c15e-43c7-9efc-3bc4300b695c" />



### Then cluster is healthy.

### 🔍 If kubectl Still Not Found After Install

## Run:

```
 echo $PATH
```

### If /usr/bin is missing (rare), then shell PATH issue.



## Next: deploy your OTT app to GKE

### We’ll do this in clean, predictable steps.

### Step 1 — Confirm current context (sanity check)

```
kubectl config current-context
```

### You should see something like:

```
gke_project-3a9d1629-f247-457c-ae4_us-central1-a_cluster-1
```
