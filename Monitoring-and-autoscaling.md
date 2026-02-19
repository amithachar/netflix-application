## Grafana and Prometheus

#### We’ll add Prometheus (metrics collector) and Grafana (visualization UI) to your GKE cluster the clean way.
#### We’ll use Helm. That’s the professional method.

🧠 What We’re Installing

### We’ll install:
#### * kube-prometheus-stack
#### * That bundle includes:
#### * Prometheus
#### * Grafana
#### * Node Exporter
#### * kube-state-metrics
#### * Alertmanager
#### * It gives:
#### * Node CPU, memory, disk
#### * Pod metrics
#### * Deployment metrics
#### * Cluster health
#### * Prebuilt dashboards

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

```
kubectl get svc -n monitoring
```

# How to get monitoring IP
<img width="1123" height="150" alt="image" src="https://github.com/user-attachments/assets/8dc7db1c-cc92-4bb5-83d1-907cd59ab928" />

## Grafana Dashboard

<img width="1897" height="958" alt="image" src="https://github.com/user-attachments/assets/2490677c-ed0a-4a6a-88b8-5d157f10c698" />


### Monitoring without alerts is only half observability.


# LOAD TESTING FOR KUBERNETES

## 1. Updated GPG Key Command

```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://apt.grafana.com/gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/grafana.gpg
````
## 2. Verify and Add the Repository

```
echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee /etc/apt/sources.list.d/grafana.list
```

## 3. Update and Install

```
sudo apt-get update
sudo apt-get install k6
```

## Alternative: Use Snap (Quickest Fix)

```
sudo snap install k6
```
## Simple stress test:
```
import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  vus: 200,        // virtual users
  duration: '2m',
};

export default function () {
  http.get('http://your-external-ip');
  sleep(1);
}
```

## Run:

```
k6 run script.js
```

### Now you’re sending 200 concurrent users continuously.


## Here is your production-ready deployment YAML with resource definitions added:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ott-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: ott-app
  template:
    metadata:
      labels:
        app: ott-app
    spec:
      containers:
      - name: ott-app
        image: amithachar/ott-app:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "200m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
```

## Apply it

```
kubectl apply -f deployment.yaml

```

## Now Kubernetes understands how “big” your pod is supposed to be.

## Next, create the HPA.

### Create a new file hpa.yaml:

```
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: ott-app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: ott-app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 60
```

## Apply:

```
kubectl apply -f hpa.yaml
```
## Now Check 

```
kubectl get hpa
```

## And watch during load:

```
kubectl get hpa -w
```

## Here’s the science of what will happen:

### If CPU average across pods > 60%,
### Kubernetes increases replicas.

### If CPU drops below threshold,
### It scales down.

### But remember something important.

## HPA reacts to CPU usage relative to requests, not limits.

### So with:
```
request: 200m
```
### If pod uses 120m CPU → that’s 60% utilization.

### That’s when scaling triggers.

# 🔬 The Science of Scaling (HPA Logic)

Understanding how the Horizontal Pod Autoscaler (HPA) makes decisions is the difference between a basic deployment and true Site Reliability Engineering.

### How the Trigger Works
The HPA doesn't just look at "load"; it follows a specific mathematical threshold based on the resources we defined.

* **If CPU average across pods > 60%:** Kubernetes increases replicas (up to 10).
* **If CPU drops below the threshold:** Kubernetes gradually scales down (minimum 2).

### ⚠️ The SRE Golden Rule
A common mistake is assuming HPA looks at the **Limit**. It does not. 
**HPA reacts to CPU usage relative to REQUESTS.**



#### The Math for our `ott-app`:
Given our `deployment.yaml` configuration:
* **CPU Request:** `200m`
* **Target Utilization:** `60%`
* **Scaling Threshold:** $200m \times 0.60 = 120m$

> **Practical Insight:** If your pod uses **120m** of CPU, scaling triggers. If your app is lightweight and CPU never crosses that 60% mark, the HPA will never scale—even if the app feels slow.

---

