# Terraform AKS cluster creation 

<img width="1536" height="1024" alt="ChatGPT Image Feb 28, 2026, 06_10_13 PM" src="https://github.com/user-attachments/assets/d75a847c-4899-43a0-b076-f8c801658769" />


<img width="1135" height="517" alt="image" src="https://github.com/user-attachments/assets/4e96273a-14e9-4df9-979a-c96e8eb2e7e6" />

<img width="1199" height="666" alt="image" src="https://github.com/user-attachments/assets/7a320460-2711-4a71-b2e9-69c297d1a3a8" />

This is AKS doing exactly what it is designed to do.

You created:

rg-aks-demo
That is your user-managed resource group.

Then Azure automatically created:

MC_rg-aks-demo_aks-demo-cluster_eastus

That second one is the node resource group.

AKS always does this.

Let’s unpack what’s happening behind the curtain.

When you create an AKS cluster, Azure does two things:

Creates the logical Kubernetes service (control plane) in your resource group

Creates all the infrastructure needed to run nodes in a separate managed resource group

That second resource group contains:

• VM Scale Set
• Load Balancer
• Public IP
• NSG
• Managed Identity
• NICs
• Disks

Those are the real compute resources backing your cluster.

AKS separates them intentionally.

Why?

Because Azure wants:

To manage lifecycle safely

To avoid accidental deletion of internal components

To control upgrades

To enforce platform governance

Think of it like this:

Your RG → Control plane definition
MC_ RG → The actual engine room

The MC_ prefix literally means:
Managed Cluster.

This is completely normal.

Every AKS cluster creates:

```
MC_<yourRG>_<clusterName>_<region>

```

Unless you explicitly override it.

And here’s the interesting part:

If you delete the AKS cluster, Azure automatically deletes the MC_ resource group.

It’s tied to the cluster lifecycle.

Now here’s a subtle DevOps insight.

You should NOT:

Modify resources inside MC_ group manually

Attach custom rules directly there

Delete anything inside it

Because AKS manages it.

If you need custom networking or advanced control, you configure it via Terraform in the AKS resource block — not by editing the MC_ group.

If you want to define your own node resource group name in Terraform, you can do this:

```
resource "azurerm_kubernetes_cluster" "aks" {
  name                = "aks-demo-cluster"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  node_resource_group = "rg-aks-demo-nodes"

  ...
}
```

But even then, Azure still manages its contents.

So nothing is wrong.
Nothing duplicated.
Nothing accidental.

AKS just built the machine room next to your control room.

Cloud systems often look like they are “creating extra things,” but what they are really doing is separating responsibility boundaries.

Infrastructure is polite like that.

If you want, I can now explain how networking flows between:

Jenkins (Central India)
→ AKS Control Plane (East US)
→ Node Resource Group

Because that architecture detail is where real DevOps mastery begins.

# My jenkins vm in central india in different resource and aks cluster in east us different resaource can we connect ? Give me flow chart

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/bdee601a-9966-4428-9b9a-df897b59f14c" />

Yes, you can connect them. Different region. Different resource group. Doesn’t matter. Azure is a giant global network pretending to be geography.

Now let’s do this cleanly and professionally.

First, determine your AKS type. This changes everything.

Run this:

```
az aks show \
  --resource-group rg-aks-demo \
  --name aks-demo-cluster \
  --query "apiServerAccessProfile.enablePrivateCluster"
```

If it returns false → your cluster is public.
If it returns true → it’s private.

I’ll give you both paths.


CASE 1 — AKS is PUBLIC (Most Common, Easiest)

This means the Kubernetes API server has a public endpoint secured by TLS + Azure AD.

Your Jenkins VM just needs:

• Azure CLI
• kubectl
• Proper authentication

### Step 1 — Install tools on Jenkins VM

```
sudo apt update
sudo apt install -y azure-cli
sudo snap install kubectl --classic

```

### Step 2 — Login using Service Principal (Recommended for Jenkins)

Create SP (run once from your machine):

```
az ad sp create-for-rbac \
  --name jenkins-sp \
  --role "Azure Kubernetes Service Cluster User Role" \
  --scopes /subscriptions/<subscription-id>/resourceGroups/rg-aks-demo
```

Save:

appId

password

tenant

Store them in Jenkins credentials.

### Step 3 — Login inside Jenkins pipeline

```
az login --service-principal \
  --username <appId> \
  --password <password> \
  --tenant <tenant>
```

### Step 4 — Get AKS credentials

```
az aks get-credentials \
  --resource-group rg-aks-demo \
  --name aks-demo-cluster
```

### Step 5 — Test connection

```
kubectl get nodes
```

If nodes show up → connection successful.

That’s it. Region difference is irrelevant. It goes over HTTPS like any API call.

CASE 2 — AKS is PRIVATE ( in our case its public)

Now the API server lives inside a VNet in East US.

Your Jenkins VM in Central India cannot reach it over internet.

You must create network connectivity.

# Option A (Recommended) — Global VNet Peering

### Step 1 — Identify:
• Jenkins VNet (Central India)
• AKS VNet (East US — usually created automatically)

### Step 2 — Create peering both ways:

Jenkins VNet → AKS VNet
AKS VNet → Jenkins VNet

Enable:
• Allow forwarded traffic
• Allow virtual network access

### Step 3 — Ensure NSG allows outbound 443

### Step 4 — Ensure DNS resolution works for private endpoint

Then run:

```
az login --service-principal ...
az aks get-credentials ...
kubectl get nodes
```

Now traffic flows privately across Azure backbone network.

Security Best Practice

Never use interactive az login in Jenkins.
Always use Service Principal or Managed Identity.

Even better architecture:

Jenkins VM with Managed Identity
Grant role:
Azure Kubernetes Service Cluster User Role

Then no passwords required.

Architecture Flow (Mental Model)

Jenkins VM
→ Azure AD authentication
→ AKS API endpoint (Public or Private)
→ Control plane
→ Node pool (VM Scale Set)

Resource groups do not block connectivity.
Regions do not block connectivity.
Networking design and RBAC decide access.

If you tell me whether your cluster is public or private, I can give you the exact minimal commands for your setup without unnecessary configuration.



