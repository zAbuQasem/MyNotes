# Navigation
- [**Installing-and-runinng-minikube**](#Installing-and-runinng-minikube)
- [**EKS**](#EKS)
- [**NameSpaces**](#NameSpaces)
- [**Managing-Pods**](#Managing-Pods)
- [**YAML**](#YAML)
	- [Generate-template](#Generate-template)
	- [Kubectl-manual](#Kubectl-manual)
- [**Replicas**](#Replicas)
	- [Scaling-Replicas](#Scaling-Replicas)
- [**Deployments**](#Deployments)
	- [Deployment-strategies](#Deployment-strategies)
	- [References](#References)
- [**Services**](#Services)
	- [NodePort](#NodePort)
	- [ClusterIp](#ClusterIp)
	- [LoadBalancer](#LoadBalancer)
- [**Scheduling**](#Scheduling)
	- [Taints-and-Tolerations](#Taints-and-Tolerations)
	- [NodeSelector-and-NodeAffinity](#NodeSelector-and-NodeAffinity)
	- [Daemon-Sets](#Daemon-Sets)
- [**Monitoring**](#Monitoring)
- [**Jobs-CronJobs**](#Jobs-CronJobs)
- [**Multi-Containers**](#Multi-Containers)
- [**Secrets**](#Secrets)
- [**initContainer**](#initContainer)
- [**Maintenance**](#Maintenance)
	- [Software-Releases](#Software-Releases)
	- [Cluster-Upgrade](#Cluster-Upgrade)
- [**Security**](#Security)
	- [API-Groups](#API-Groups)
	- [Authorization](#Authorization)
	- [RBAC](#RBAC)
	- [ServiceAccounts](#ServiceAccounts)
	- [ImageSecurity](#ImageSecurity)
	- [SecurityContexts](#SecurityContexts)
	- [NetworkPolicy](#NetworkPolicy)
		- [Ingress](#Ingress)
		- [Egress](#Egress)
- [**Volumes-Mounts**](#Volumes-Mounts)
	- [Pod-Volume](#Pod-Volume)
	- [Persistent-Volume](#Persistent-Volume)
		- [Reclaiming](#Reclaiming)
			- [Retain](#Retain)
			- [Delete](#Delete)
			- [Recycle](#Recycle)
	- [Persistent-Volume-Claim](#Persistent-Volume-Claim)
	- [Security-Risks](#Security-Risks)
		- [HostPath](#HostPath)
	- [StorageClass](#StorageClass)
	- [TLDR](#TLDR)

# Installing-and-running-minikube
```bash
# On debian x86_64
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# On windows
choco install minikube

# Start minikube with virtualbox driver
minikube start --driver=virtualbox

# If you faced some issues related to VTX on windows 11 (while it's enabled) 
minikube start --no-vtx-check --driver virtualbox
```
> **Important Notes**:
> - On failure run `minikube delete && minikube start` if it didn't work then follow the traceback instructions
> - [**Click me for other distros installation guide**](https://minikube.sigs.k8s.io/docs/start/)
---
# EKS
Make sure to have the required privileges [Minimum Required](https://eksctl.io/usage/minimum-iam-policies/)
1. Creating a Cluster
```bash
eksctl create cluster --name DemoCluster --fargate
```

2. Configure your cluster with kubectl
```bash
aws eks update-kubeconfig --name DemoCluster
```

3. Verify
```bash
# Look for aws-auth
kubectl get configmap -A
# -A = --all-namespaces
```
---
# NameSpaces

- Create a namespace
```bash
kubectl create namespace <NAMESPACE>
```

- List namespaces
```bash
kubectl get namespaces
```

- Getting namespace information
```bash
kubectl describe namespaces # All namespaces
kubectl describe namespaces <NAMESPACE>
```

- Delete a namespace
```bash
kubectl delete <NAMESPACE>
```
> **Important note**: Deleting a namespace will **delete everything** within it.
---
# Managing-Pods

**Control and manage your Kubernetes pods efficiently using labels and selectors.**

## **Running a Container in a Pod**

**Deploy a pod with a specific container image.**

```bash
# Images are pulled from Docker Hub
kubectl run nginx --image=nginx
```

## **Listing Pods**

**View pods in various ways using labels and selectors.**

```bash
# List all pods in the current namespace
kubectl get pods

# List all pods with detailed information
kubectl get pods -o wide

# List pods from a specific namespace
kubectl get pods -n <Namespace>

# List all pods across all namespaces
kubectl get pods --all-namespaces

# Get all container names within a specific pod
kubectl get pods <POD> -n <NAMESPACE> -o jsonpath='{.spec.containers[*].name}'

# Describe a specific pod for detailed information
kubectl describe pods <POD> -n <NAMESPACE>
```

> **Note:** The **Ready** column shows `1/2` meaning 1 running container out of 2 total containers in the pod.

## **Using Labels and Selectors**

**Organize and filter pods using labels and selectors for better management.**

### **Adding Labels to a Pod**

**Assign key-value pairs to pods for identification and organization.**

```bash
# Add a label to an existing pod
kubectl label pod <PodName> app=frontend

# Example:
kubectl label pod nginx app=webserver
```

### **Listing Pods with Specific Labels**

**Filter and view pods based on their labels using selectors.**

```bash
# List pods with the label app=webserver
kubectl get pods -l app=webserver

# List pods with multiple labels
kubectl get pods -l app=webserver,env=production
```

### **Selecting Pods with Labels in YAML**

**Use label selectors in YAML configurations for deployments and services.**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend-service
spec:
  selector:
    app: webserver
  ports:
    - protocol: TCP
      port: 80
      targetPort: 8080
```

**Explanation:**

- **selector:** Matches pods with the label `app=webserver` to route traffic through the service.

## **Change Pod Specification**

**Update pod configurations, such as changing container images.**

```bash
# Change the image of a container in a pod
kubectl set image <RESOURCE/RESOURCE_NAME> <CONTAINER_NAME>=<NEW_IMAGE_NAME>

# Example:
kubectl set image pod/redis-container redis-container=redis:latest
```

## **Getting Detailed Pod Information**

**Retrieve comprehensive details about pods for troubleshooting and monitoring.**

```bash
# Describe all pods in the current namespace
kubectl describe pod

# Describe a specific pod
kubectl describe pod <PodName>
```

## **Delete a Pod**

**Remove pods when they are no longer needed.**

```bash
# Delete a specific pod by name
kubectl delete pod <PodName>

# Delete pods using a YAML configuration file
kubectl delete -f <Pod.yml>
```

> **Note:** File extensions `.yml` or `.yaml` are interchangeable. However, it's advised for Windows users to use `.yml`.

## **Quick Reference: Labels and Selectors**

- **Labels:**
    - **Purpose:** Attach metadata to pods (key-value pairs) for organization and selection.
    - **Usage:** `kubectl label pod <PodName> key=value`
- **Selectors:**
    - **Purpose:** Query and filter pods based on labels.
    - **Usage:** `kubectl get pods --selector key=value,key2=value2`
- **Best Practices:**
    - **Consistent Labeling:** Use meaningful and consistent labels across your pods.
    - **Combine Labels:** Utilize multiple labels for more granular selection.
    - **Use Labels in Services:** Leverage labels to connect services with the appropriate pods.

### **Example Workflow:**

1. **Run a Pod with a Label:**
```bash
kubectl run frontend --image=nginx --labels="app=frontend,env=production"
```
2. **List All Frontend Pods:**
```bash
kubectl get pods --selector app=frontend
 # Get all objects with the label app=frontend
kubectl get all --selector app=frontend
```
3. **Describe a Frontend Pod:**
```bash
kubectl describe pod frontend
```
4. **Update the Frontend Pod Image:**
```bash
kubectl set image pod/frontend frontend=nginx:latest
```
5. **Delete the Frontend Pod:**
```bash
kubectl delete pod frontend
```

### **Reference**
- [Assign Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
- [Using Labels and Selectors](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/)
- [kubectl Command Reference](https://kubernetes.io/docs/reference/kubectl/)

---
# YAML
It is a good practice to declare resource requests and limits for both [memory](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/) and [cpu](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/) for each container. This helps to schedule the container to a node that has available resources for your Pod, and also so that your Pod does not use resources that other Pods needs.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: abuqasem-firstpod # Pod name - Always lowercase
  labels: 
    app: myapp
    type: server
    env: production
    tier: frontend
spec:
  containers:
  - name: abuqasem-nginx-container # Container name -Always lowercase
    image: nginx
     env:
       - name: ENVIRONMENT_VARIABLE_PASSWORD
         value: "SuperSecretPassword"
    resources:
      limits:
        memory: 512Mi
        cpu: "1"
      requests:
        memory: 256Mi
        cpu: "0.2"
```
-  **`apiVersion`** - Which version of the Kubernetes API you're using to create this object
-   **`kind`** - What kind of object you want to create
-   **`metadata`** - Data that helps uniquely identify the object, including a `name` string, `UID`, and optional `namespace`
-   **`spec`** - What state you desire for the object

## Generate-template
You can let kubectl generate a yaml file for you by using the `--dry-run` option
- **Examples**
```bash
1- kubectl run nginx --image nginx --dry-run client -o yaml
2- kubectl create deployment --image=nginx nginx --dry-run=client -o yaml
3- kubectl create deployment --image=nginx nginx --replicas=4 --dry-run=client -o yaml 
```

## Kubectl-manual
Get the usage of a command
```sh
kubectl explain <Object>
kubectl explain pod
kubectl explain deployment
...etc
```
## References:
- [**YAML Structure Explained**](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started)
- [**YAML explained - Great resource**](https://learnk8s.io/templating-yaml-with-code#introduction-managing-yaml-files)
- [**Kubernetes for the Absolute beginners**](https://www.udemy.com/share/1013LO3@Wfs8GSg7yXNJf2pneg2OgTWAIXOkIF5-hguWhEg51WfgYYb7vWENhvP50PHfuWji/)
---
# Replicas
- Create `ReplicationController`
```yaml
apiVersion: v1
kind: ReplicationController
metadata:
  name: myfirst-replica-controller
spec:
  replicas: 3
  template:
    metadata:
      name: nginx
      labels:
        app: nginx-1
    spec:
      containers:
        - name: nginx-contanier-1
          image: nginx
          ports:
            - containerPort: 9001
```

```bash
kubectl create -f <File.yml>
```

- Create `ReplicaSet`
```yaml
apiVersion: v1
kind: ReplicaSet
metadata:
  name: myfirst-replica-controller
spec:
  replicas: 3
  selector:   # A Must in ReplicaSet
    matchLabels:
        type: frontend
  template:
    metadata:
      name: nginx
      labels:
        app: nginx-1
    spec:
      containers:
        - name: nginx-contanier-1
          image: nginx
          ports:
            - containerPort: 9001-
```

```bash
kubectl create replicaset -f <File.yml>
```

> **Note**: Selectors are mandatory in replicasets, becuase they will match any non-replicated pod based on the labels and will include them in the replecation.


- List `ReplicaSet`
```bash
kubectl get replicaset
```

- Edit a ReplicaSet
```bash
kubectl edit rs/<SET>
```

- Describe replicasets
```bash
kubectl describe replicasets/<SET>
```

- Delete replicasets
```bash
kubectl delete replicasets/<SET>
```

## Scaling-Replicas

- Edit the Yaml file then
```bash
kubectl replace -f <File.yml>
```

- Scale directly from the cli
```bash
kubectl scale --replicas=<NUMBER> -f <File.yml>
```

- Scale from the cli as a resource
```bash
kubectl scale --replicas=<NUMBER> replicaset/<NAME>
```

- Cheat cmd to delete all pods within a replicaset
```bash
kubectl scale rs/<SET> --replicas=0
```
---
# Deployments

![](https://i.imgur.com/GgInLMb.png)

- Create a deployment
```bash
kubectl create -f <File.yml>
```

- Apply an update to a deployment
```bash
kubectl apply -f <File.yml>
```

- Get rollout status
```bash
kubectl rollout status deployment/<DEPLOYMENT>
kubectl rollout history deployment/<DEPLOYMENT>
```
> **Note**:
> In order to view the rollout history, comsider adding `--record` option when applying or doing updates via cli.

- Rollback to a previous version
```bash
kubectl rollout undo 
```

## Deployment-strategies

**Manage how updates are deployed to your applications in Kubernetes using different strategies.**

### **1. Recreate Strategy**

- **Description:**
    - Deletes all existing pods (`ReplicaSet`) before creating new ones with the updated configuration.
- **Use Cases:**
    - Suitable for development or staging environments where downtime is acceptable.
    - Ideal for applications that **cannot** handle multiple versions running simultaneously.
- **Pros:**
    - Simple to implement.
- **Cons:**
    - Causes downtime as all old pods are removed before new ones are available.
    - Not recommended for production environments where uptime is critical.
- **YAML Example:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
	type: Recreate
  selector:
	matchLabels:
	  app: my-app
  template:
	metadata:
	  labels:
		app: my-app
	spec:
	  containers:
	  - name: my-app-container
		image: my-app:v2
```
### **2. RollingUpdate Strategy**

- **Description:**
    - Gradually replaces old pods with new ones, ensuring that some pods are always running during the update process.
- **Use Cases:**
    - Ideal for stateful applications that can handle data rebalancing.
    - Suitable for production environments where minimizing downtime is essential.
- **Pros**:
    - Minimizes downtime by keeping some pods running during updates.
    - Allows for smoother transitions and gradual rollouts.
- **Cons:**
    - Rollouts and rollbacks can take time.
    - Managing multiple API versions can be complex.
    - Limited control over traffic distribution during updates.
- **YAML Example:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  replicas: 3
  strategy:
	type: RollingUpdate
	rollingUpdate:
	  maxSurge: 2      # Maximum number of pods that can be created above the desired replicas
	  maxUnavailable: 0# Maximum number of pods that can be unavailable during the update
  selector:
	matchLabels:
	  app: my-app
  template:
	metadata:
	  labels:
		app: my-app
	spec:
	  containers:
	  - name: my-app-container
		image: my-app:v2
```

### **3. Additional Deployment Strategies (Advanced)**

While **Recreate** and **RollingUpdate** are the primary strategies in Kubernetes, advanced deployment scenarios may require more sophisticated approaches:

- **Blue-Green Deployment:**
    - **Description:** Run two identical environments (blue & green). Switch traffic from blue to green once the new version is ready.
    - **Pros:** Zero downtime and easy rollback.
    - **Cons:** Requires double the resources.
- **Canary Deployment:**
    - **Description:** Gradually roll out the new version to a subset of users before a full-scale release.
    - **Pros:** Reduces risk by testing the new version with limited traffic.
    - **Cons:** More complex to manage traffic routing.

> **NOTE:** These advanced strategies often require additional tooling or service mesh integrations.

### **Rollout Commands**

**Manage and monitor the deployment rollout process using these `kubectl` commands.**

- **Check Rollout Status:**
    
```bash
kubectl rollout status deployment/<DEPLOYMENT_NAME>
```
    
- **View Rollout History:**
    
```bash
kubectl rollout history deployment/<DEPLOYMENT_NAME>
```
    
- **Undo/Rollback to Previous Revision:**
    
```bash
kubectl rollout undo deployment/<DEPLOYMENT_NAME>
```
    
- **Pause a Rollout:**
    
```bash
kubectl rollout pause deployment/<DEPLOYMENT_NAME>
```
    
- **Resume a Paused Rollout:**
    
```bash
kubectl rollout resume deployment/<DEPLOYMENT_NAME>
```
    
- **Restart a Deployment:**
    
```bash
kubectl rollout restart deployment/<DEPLOYMENT_NAME>
```
    
- **View Detailed Deployment Information:**
    
```bash
kubectl describe deployment/<DEPLOYMENT_NAME>
```

- **Scale a Deployment:**

```bash
kubectl scale deployment/<DEPLOYMENT_NAME> --replicas=<NUMBER_OF_REPLICAS>
```

- **Update Deployment Image:**

```bash
kubectl set image deployment/<DEPLOYMENT_NAME> <CONTAINER_NAME>=<NEW_IMAGE>
```

### **Example Workflow: RollingUpdate Deployment**

1. **Create a Deployment:**
    
```bash
kubectl create deployment my-app --image=my-app:v1 --replicas=3
```
    
2. **Check Deployment Status:**
    
```bash
kubectl rollout status deployment/my-app
```
    
3. **Update the Deployment to a New Version:**
    
```bash
kubectl set image deployment/my-app my-app-container=my-app:v2
```
    
4. **Monitor the Rollout Progress:**
    
```bash
kubectl rollout status deployment/my-app
```
    
5. **View Rollout History:**
    
```bash
kubectl rollout history deployment/my-app
```
    
6. **Rollback to Previous Version if Needed:**
    
```bash
kubectl rollout undo deployment/my-app
```
    
7. **Scale the Deployment:**
    
```bash
kubectl scale deployment/my-app --replicas=5
```

### **References**

- [Kubernetes Deployment Strategies](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/#deployment-strategies)
- [kubectl Rollout Command Reference](https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#rollout)
- [Advanced Deployment Techniques](https://blog.container-solutions.com/kubernetes-deployment-strategies)

---
# Services

## NodePort

A service that forwards traffic from a node to a pod, so users can access the application in a pod using the node's IP and specified port.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  labels:
    app: myapp
    type: front-end
spec:
  type: NodePort
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008 # A port we will connect to
  selector:
    app: myapp
```
### Imperative Commands:
- Create a NodePort service:
```bash
kubectl create -f <file.yml>
```
- Expose an existing deployment as a NodePort service:
```bash
kubectl expose deployment <deployment-name> --type=NodePort --port=80 --target-port=80
```
- Get the service details:
```bash
kubectl get svc myapp-service
```
- Get the service URL:
```bash
# Minikube
minikube service <service-name> --url

# Kubernetes cluster
kubectl port-forward svc/<service-name> LOCALPORT:REMOTEPORT -n <namespace>
```
## Best Practices:

1. Avoid hardcoding `nodePort` values unless necessary. Let Kubernetes assign ports dynamically when possible.
2. Use `NodePort` only when external access to the cluster is minimal or specific to development environments.
3. Always validate the service's selector matches the correct pods.

### Troubleshooting:

1. **Service not reachable on the `nodePort`:**
    - Ensure the correct firewall rules are configured to allow traffic to the specified `nodePort`.
    - Verify the pod's readiness status:
```bash
kubectl get pods -o wide
```

2. **Traffic not routing to the intended pod:**
    - Confirm that the `selector` labels in the service match the labels on the pods:
```bash
kubectl describe svc myapp-service
```
## ClusterIP

Exposes the service on a cluster-internal IP. This service type is only reachable within the cluster.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: back-end
  labels:
    app: myapp
    type: back-end
spec:
  type: ClusterIP
  ports:
    - targetPort: 80
      port: 80
  selector:
    app: myapp
```

### Imperative Commands:

- Create a ClusterIP service:
```bash
kubectl create -f <file.yml>
```
- Expose an existing deployment as a ClusterIP service:
```bash
kubectl expose deployment <deployment-name> --type=ClusterIP --port=80 --target-port=80
```
## Best Practices:

1. Use `ClusterIP` for internal communication between microservices.
2. Ensure network policies are implemented to secure internal service communication.

### Troubleshooting:

1. **Pod not able to connect to the service:**
	- Check DNS resolution for the service: `nslookup <service-name>`.`
	- Ensure pods are using the correct `selector`.

2. **Load distribution issues:**
    - Verify the endpoints of the service: 
```bash
kubectl get endpoints <service-name>
```
## LoadBalancer

Exposes the service externally using a cloud provider's load balancer.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
  labels:
    app: myapp
spec:
  type: LoadBalancer
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008
  selector:
    app: myapp
```

### Imperative Commands:

- Create a LoadBalancer service:
```bash
kubectl create -f <file.yml>
```
- Expose an existing deployment as a LoadBalancer service:
```bash
kubectl expose deployment <deployment-name> --type=LoadBalancer --port=80 --target-port=80
```

## Best Practices:

1. Use `LoadBalancer` for external-facing services in production on cloud platforms.
2. Regularly monitor the associated cloud resources for cost and performance.

### Troubleshooting:

1. **LoadBalancer IP not assigned:**
    
    - Verify if the cloud provider's load balancer controller is running.
    - Check the service status:  
```bash
kubectl describe svc <service-name>
```
2. **Service inaccessible from the external IP:**
    - Ensure external traffic is allowed in the cloud provider's security groups or firewall.

---
# Scheduling
What if we want to manually schedule pods and assign them to nodes, instead of leaving it to be automated by the scheduler.
we have to add `nodeName` atrribute to the `spec`

```yaml
apiVersion: v1
kind: ReplicaSet
metadata:
  name: myfirst-replica-controller
spec:
  nodeName: abuqasem-node
  replicas: 3
  selector:   # A Must in ReplicaSet
    matchLabels:
        type: frontend
  template:
    metadata:
      name: nginx
      labels:
        app: nginx-1
    spec:
      containers:
        - name: nginx-contanier-1
          image: nginx
          ports:
            - containerPort: 9001
```
---
## Taints-and-Tolerations

- **Taints:** Applied to Kubernetes nodes to **mark them as unsuitable** for hosting any pods by default. A taint has three parts:    
    1. **Key**: Identifies the taint.
    2. **Value**: Provides additional information.
    3. **Effect**: Determines what happens to pods that don’t tolerate the taint (`NoSchedule`, `PreferNoSchedule`, or `NoExecute`).
- **Tolerations:** Applied to pods to **allow them to be scheduled** on nodes with matching taints. A toleration specifies:
    1. **Key and Value**: Must match the node’s taint.
    2. **Effect**: Should align with the taint’s effect.
    3. **Operator** and **TolerationSeconds** (optional): Define how the toleration matches and for how long.

**Purpose:**
- **Control Pod Placement:** Ensure that only specific pods run on certain nodes, useful for dedicating nodes to particular workloads, handling specialized hardware, or isolating sensitive applications.
- **Enhance Cluster Efficiency:** Prevent unsuitable pods from being scheduled on inappropriate nodes, maintaining optimal resource usage and performance.
**Example Use Case:**
- **Dedicated GPU Nodes:**
    - **Taint the GPU node:** `gpu=true:NoSchedule`
    - **Tolerate in GPU-enabled pods:** Pods requiring GPUs add a toleration for `gpu=true`.

This setup ensures that only pods needing GPU resources are placed on GPU-equipped nodes, keeping other nodes free for general workloads.

- Taint a node
```sh
kubectl taint nodes <NODE> KEY=VALUE:EFFECT
kubectl taint nodes node1 key1=value1:NoSchedule
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  tolerations:
  - key: "key1"
    value: "value1"
    operator: "Exists"
    effect: "NoSchedule"
```

**Usable effects:**
- `NoSchedule`
- `PreferNoSchedule`
- `NoExecute`

- Running a pod with tolerations
```sh
# Image name: nginx
# Key: spray
# Value: mortein
# Effect: NoSchedule
kubectl run nginx --image=nginx --restart=Never --overrides='{"apiVersion":"v1","spec":{"tolerations":[{"key":"spray","operator":"Equal","value":"mortein","effect":"NoSchedule"}]}}'
```

**Remove a taint**
To remove a taint, use the `kubectl taint` command with the taint specification followed by a `-` (dash) at the end.
```sh
kubectl taint nodes <node-name> <key>=<value>:<effect>-
kubectl taint nodes node01 spray=mortein:NoSchedule-
kubectl taint nodes controlplane node-role.kubernetes.io/control-plane:NoSchedule-
```


> **Note:**
	There are two special cases:
	An empty `key` with operator `Exists` matches all keys, values and effects which means this will tolerate everything.
	An empty `effect` matches all effects with key `key1`.

### Example
For example, imagine you taint a node like this
```shell
kubectl taint nodes node1 key1=value1:NoSchedule
kubectl taint nodes node1 key1=value1:NoExecute
kubectl taint nodes node1 key2=value2:NoSchedule
```

And a pod has two tolerations:
```yaml
tolerations:
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoSchedule"
- key: "key1"
  operator: "Equal"
  value: "value1"
  effect: "NoExecute"
```


In this case, the pod will not be able to schedule onto the node, because there is no toleration matching the third taint. But it will be able to continue running if it is already running on the node when the taint is added, because the third taint is the only one of the three that is not tolerated by the pod.

### Reference
- https://kubernetes.io/docs/concepts/scheduling-eviction/taint-and-toleration/

---
## NodeSelector-and-NodeAffinity

**Control where pods run by matching node labels.**
### **NodeSelector**

**Simple way** to assign pods to specific nodes based on labels.

**Use Case:** When you have straightforward label matching without complex rules.

**Example:**

This pod **must** run on nodes labeled with `disktype=ssd`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-selector
spec:
  nodeSelector:
    disktype: ssd
  containers:
    - name: nginx
      image: k8s.gcr.io/pause:2.0
```
### **NodeAffinity**

**Advanced way** to control pod placement with more flexible and expressive rules.

**Use Case:** When you need complex scheduling rules, such as multiple conditions or preference weighting.

**Example:**

This pod **must** run on nodes in the `antarctica-east1` or `antarctica-west1` zones and **prefers** nodes with `another-node-label-key: another-node-label-value`.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
  # Required: Must match one of these zones
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
              - antarctica-east1
              - antarctica-west1
  # Preferred: Prefer nodes with this label
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
              - another-node-label-value
  containers:
    - name: nginx
      image: k8s.gcr.io/pause:2.0
```

### **Combined Example**

You can use both **NodeSelector** and **NodeAffinity** in the same pod for simple and advanced scheduling rules.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: combined-scheduling
spec:
  nodeSelector:
    disktype: ssd
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: environment
            operator: In
            values:
              - production
              - staging
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 2
        preference:
          matchExpressions:
          - key: gpu
            operator: Exists
  containers:
    - name: nginx
      image: k8s.gcr.io/pause:2.0
```

**Explanation:**

- **nodeSelector:**
    - **disktype: ssd**: Pod **must** be on nodes with `disktype=ssd`.
- **nodeAffinity:**
    - **requiredDuringSchedulingIgnoredDuringExecution:**
        - **environment In [production, staging]**: Pod **must** be in `production` or `staging` environments.
    - **preferredDuringSchedulingIgnoredDuringExecution:**
        - **gpu Exists**: Pod **prefers** nodes that have a `gpu` label.
### **Other NodeAffinity Operators**

NodeAffinity uses various **operators** to define how labels should match. Here are the common operators:

- **In**
    - **Use When:** You want to include nodes that have specific label values.
    - **Example:**
```yaml
- key: "zone"
  operator: In
  values:
	- "us-east-1a"
	- "us-east-1b"
```
        
- **NotIn**
    - **Use When:** You want to exclude nodes that have certain label values.
    - **Example:**
```yaml
- key: "diskType"
  operator: NotIn
  values:
	- "hdd"
```

- **Exists**
    - **Use When:** You require nodes to have a specific label, regardless of its value.
    - **Example:**
```yaml
- key: "backup"
  operator: Exists
```

- **DoesNotExist**
    - **Use When:** You want to ensure nodes do not have a particular label.
    - **Example:**
```yaml
- key: "maintenance"
  operator: DoesNotExist
  ```
- **Gt (Greater Than)**
    - **Use When:** Label values are numerical, and you need nodes with values above a threshold.
    - **Example:**
 ```yaml
- key: "memory"
  operator: Gt
  values:
	- "16"
```

- **Lt (Less Than)**
    - **Use When:** Label values are numerical, and you need nodes with values below a threshold.
    - **Example:**
```yaml
- key: "cpu"
  operator: Lt
  values:
	- "8"
```

### **Quick Notes**

- **NodeSelector:**
    - **Pros:** Simple and easy for basic label matching.
    - **Cons:** Limited to exact matches; lacks flexibility for complex rules.
- **NodeAffinity:**
    - **Pros:** Highly flexible with multiple operators (`In`, `NotIn`, `Exists`, `DoesNotExist`, `Gt`, `Lt`), supports preferred rules.
    - **Cons:** More complex to configure compared to `nodeSelector`.
- **When to Use:**
    - Use **NodeSelector** for straightforward scheduling needs.
    - Use **NodeAffinity** when you need advanced scheduling rules or prefer certain nodes over others.

### **Reference**

- [Assign Pods to Nodes](https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/)
---
## Daemon-Sets
ReplicaSet ensures that the number of pods of an application is running on the correct scale as specified in the conf file. Whereas in the case of DaemonSet it will ensure that **one copy of pod defined in our configuration will always be available on every worker node.**
```yml
apiVersion: v1
kind: DaemonSet
metadata:
  name: myfirst-replica-controller
spec:
  replicas: 3
  selector:   # A Must in ReplicaSet
    matchLabels:
        type: frontend
  template:
    metadata:
      name: nginx
      labels:
        app: nginx-1
    spec:
      containers:
        - name: nginx-contanier-1
          image: nginx
          ports:
            - containerPort: 9001
```

---
# Monitoring
Using Built-In metrics server (in memory solution).
- Installing Metrics-Server
```bash
# Minikube
minikube addons enable metrics-server

# Cluster
Check: https://github.com/kubernetes-sigs/metrics-server
```

- Viewing data
```bash
kubectl top node
kubectl top pod
```

- Viewing logs
```bash
kubectl logs -f <PodName> <ContainerName>
# -f: View live
# ContianerName: Only mandatory if your pod had multiple containers
```
---
# Jobs-CronJobs

## **Key Differences Between Jobs and CronJobs**:

| Feature            | Job                              | CronJob                                  |
| ------------------ | -------------------------------- | ---------------------------------------- |
| **Purpose**        | One-time task                    | Recurring/scheduled task                 |
| **Execution**      | Runs immediately or when created | Runs based on schedule (Cron syntax)     |
| **Concurrency**    | Handles one-off parallelism      | Controls concurrency for recurring tasks |
| **Pod Management** | Pods terminate upon completion   | Pods created as per the schedule         |

## **1. Job Template**

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: advanced-job
spec:
  parallelism: 3  # Number of pods running in parallel.
  completions: 5  # Total number  of pods to complete the job successfully.
  backoffLimit: 4 # Number of retries before marking the job as failed.
  activeDeadlineSeconds: 120 #  Maximum time for the job to run.
  ttlSecondsAfterFinished: 300 # Time to live for completed pods.
  podFailurePolicy:
    rules:
    - action: Ignore
      onExitCodes:
        operator: In
        values: [1, 2]
  template:
    metadata:
      labels:
        app: my-job
    spec:
      containers:
      - name: my-container
        image: busybox
        command: ["sh", "-c", "echo Hello; sleep 5; exit 0"]
      restartPolicy: Never
```

#### **Imperative Command to Create a Job**:

```bash
kubectl create job simple-job --image=busybox -- echo "Hello, Kubernetes!"
```
- **View Job details**:
```bash
kubectl get jobs
kubectl describe job simple-job
```
- **Delete a Job**:
```bash
kubectl delete job simple-job
```
- **Forcefully Create Pods for a Job**:
```bash
kubectl scale job simple-job --replicas=5
```
## **2. CronJob Template**

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: scheduled-task
spec:
  schedule: "*/5 * * * *" # Every 5 minutes
  jobTemplate:
    spec:
      completions: 1
      parallelism: 1
      backoffLimit: 3
      template:
        metadata:
          name: cronjob-task
        spec:
          containers:
          - name: cronjob-container
            image: busybox
            command: ["echo", "Running a scheduled task!"]
          restartPolicy: Never
  successfulJobsHistoryLimit: 3
  failedJobsHistoryLimit: 1
```

#### **Imperative Command to Create a CronJob**:

```bash
kubectl create cronjob scheduled-task --image=busybox --schedule="*/5 * * * *" -- echo "Running a scheduled task!"
```
- **View CronJob details**:
```bash
kubectl get cronjobs
kubectl describe cronjob scheduled-task
```
- **Delete a CronJob**:
```bash
kubectl delete cronjob scheduled-task
```
- **Trigger a CronJob manually**:
```bash
kubectl create job --from=cronjob/scheduled-task manual-run
```
## **Best Practices**:

1. **For Jobs**:
    - Use `backoffLimit` to control retries and avoid infinite loops.
    - Define resource requests/limits for Pods to prevent overloading nodes.
2. **For CronJobs**:
    - Test the Job template separately to ensure it behaves as expected.
    - Keep the `successfulJobsHistoryLimit` and `failedJobsHistoryLimit` reasonable to avoid clutter.
    - Use descriptive names for CronJobs for better identification.
3. **Monitoring**:
    - Monitor Job and CronJob statuses using `kubectl get jobs` and `kubectl get cronjobs`.
    - Enable logging to debug failures effectively.
---
# Secrets
- Imperative method
```yaml
kubectl create secret generic <SecretName> --from-lietral=<KEY>=<VALUE>
kubectl create secret generic <SecretName> --from-file=<FileName>
```
- Declarative method
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: db-secret
data:
  DB_Host: c3FsMDE=
  DB_User: cm9vdA==
  DB_Password: cGFzc3dvcmQxMjM= 
```
**Secrets can be injected into pods in 3 different ways:**
- ENV
```yml
envFrom:
  - secretRef:
        name: app-config
```
- Single env
```yml
env:
  - name: DB_PASSWORD
    valueFrom:
      secretKeyRef:
        name: app-secret
        key: DB_PASSWORD
```

- Volume
```yml
volumes:
- name: app-secret-volume
  secret:
    secretName: app-secret
```
 > **Note**: When mounting secrets as volumes, each key will be a separate file in the /opt/\<SecretName\> folder

---
# Multi-Containers

**There are 3 common patterns:**
- **Sidecar pattern**: An extra container in your pod to **enhance** or **extend** the functionality of the main container.
- **Ambassador pattern**: A container that **proxy the network connection** to the main container.
- **Adapter pattern**: A container that **transform output** of the main container.
# initContainer
A Container that runs a defined task once when the pod is started. 
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: myapp-pod
  labels:
    app: myapp
spec:
  containers:
  - name: myapp-container
    image: busybox:1.28
    command: ['sh', '-c', 'echo The app is running! && sleep 3600']
  initContainers:
  - name: init-myservice
    image: busybox
    command: ['sh', '-c', 'git clone <some-repository-that-will-be-used-by-application>']
```
---
# Maintenance
The node eviction timeout is triggered when a node goes down for 5 mins. This could be changed by the following command
```bash
kube-controller-manager --pod-eviction-timeout=5m0s
```

When a node is gone down we don't know for sure if it's going to be back online so we can drain the pods from it to another nodes. (Terminated from the node and recreated on another node).

The following command also marks the node as non-schedulable.
```bash
kubectl drain node-1
```

The following command will be marked as non-schedulable, So no pods will be created on it without draining the pods.
```bash
kubectl cordon node-1
```

To remove the mark
```bash
kubectl uncordon node-1
```

> -  Pods will not fall over to their main node automatically, But when pods gets rescheduled they will be created on it
> - Pods that aren't part of a replicaset isn't drained, you have to use --force

## Software-Releases
Software version in k8s consists of 3 parts:
```txt
v1.11.3
Major.Minor.Patch

# Minor = [Features,Functionalities]
# Patch = [BugFixes]
```
>**Notes**: 
>Kubernetes only support 3 minor releases.
>It's advised to upgrade version 1 minor version at a time.

## Cluster-Upgrade

1. Upgrade `Kubeadm`
```bash
apt-get upgrade kubeadm=<Version>
kubeadm upgrade apply <Version>
systemctl restart kubelet
kubectl get nodes # To verify
```

2.  Upgrade `Kubelet` on the master node
```bash
sudo apt-get upgrade kubelet=<Version>
sudo systemctl restart kubelet
```

3. Upgrading the working nodes (For every node in the cluster)
```
kubectl drain <Node>
apt-get upgrade kubeadm=<Version>
apt-get upgrade kubelet=<Version>
kubeadm upgrade node config --kubelet-version <Version>
systemctl restart kubelet
kubectl uncordon <Node> 
```
## Backup-and-Restore

- Backup resource configs
```bash
kubectl get all -A -o yaml > all-deploy-services.yml
```

- Backup ETCD
```bash
ETCDL_API=3 etcdl snapshot save snapshot.db --endpoints= --cacert= --cert= --key=
```

- Restore Snapshot
```bash
service kube-apiserver stop
ETCDL_API=3 etcdl snapshot restore snapshot.db --data-dir --endpoints= --cacert= --cert= --key=<Destination-Restore-DIR>
systemctl daemon-reload
service etcd restart
service kube-apiserver start
```
---
# Security

## API-Groups

- **Core**
![](https://i.imgur.com/Vn99kDL.png)

- **Named**
![](https://i.imgur.com/3ihypbt.png)
## Authorization
- **Node**: Every request comes from user with name system node and part of the systems nodes group is authorized by the node authorizer.
- **ABAC**: Attribute based Access Control
![](https://i.imgur.com/yRskq0x.png)
> **Note**: For each change you have to edit the file manually.
- **RBAC**: Role Based Access Control
![](https://i.imgur.com/5AYzTAt.png)
- **Webhook**: Used for out-sourcing authorization methods by leveraging`OpenPolicyAgent`
- **AlwaysAllow**: Always allow -> `By default`
- **AlwaysDeny**: Always deny
>  **Note**: If you specified more than one auth mode they will work in order.

- Describe Auth modes on a cluster
```bash
kubectl describe pod kube-apiserver-controlplane -n kube-system
```

## RBAC
Create a role and assign users to that role.
```yml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get","create", "update","delete"]
- apiGroups: [""]
  resources: ["configMap"]
  verbs: ["create"]
  resourceNames: ["Blue","Orange"]
```

- **Binding**
	- A role binding grants the permissions defined in a role to a user or set of users. It holds a list of _subjects_ (users, groups, or service accounts), and a reference to the role being granted. A RoleBinding grants permissions within a specific namespace whereas a ClusterRoleBinding grants that access cluster-wide.

```yml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
- kind: User # or ServiceAccount
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
  namespace: default
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

- View RBAC
```bash
kubectl get roles
kubectl get rolebindings
kubectl describe role <ROLE>
```

- Check access
```bash
kubectl auth can-i create deployments
kubectl auth can-i create deployments --as <USER>
kubectl auth can-i create deployments --as=system:serviceaccount:default:<SA>
```

### Great Tools
[**KubiScan**](https://github.com/cyberark/KubiScan) : Scan Kubernetes cluster for risky permissions in Kubernetes's Role-based access control (RBAC) authorization model.

[**kubesploit**](https://github.com/cyberark/kubesploit): Cross-platform post-exploitation HTTP/2 Command & Control server and agent dedicated for containerized environments.

## ServiceAccounts
A service account provides an identity for processes that run in a Pod.
1. The name of the ServiceAccount **must be a vaild DNS subdomain name**.
2. It's usually used to give access to the cluster. [**More Info**](https://medium.com/the-programmer/working-with-service-account-in-kubernetes-df129cb4d1cc)

- Applying it to a POD
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: build-robot
  automountServiceAccountToken: false
```
> **NOTE**: In deployment, you can specify the service account name in the spec of the containers.

## ImageSecurity
```txt
docker.io/library/nginx
Registry  User/
          Account  Image/
                   Repository
                   
# Example: gcr.io/kubernetes-e2e-test-images/dnsutils
```

- Creating a Secret for imagePulling
```yaml
kubectl create secret docker-registry regcred --docker-server=private-registry.io --docker-username=registry-user --docker-password=registry-password --docker-email=zabuqasem@spiderlabs.org
```

- Attaching the secret to a pod
```yml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: private-registery.io/apps/internal-app
  imagePullSecrets:
  - name: regcred
```

## SecurityContexts
- Container Level

```yml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: private-registery.io/apps/internal-app
    securityContext:
      runAsUser: 1000
      capabilities:
          add: ["MAC_ADMIN"]
```
- Pod Level
```yml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  securityContext:
    runAsUser: 1000
  containers:
  - name: nginx
    image: private-registery.io/apps/internal-app
```
**Note**: Capabilities are only supported at the container level not at pod level.

## NetworkPolicy

|Support network policies|Doesn't support network policies|
|-|-|
|kube-router|Flannel|
|calico|x|
|Romana|x|
|Weave-net|x|

### Ingress
`namespaceSelector`: Used when you want to allow traffic from another namespace.
1. If you specified a `namespaceSelector` and didn't specify a `podSelector`, then all traffic from that namespace will be allowed.
```yml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  podSelector:
    matchLabels:
      role: db
  policyTypes:
  - Ingress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
      namespaceSelector:
        matchLabel:
          name: prod
    - ipBlock:
        cidr: 192.168.5.10/32
    ports:
    - protocol: TCP
      port: 3306
```

### Egress
```yml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: db-policy
spec:
  policyTypes:
  - Ingress
  - Egress
  ingress:
  - from:
    - podSelector:
        matchLabels:
          name: api-pod
    ports:
    - protocol: TCP
      port: 3306
  egress:
  - to:
    - ipBlock:
        cidr: 192.168.5.10/32
    ports:
    - protocol: TCP
      port: 80
```

- **Example**: Allow External trafiic from mysql and webapp on port 3306,8080 and allow all ingress.
```yml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: internal-policy
spec:
  podSelector:
    matchLabels:
      name: mysql 
  policyTypes:
  - Egress
  - Ingress
  ingress:
  - {}
  egress:
  - to:
    - podSelector:
        matchLabels:
          name: payroll
    ports:
    - protocol: TCP
      port: 8080
  - to:
    - podSelector:
        matchLabels:
          name: mysql
    ports:
    - protocol: TCP
      port: 3306
```

-  Inspection
```bash
kubectl get networkpolicy
kubectl get netpol
```

---
# Volumes-Mounts

## Pod-Volume
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx-pod
spec:
  containers:
  - name: nginx
    image: private-registery.io/apps/internal-app
    securityContext:
      runAsUser: 1000
      capabilities:
          add: ["MAC_ADMIN"]
    volumeMounts:
    - mountPath: /opt
      name: data-volume
  volumes:
  - name: data-volume
    hostPath:# Mount on the host machine
      path: /data
      type: Directory
```

##  Persistent-Volume
```yml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-voll
spec:
  accessModes:
  - ReadWriteOnce
  capacity:
    storage: 1Gi
  hostPath:
    path: /tmp/data
```

## Reclaiming
When a user is done with their volume, they can delete the PVC objects from the API that allows reclamation of the resource. The reclaim policy for a `PersistentVolume` tells the cluster what to do with the volume after it has been released of its claim. Currently, volumes can either be Retained, Recycled, or Deleted
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-voll
spec:
  accessModes:
  - ReadWriteOnce
  capacity:
    storage: 1Gi
  hostPath:
    path: /tmp/data
  persistentVolumeReclaimPolicy: <Reclaim> ##
```

### Retain
Allows for manual reclamation of the resource. When the `PersistentVolumeClaim` is deleted, the PersistentVolume still exists and the volume is considered "released". But it is not yet available for another claim because the previous claimant's data remains on the volume. An administrator can manually reclaim the volume with the following steps.
	1.  Delete the `PersistentVolume`. The associated storage asset in external infrastructure (such as an AWS EBS, GCE PD, Azure Disk, or Cinder volume) still exists after the PV is deleted.
	2.  Manually clean up the data on the associated storage asset accordingly.
	3.  Manually delete the associated storage asset.

If you want to reuse the same storage asset, create a new `PersistentVolume` with the same storage asset definition.

### Delete
Deletion removes both the `PersistentVolume` object from Kubernetes, as well as the associated storage asset in the external infrastructure.

### Recycle
**Warning:** The `Recycle` reclaim policy is deprecated. Instead, the recommended approach is to use dynamic provisioning.
> **Reference**: https://kubernetes.io/docs/concepts/storage/persistent-volumes/#recycle


## Persistent-Volume-Claim
A _PersistentVolumeClaim_ (PVC) is a request for storage by a user. It is similar to a Pod. Pods consume node resources and PVCs consume PV resources.
- Every PVC is bounded to a single PV.
- Binding process is based on the following attributes:
	1. Sufficient Capacity
	2. Access Modes
	3. Volume Modes
	4. Storage Class
	5. Selector
```yml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-voll
spec:
  accessModes:
  - ReadWriteOnce
  storageClassName: local-storage
  resources:
    requests:
      storage: 500Mi
```

- Using it in a pod
```yml
apiVersion: v1
kind: Pod
metadata:
  name: mypod
spec:
  containers:
    - name: myfrontend
      image: nginx
      volumeMounts:
      - mountPath: "/var/www/html"
        name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: myclaim
```

## Security-Risks

### HostPath
Not recommended for a multi-node cluster, And If not applied securely it may cause a security concern.
- DOD: Docker in docker
- DinD: Docker in docker using dind
> **References**:
> 1. https://devopscube.com/run-docker-in-docker

## StorageClass
Each StorageClass has a provisioner that determines what volume plugin is used for provisioning PVs. This field must be specified. And every `provisioner` have his own parameters.

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: standard
provisioner: kubernetes.io/aws-ebs 
parameters:
  type: gp2
reclaimPolicy: Retain
allowVolumeExpansion: true
mountOptions:
  - debug
volumeBindingMode: Immediate
```
> **Reference**: https://kubernetes.io/docs/concepts/storage/storage-classes/#provisioner

## TLDR
An Admin creates a PV, Then he creates a PVC that binds to a suitable PV then a user creates a pod and attaches it to the PVC.