### 🔍 Beyond CPU: The SRE Investigation
If your application is struggling under load but the HPA is not scaling, the bottleneck is likely not CPU-bound. As an SRE, this is where the "fun" starts. You must investigate:

1. **Database:** Are we hitting connection pool limits?
2. **Network:** Is there high latency or bandwidth throttling?
3. **Thread Pool:** Is the application server bottlenecked on concurrent threads?
4. **External APIs:** Are slow downstream dependencies holding up the request?

**Remember:** Autoscaling is easy. Understanding why it *didn't* trigger is where real engineering begins.


## 🧠 SRE Insight: The "Subtle" Power of HPA

A common misconception in Kubernetes is that HPA is a "magic button" for all performance issues. Here is the reality:

> **If your app is lightweight and CPU usage never crosses 60%, the HPA will never scale.**

If your application is struggling but the pod count remains static, it doesn't mean your autoscaling is broken. It means your bottleneck is likely **not CPU-bound**. You may be facing issues with:

* 🗄️ **Database:** Connection pool exhaustion or slow queries.
* 🌐 **Network:** Bandwidth throttling or high latency.
* 🧵 **Thread Pool:** Application-level concurrency limits.
* 🔌 **External APIs:** Slow downstream dependencies.

**Crucial Rule:** CPU-based scaling only solves **CPU-bound** workloads.

---

## 🧪 The Elasticity Experiment

After enabling HPA, run this test to verify your configuration:

1.  **Start a Load Test:** Use a tool like `hey`, `ab`, or `locust`.
2.  **Monitor HPA:** ```bash
    kubectl get hpa -w
    ```
3.  **Watch Pods:** ```bash
    kubectl get pods -w
    ```

### Results
* **If pods increase:** Congratulations, you have successfully built **elasticity**.
* **If pods don't increase:** It’s time to debug deeper into the application stack.

This is where real **Site Reliability Engineering** begins. Autoscaling is the easy part—understanding why it *didn't* trigger is where the real fun starts.

### That block:

```
resources:
  requests:
    cpu: "200m"
    memory: "256Mi"
  limits:
    cpu: "500m"
    memory: "512Mi"
```

### is Kubernetes saying:

### “Here is what this container needs…
### and here is the maximum it’s allowed to consume.”

### Let’s break it down calmly and precisely.

## 🔹 Requests = Guaranteed Minimum
```
requests:
  cpu: 200m
  memory: 256Mi
```

### This tells Kubernetes scheduler:

### “When placing this pod on a node, ensure the node has at least this much free.”

### So:

### 200m CPU is reserved

### 256Mi memory is reserved

### The scheduler uses this to decide which node the pod can run on.

### No request → Kubernetes might overpack nodes blindly.

## 🔹 Limits = Hard Ceiling

```
limits:
  cpu: 500m
  memory: 512Mi
```

# ⚙️ Kubernetes Resource Management: The Deep Dive

Managing resources for the `ott-app` involves balancing performance and stability. Here is the technical breakdown of how we define "boundaries" for our containers.

---

## 🛑 Requests vs. Limits: The "Harsh but Fair" Rules

In our configuration, we have set strict boundaries:
* **CPU Limit:** 500m
* **Memory Limit:** 512Mi

| Resource | Action when limit is hit | Result |
| :--- | :--- | :--- |
| **CPU** | Throttling | The application **slows down**. |
| **Memory** | OOMKilled | The container is **terminated**. |

> **SRE Insight:** CPU limits cause a "slowdown," while Memory limits cause a "kill." Distributed systems are polite only when you enforce these boundaries.

---

## 📏 Understanding Units (m and Mi)

### What is “m” in CPU?
CPU is measured in **millicores**.
* **1000m** = 1 Full CPU Core
* **200m** = 0.2 CPU Core (Our Request)
* **500m** = 0.5 CPU Core (Our Limit)

*If your worker node has 4 cores, the total capacity is **4000m**.*

### What is “Mi” in Memory?
Kubernetes uses binary units (base-2) rather than decimal units (base-10).
* **Mi (Mebibyte)** = $1024^2$ bytes.
* **256Mi** ≈ 268 Megabytes (MB).
* **512Mi** ≈ 536 Megabytes (MB).

