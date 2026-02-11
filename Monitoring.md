#### Now you’re thinking like someone building a real platform.
####If you can’t observe it, you don’t control it.

####We’ll add Prometheus (metrics collector) and Grafana (visualization UI) to your GKE cluster the clean way.

#### We’ll use Helm. That’s the professional method.

🧠 What We’re Installing

#### We’ll install:

#### kube-prometheus-stack

#### That bundle includes:

#### Prometheus

#### Grafana

#### Node Exporter

#### kube-state-metrics

#### Alertmanager

#### It gives:

#### Node CPU, memory, disk

#### Pod metrics

#### Deployment metrics

#### Cluster health

#### Prebuilt dashboards

## 🚀 Step 1 — Install Helm

#### On your Jenkins VM (or wherever kubectl works):

```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Verify:

```
helm version
```

## 🚀 Step 2 — Add Prometheus Helm Repo
```
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```
## 🚀 Step 3 — Create Monitoring Namespace
```
kubectl create namespace monitoring
```
## 🚀 Step 4 — Install kube-prometheus-stack
```
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring
```

### Wait 2–3 minutes.

### Check pods:
```
kubectl get pods -n monitoring
```

You should see:

prometheus

grafana

node-exporter

kube-state-metrics

## 🚀 Step 5 — Expose Grafana

### By default Grafana is internal.

### Expose it via LoadBalancer:
```
kubectl patch svc monitoring-grafana \
  -n monitoring \
  -p '{"spec": {"type": "LoadBalancer"}}'
```

### Then:
```
kubectl get svc -n monitoring
```

### Wait for EXTERNAL-IP.

### Open in browser:

```
http://<external-ip>
```

## 🔐 Grafana Login

### Default:

### Username:
```
admin
```

### Password:
```
kubectl get secret --namespace monitoring monitoring-grafana \
  -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```

## 🧠 What You’ll See

#### Inside Grafana → Dashboards → Manage

### Look for:

####  Kubernetes / Compute Resources / Node

####  Kubernetes / Compute Resources / Pod

#### Kubernetes / Compute Resources / Namespace

#### Kubernetes / Cluster Overview

### Those dashboards show:

#### CPU usage

####  Memory usage

#### Network

#### Pod status

#### Node health

## 🧠 Architecture After Install
GKE Cluster
 ├── Your OTT Pods
 ├── Prometheus Pod (scraping metrics)
 ├── Node Exporter (collecting node metrics)
 └── Grafana (visualizing)


####  You now have observability.

#### ⚠️ Free Tier Warning

####   This stack consumes resources.

#### You may see:

####  4–8 extra pods

#### Increased memory usage

#### If your node is e2-micro, it might struggle.

#### If pods stay Pending:
####  You need to scale node.

## 🔬 Optional (Safer for Small Nodes)

#### If your node is small, install with reduced resource usage:

```
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set prometheus.prometheusSpec.resources.requests.memory="256Mi" \
  --set grafana.resources.requests.memory="128Mi"
```

## 🧠 Why This Matters

#### Before monitoring:
####  You deploy blindly.

#### After monitoring:
#### You see:

####  CPU spikes

####  Memory pressure

#### Restart loops

#### Node health

#### Now you’re building a real production-ready cluster.

#### If you want next level:

#### Add HPA and watch scaling in Grafana

#### Add alert rules

#### Integrate with Slack

####  Add Loki for logs

####  You’re stepping into SRE territory now.

####  explain how to set dasboard in grafana for kubernetes monitring

####  Now we’re entering observability philosophy. Good.

#### Grafana is just a window.
####  Prometheus is the brain.
####  Metrics are the truth.

####  If Prometheus is scraping your cluster (via kube-prometheus-stack), Grafana already has most dashboards preloaded.

## Let’s walk through it properly and cleanly.

####  🧠 First Understand the Data Flow
####  Node → node-exporter → Prometheus
#### Pod → kube-state-metrics → Prometheus
#### Prometheus → Grafana → You


### Prometheus collects metrics.
### Grafana visualizes them.

### You don’t “create monitoring.”
### You visualize metrics that already exist.

## 🚀 Step 1 — Open Grafana

### Go to:
```
http://<grafana-external-ip>
```

### Login with:

### Username: admin

### Password: (from secret)

## 🚀 Step 2 — Check Data Source

### Left sidebar → ⚙️ Settings → Data Sources

### You should see:

### Prometheus


### Click it → Test

### It should say:

### Data source is working


### If not, something is wrong with Prometheus.

## 🚀 Step 3 — Use Prebuilt Kubernetes Dashboards

### kube-prometheus-stack installs dashboards automatically.

### Go to:

### Left Sidebar → Dashboards → Browse

### Search:

### Kubernetes


## You will find:

### Kubernetes / Compute Resources / Node

### Kubernetes / Compute Resources / Pod

### Kubernetes / Compute Resources / Namespace

### Kubernetes / Cluster Overview

### Kubernetes / API Server

## Open:

## 👉 Kubernetes / Compute Resources / Node

### You will see:

### CPU usage per node

### Memory usage

### Filesystem usage

### Network traffic

### Open:

## 👉 Kubernetes / Compute Resources / Pod

### You will see:

### Pod CPU usage

### Pod memory usage

### Restart counts

### Container status

## That’s real cluster monitoring.

### 🧠 How Dashboards Actually Work

### Each panel runs a PromQL query.

### Example CPU usage query:
```
sum(rate(container_cpu_usage_seconds_total[5m])) by (pod)
```

### That means:
### “Show CPU usage per pod over last 5 minutes.”

### Grafana panels = visual PromQL queries.

## 🚀 Step 4 — Create Your Own Dashboard

### Let’s create a simple one for your ott-app.

### Click:

### → Dashboard → Add new panel

### Query:

### For CPU usage of your deployment:
```
sum(rate(container_cpu_usage_seconds_total{namespace="default", pod=~"ott-app.*"}[5m]))
```

### Set visualization:

### Time series

### Click Apply.

### You now have custom CPU monitoring for your app.

## 🚀 Add Memory Panel

### Add another panel:
```
sum(container_memory_usage_bytes{namespace="default", pod=~"ott-app.*"})
```

### Set unit to:
### Bytes → MB

### Now you can watch memory growth.

## 🚀 Node CPU Panel

### Query:
```
sum(rate(node_cpu_seconds_total{mode!="idle"}[5m])) by (instance)
```

### This shows node-level CPU usage.

### 🧠 Understanding What You're Watching

### Node dashboard → Infrastructure health
### Pod dashboard → Application health
### Namespace dashboard → Service-level health

### If node CPU spikes → scale nodes
### If pod CPU spikes → scale pods
### If memory spikes → fix app or increase resources

### Monitoring drives scaling decisions.

## 🚀 Bonus — Add Replica Monitoring

### Query:
```
kube_deployment_status_replicas{deployment="ott-app"}
```

### This shows how many replicas are running.

### If you scale deployment, this graph changes instantly.

## 🧠 Real Production Setup

### Production Grafana setup usually includes:

### Node dashboard

### Pod dashboard

### API latency dashboard

### Error rate dashboard

### HPA metrics

### Alert rules

### Monitoring without alerts is only half observability.