---

## ⚖️ Why This Matters for Autoscaling

The Horizontal Pod Autoscaler (HPA) uses the **Request** value as the denominator for its math.

$$Utilization = \frac{\text{Actual CPU Usage}}{\text{Requested CPU}}$$

**Example Scenario:**
* **Request:** 200m
* **Current Usage:** 120m
* **Calculation:** $120 / 200 = 60\%$

If your HPA target is **60%**, scaling triggers now. Without specific requests, the autoscaler has no baseline to calculate percentages.

---

## 🍽️ The Restaurant Analogy
* **Requests:** The chair you reserve in a restaurant. You are guaranteed this seat.
* **Limits:** The maximum amount of food you are allowed to eat. If you try to eat more, security (Kubernetes) intervenes.

---

## 🛠️ Engineering Trade-offs

Resource tuning is a balancing act. If you:
* **Set request too high:** You waste money; fewer pods fit on the node.
* **Set request too low:** The autoscaler triggers too easily (false positives).
* **Set limit too low:** The app throttles and performance degrades.
* **Set limit too high:** One "greedy" pod can starve others and take down the entire node.

> **Warning:** If you remove limits entirely, a single pod under load might work beautifully—until the day it consumes the whole node's resources and causes a cluster-wide failure.

---

Would you like me to help you **calculate the optimal CPU requests** for your `ott-app` based on your current production load numbers?


## Troubleshooting

### One pod is pending.

<img width="981" height="108" alt="image" src="https://github.com/user-attachments/assets/9c9072c1-f803-4549-af85-3d5518564e23" />

### Now we’re in the interesting part of Kubernetes behavior.

## Pending does not mean “crashed.”

### It means:

### “Kubernetes wants to run this pod… but cannot find a place for it.”

### The scheduler is basically saying:

### “I don’t have enough room.”

### Since you just added:
```
requests:
  cpu: 200m
  memory: 256Mi
```

### This is almost certainly a resource scheduling issue.

### Let’s diagnose properly instead of guessing.

### Step 1 — Describe the Pod (This Reveals Truth)

### Run:
```
kubectl describe pod ott-app-5c465f9597-q7grj
```

### Look at the bottom under Events.

### You will probably see something like:
```
0/1 nodes are available: insufficient cpu
```

### or
```
0/1 nodes are available: insufficient memory
```

### That message is the real answer.

### Why This Happens

### Before adding requests, Kubernetes didn’t reserve resources.

### Now it must guarantee:
```
200m CPU

256Mi memory
```
### If your node does not have enough free allocatable resources,
### scheduler refuses to place the pod.

### That’s discipline.

### Step 2 — Check Node Capacity

### Run:
```
kubectl describe node <node-name>
```

### Scroll to:

### Allocated resources:


### You’ll see something like:
```
CPU Requests  1800m / 2000m
Memory Requests  1800Mi / 2048Mi
```

### If it’s near full, that’s why pod is pending.

### Very Common Scenario

### Single-node cluster
### 2 pods already running
### Each requesting 200m CPU

### If node has only 500m or 1 CPU, and other system pods are consuming CPU,
### there may not be enough room for a new replica.

### specially if HPA tried to scale up.

### Possible Causes

### 1️⃣ Node too small
### 2️⃣ Too many pods already
### 3️⃣ HPA scaling beyond node capacity
### 4️⃣ Taints preventing scheduling
### 5️⃣ No metrics-server (less common for pending)

### But 90% of the time it’s insufficient CPU or memory.

## Quick Fix Options

## Option A — Reduce Requests

### Change to:
```
requests:
  cpu: "100m"
  memory: "128Mi"
```

### Then apply again.

## Option B — Increase Node Size

### If on cloud:

### Scale node pool.

## Option C — Add Another Node

### If cluster supports multiple nodes.

## Important Insight

### This is actually good news.

### Your cluster is respecting resource guarantees.

### Without requests, Kubernetes would pack pods recklessly.

### Now it’s behaving like a responsible scheduler.

## Deep SRE Lesson

### When a pod is Pending:

### It’s not broken.

### It’s unscheduled.

### The scheduler is telling you your cluster capacity planning is insufficient.

### That’s not a failure of Kubernetes.

### hat’s math.

### Run this now:
```
kubectl describe pod ott-app-5c465f9597-q7grj
```

### and paste the Events section if you want exact diagnosis.

### Distributed systems don’t hide errors.

### They whisper them in kubectl describe.

<img width="929" height="250" alt="image" src="https://github.com/user-attachments/assets/555960d3-47d6-4509-bbbf-ac0ade6cf5b1" />


### Beautiful. This output tells a story.

### Let’s decode it calmly.

## You showed:

## Allocated resources:
```
CPU Requests:    748m (79%)
CPU Limits:     6043m (642%)

Memory Requests: 1084361600 (36%)
Memory Limits:  7448967680 (253%)
```

### Now here’s the key.

### ubernetes schedules pods based on requests, not limits.

## Your node has:

### ~1000m CPU total (because 748m = 79%)

### That means your node is roughly a 1-core node.

### Now think.

### If HPA tries to scale and add another pod requesting:

### cpu: 200m


### But only ~252m CPU is free (1000m - 748m),

### And system pods are also consuming some,

### The scheduler may not find enough clean allocatable CPU.

## Result?

### Pending.

### Now look at the wild part:

### CPU Limits: 6043m (642%)


### This means you have massively overcommitted CPU limits.

### That’s allowed.

### Limits can exceed 100%.

### equests cannot.

### Scheduling only cares about requests.

### So what’s happening?

### You likely:

 ###    • Have a small single node
 ###    • HPA increased replicas
 ###    • New pod requires 200m
 ###   • Node doesn’t have guaranteed space

### Scheduler refuses.

### Let’s verify capacity precisely.

### Run:
```
kubectl describe node <node-name> | grep -A5 Capacity
```

### You’ll likely see something like:
```
cpu: 1
memory: 2Gi
```

### If it’s a 1 CPU node, you’re already near ceiling.

### Now here’s the deeper lesson.

### Autoscaling pods does nothing if nodes cannot scale.

### You need:

### Pod autoscaling + Node autoscaling.

### If you’re on cloud (AKS, EKS, GKE), enable Cluster Autoscaler.

### Otherwise:

### More pods = Pending.

### Quick Solutions:

## Option 1 — Reduce CPU request

### Change from:

### cpu: 200m


### to

### cpu: 100m


### That doubles pod density.

## Option 2 — Increase node size

### Upgrade VM from 1 core → 2 core.

## Option 3 — Add another node

### Multi-node cluster.

### Now the strategic truth.

### You tried to make your system elastic.

### But elasticity requires room to expand.

### Right now your cluster is like a rubber band nailed to a wall.

## HPA says:
### “Scale up!”

### Scheduler says:
### “With what resources?”

### And the pod sits in Pending.

### If you tell me:

### • Is this AKS?
### • How many nodes?
### • Node size?

### I’ll tell you the exact scaling math for your setup so your cluster behaves like a living organism instead of a cramped box.

<img width="620" height="224" alt="image" src="https://github.com/user-attachments/assets/0f82a662-389a-4be4-8c3d-3fb96592aad3" />


## Now we have real numbers. Good.

### Your node capacity:

```
CPU: 2 cores
Memory: ~4 Gi
```
### So total CPU = 2000m.

### Earlier we saw:

### CPU Requests: 748m (79%)

### That percentage confused you because it was relative to allocatable, not full capacity. Kubernetes keeps some CPU reserved for system components.

### Now let’s think clearly.

### If allocatable CPU is around ~950m–1000m (common in small clusters after system reservation), and 748m is already requested, then you only have ~200–250m free.

## Your new pod requests:

### cpu: 200m


### That’s cutting it extremely close.

### And scheduler needs clean, guaranteed space.

### If even 1m is missing → Pending.

### Kubernetes does not negotiate.

### Let’s confirm allocatable CPU.

## Run:
```
kubectl describe node <node-name> | grep -A5 Allocatable
```

### You’ll likely see something like:
```
cpu: 940m
```

### That’s your real usable CPU.

### Now the math makes sense:

### 748m already used

### 200m new pod
### = 948m

### If allocatable is ~940m → not enough → Pending.

### Now here’s the subtle insight.

### Capacity ≠ Allocatable.

## Kubernetes subtracts CPU for:

kubelet

system daemons

networking

OS

So your 2-core node may only allow ~1 core for pods.

That’s why it feels smaller than expected.

 So what are your options?

## Option 1 — Reduce CPU request

Change to:

### requests:
  cpu: "100m"


That immediately frees scheduling space.

## Option 2 — Increase node size (best long-term)

Upgrade to 4-core node.

## Option 3 — Add another node

If using AKS/EKS/GKE, enable cluster autoscaler.

Because pod autoscaling without node autoscaling is half an elastic system.

Now the philosophical part.

You built HPA.

It tried to scale.

But infrastructure is finite.

Autoscaling is not magic.

It’s mathematics constrained by physics.

Right now your cluster is like a growing city with only one power plant.

If demand increases, lights flicker.

You don’t need more clever YAML.

You need more compute.

### Run this command next and paste the Allocatable section:
```
kubectl describe node <node-name>
```

### That will confirm the exact limit your scheduler is working with.

### And then we can tune it properly instead of fighting invisible ceilings.


## can we increase node cpu requests in GKE ?

But here’s the important distinction that trips people up:

You cannot increase CPU of an existing node in GKE.

Nodes are VMs.
VM size is fixed at creation time.

If you want more CPU, you must:

Change machine type

Or add more nodes

Or enable cluster autoscaling

There is no “resize this running node to 8 cores” button.

Cloud infrastructure is immutable by design.

Now let’s talk about your real goal.

You don’t actually want to “increase CPU requests.”

You want more allocatable CPU available for pods.

That means increasing node capacity.

Here are your options in GKE.


## Option 1 — Upgrade Node Pool Machine Type (Best Long-Term)

### Check your current machine type:

```
gcloud container clusters describe <cluster-name> \
  --zone <zone> \
  --format="value(nodePools.config.machineType)"
```

## It’s probably something like:

```
e2-medium  (2 vCPU)
```

## To upgrade:

### Create a new node pool with bigger machine type:

```
gcloud container node-pools create bigger-pool \
  --cluster=<cluster-name> \
  --zone=<zone> \
  --machine-type=e2-standard-4 \
  --num-nodes=1
```

### Then delete the old small node pool.

### This is the clean way.


## Option 2 — Increase Node Count

### If machine type is fine but capacity is tight:

```
gcloud container clusters resize <cluster-name> \
  --node-pool=<pool-name> \
  --num-nodes=3 \
  --zone=<zone>

```
### More nodes = more total CPU.

### This is horizontal scaling of infrastructure.

## Option 3 — Enable Cluster Autoscaler (Recommended)

## This is the real solution.

### You already enabled HPA for pods.

### Now enable autoscaling for nodes.

```
gcloud container clusters update <cluster-name> \
  --enable-autoscaling \
  --min-nodes=1 \
  --max-nodes=5 \
  --node-pool=<pool-name> \
  --zone=<zone>
```

### Now when HPA scales pods and nodes become full:

### GKE automatically adds new nodes.

### This is how production systems breathe.

### Pod scaling + Node scaling together.

### Now let’s zoom out philosophically for a second.

### Right now your cluster probably has:

1 node
2 CPU

### But Kubernetes system components consume part of that.

### So you don’t really have 2 full CPUs for apps.

### You might have ~1 CPU allocatable.

### That’s why 200m requests start pushing limits quickly.

### Small clusters are educational.
### Production clusters are elastic ecosystems.

### If you tell me:

• Current machine type
• Current node count
• Whether autoscaling is enabled



I’ll calculate how many ott-app pods your cluster can realistically support before saturation.

Because autoscaling is not about YAML.

It’s about capacity mathematics.

If you don’t remember your zone, run:

```
gcloud container clusters list
```
