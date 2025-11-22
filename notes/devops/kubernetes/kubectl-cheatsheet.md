# kubectl Cheatsheet

Kubernetes command-line tool reference.

## Kubectl Cheatsheet
```bash
## On debian x86_64
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

## On windows
choco install minikube

## Start minikube with virtualbox driver
minikube start --driver=virtualbox

## If you faced some issues related to VTX on windows 11 (while it's enabled)
minikube start --no-vtx-check --driver virtualbox
```
> **Important Notes**:
> - On failure run `minikube delete && minikube start` if it didn't work then follow the traceback instructions
> - [**Click me for other distros installation guide**](https://minikube.sigs.k8s.io/docs/start/)
---
## EKS
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
## Look for aws-auth
kubectl get configmap -A
## -A = --all-namespaces
```
---
## NameSpaces

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
## Managing-Pods

**Control and manage your Kubernetes pods efficiently using labels and selectors.**

## **Running a Container in a Pod**

**Deploy a pod with a specific container image.**

```bash
## Images are pulled from Docker Hub
kubectl run nginx --image=nginx
```

## **Listing Pods**

**View pods in various ways using labels and selectors.**

```bash
## List all pods in the current namespace
kubectl get pods

## List all pods with detailed information
kubectl get pods -o wide

## List pods from a specific namespace
kubectl get pods -n <Namespace>

## List all pods across all namespaces
kubectl get pods --all-namespaces

## Get all container names within a specific pod
kubectl get pods <POD> -n <NAMESPACE> -o jsonpath='{.spec.containers[*].name}'

## Describe a specific pod for detailed information
kubectl describe pods <POD> -n <NAMESPACE>
```

> **Note:** The **Ready** column shows `1/2` meaning 1 running container out of 2 total containers in the pod.

## **Using Labels and Selectors**

**Organize and filter pods using labels and selectors for better management.**

### **Adding Labels to a Pod**

**Assign key-value pairs to pods for identification and organization.**

```bash
## Add a label to an existing pod
kubectl label pod <PodName> app=frontend

## Example:
kubectl label pod nginx app=webserver
```

### **Listing Pods with Specific Labels**

**Filter and view pods based on their labels using selectors.**

```bash
## List pods with the label app=webserver
kubectl get pods -l app=webserver

## List pods with multiple labels
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
## Change the image of a container in a pod
kubectl set image <RESOURCE/RESOURCE_NAME> <CONTAINER_NAME>=<NEW_IMAGE_NAME>

## Example:
kubectl set image pod/redis-container redis-container=redis:latest
```

## **Getting Detailed Pod Information**

**Retrieve comprehensive details about pods for troubleshooting and monitoring.**

```bash
## Describe all pods in the current namespace
kubectl describe pod

## Describe a specific pod
kubectl describe pod <PodName>
```

## **Delete a Pod**

**Remove pods when they are no longer needed.**

```bash
## Delete a specific pod by name
kubectl delete pod <PodName>

## Delete pods using a YAML configuration file
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
## Get all objects with the label app=frontend
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
## StatefulSets

## Description

A **StatefulSet** is a Kubernetes resource designed for managing stateful applications. Unlike Deployments, StatefulSets provide:

- **Stable network identities**: Each pod gets a unique name (e.g., `statefulset-0`, `statefulset-1`).
- **Persistent storage**: StatefulSets allow pods to retain storage across restarts using PersistentVolumeClaims (PVCs).
- **Ordered deployment**: Pods are created or deleted in a specific order, useful for apps like databases.

## Key Features

- **Stable Pod Names**: Pods are assigned unique, consistent names.
- **Persistent Volumes**: Each pod gets a dedicated persistent volume.
- **Ordered Scaling**: Pods are created and terminated in a predefined sequence.

## Headless Services

A **Headless Service** is a Kubernetes service with `clusterIP: None`. It allows each pod in a StatefulSet to have its own DNS entry, enabling direct access to individual pods. This is useful when each pod needs to be uniquely addressed, as in databases like MySQL or Kafka.

Example of a headless service:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: web
spec:
  clusterIP: None  # No Cluster IP
  selector:
    app: web
  ports:
    - port: 80
```

This ensures DNS resolution for pods like `web-0`, `web-1`, etc., allowing access by name (e.g., `web-0.web`).

---

## Example StatefulSet YAML

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: web
spec:
  serviceName: web
  replicas: 3
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
    spec:
      containers:
      - name: web
        image: nginx:latest
        volumeMounts:
        - name: webdata
          mountPath: /usr/share/nginx/html
  volumeClaimTemplates:
  - metadata:
      name: webdata
    spec:
      accessModes: [ReadWriteOnce]
      resources:
        requests:
          storage: 1Gi
```

StatefulSets are ideal for applications that need stable identities and persistent storage, such as databases and distributed systems. Headless services complement StatefulSets by enabling direct DNS access to individual pods.

---
## ReplicaSets

## Description

A **ReplicaSet** ensures that a specified number of pod replicas are running at any given time. It replaces the older **ReplicationController** and provides better management of pod scaling. ReplicaSets are used to maintain the desired number of pods, automatically creating or deleting pods as needed.

- **Replicas**: Defines the number of identical pods that should be running.
- **Selector**: A label selector used to identify which pods are controlled by the ReplicaSet.
- **Template**: The pod specification (metadata and spec) used for creating pods in the ReplicaSet.

## Creating a ReplicationController (Deprecated)

ReplicationControllers are deprecated in favor of ReplicaSets. However, here’s an example for reference:

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
        - name: nginx-container-1
          image: nginx
          ports:
            - containerPort: 9001
```

To create it:

```bash
kubectl create -f <File.yml>
```
## Creating a ReplicaSet

```yaml
apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: myfirst-replica-set
spec:
  replicas: 3
  selector:   # A must in ReplicaSet
    matchLabels:
      type: frontend
  template:
    metadata:
      name: nginx
      labels:
        app: nginx-1
    spec:
      containers:
        - name: nginx-container-1
          image: nginx
          ports:
            - containerPort: 9001
```

To create it:

```bash
kubectl create -f <File.yml>
```

### Key Notes:

- **Selector**: Selectors are mandatory in ReplicaSets. They match pods based on their labels and ensure replication only includes the targeted pods.
- **Template**: Defines the pod configuration (labels, containers, etc.).
## Scaling Replicas

### 1. Scale using YAML file

Edit the number of replicas in the YAML file, then apply the changes:

```bash
kubectl replace -f <File.yml>
```

### 2. Scale directly from CLI

```bash
kubectl scale --replicas=<NUMBER> -f <File.yml>
```

### 3. Scale a ReplicaSet resource

```bash
kubectl scale --replicas=<NUMBER> replicaset/<NAME>
```

### 4. Delete all Pods in a ReplicaSet

```bash
kubectl scale rs/<SET> --replicas=0
```

---
## Deployments

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
> In order to view the rollout history, consider adding `--record` option when applying or doing updates via cli.

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
	  maxSurge: 2       # Maximum number of pods that can be created above the desired replicas
	  maxUnavailable: 0 # Maximum number of pods that can be unavailable during the update
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
kubectl rollout history deployment/<DEPLOYMENT_NAME> --revision=3
```
    
- **Undo/Rollback to Previous Revision:**
    
```bash
kubectl rollout undo deployment/<DEPLOYMENT_NAME> --to-revision=3
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
## Services

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
## Minikube
minikube service <service-name> --url

## Kubernetes cluster
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
> Ensure external traffic is allowed in the cloud provider's security groups or firewall.

## Headless
A **headless service** is a Kubernetes Service that does not allocate a ClusterIP. Instead, it provides direct DNS resolution to the underlying Pods or external endpoints.

**When to Use Headless Services?**
- When you want direct access to backend pods without a load balancer.
- For **stateful applications** (e.g., databases like Cassandra, MySQL).
- For **service discovery** where each pod should be addressable individually.

**To create a headless service, set `clusterIP: None` in the service YAML:**
```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-headless-service
spec:
  clusterIP: None
  selector:
    app: my-app
  ports:
    - port: 80
      targetPort: 8080
```

This will return **pod IPs** when queried instead of a single service IP.

### Difference Between ClusterIP, NodePort, LoadBalancer, and Headless Service

| Service Type | Cluster IP | Load Balancing | External Access         |
| ------------ | ---------- | -------------- | ----------------------- |
| ClusterIP    | ✅ Yes      | ✅ Yes          | ❌ No                    |
| NodePort     | ✅ Yes      | ✅ Yes          | ✅ Yes (via Node IP)     |
| LoadBalancer | ✅ Yes      | ✅ Yes          | ✅ Yes (via external LB) |
| Headless     | ❌ No       | ❌ No           | ✅ Yes (direct pod IPs)  |

## Service-Selector
**Service-Selector Relationship**:
- A **Service** uses a `selector` to identify Pods by their labels.
- The **Endpoints** object (automatically created by Kubernetes) holds the IP:port pairs of all Pods matching the selector.
- Example: A Service with `selector: app=nginx` will populate its Endpoints with all Pods labeled `app=nginx`.
**Dynamic Updates**:
- The **Endpoints Controller** (part of the Kubernetes control plane) watches for Pod changes (creation/deletion) and updates the Endpoints object in real-time.    
- If a Pod fails its readiness probe, it’s removed from Endpoints, stopping traffic to it.
**Manual Endpoints for External Services**:    
- If a Service has **no selector**, you must manually create an Endpoints object pointing to external IPs (e.g., a database outside the cluster).
- Example: A Service named `external-db` with no selector can map to a static Endpoints entry like `10.0.0.50:5432`.

**Example:** Configure a service to expose an external service listening on port `9999` on the student node and make sure it's accessible from the cluster.
```yml
apiVersion: v1
kind: Service
metadata:
  name: external-webserver-ckad01-svcn
  namespace: default
spec:
  type: ClusterIP
  ports:
  - port: 80
    protocol: TCP
    targetPort: 9999
---
apiVersion: v1
kind: Endpoints
metadata:
  name: external-webserver-ckad01-svcn
  namespace: default
subsets:
  - addresses:
      - ip: <EXTERNAL_IP_OF_STUDENT_NODE>  # Replace with the actual IP
    ports:
      - port: 9999
```

## ExternalName
- **Purpose**: Creates a DNS alias (CNAME record) for an **external service** outside the cluster.
- **Use Case**: Simplify access to external services (e.g., databases, APIs) by masking their complex DNS names with a Kubernetes Service name.
- **No Selectors or Endpoints**: Unlike standard Services, it does not route traffic to Pods or use Endpoints. Instead, it acts purely as a DNS redirect.
```yaml
apiVersion: v1
kind: Service
metadata:
  name: external-db
spec:
  type: ExternalName
  externalName: my-database.example.com  # External DNS name
```
> Inside the cluster, apps can connect to `external-db` (e.g., `external-db:3306`), and Kubernetes resolves it to `my-database.example.com`.
---
## Scheduling
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
        - name: nginx-container-1
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
## Image name: nginx
## Key: spray
## Value: mortein
## Effect: NoSchedule
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
## Required: Must match one of these zones
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
              - antarctica-east1
              - antarctica-west1
## Preferred: Prefer nodes with this label
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
## DaemonSets

## Description

A **DaemonSet** ensures that a specific pod runs on all (or selected) nodes in a Kubernetes cluster. It is useful for deploying services that need to run on every node, such as logging agents, monitoring agents, or networking tools.

- **Pod distribution**: A DaemonSet guarantees that one pod is running on each node, or a subset of nodes, in the cluster.
- **Node selector**: You can use a node selector to limit where the DaemonSet’s pods are scheduled.
- **Pod update**: DaemonSets also ensure that when a node is added to the cluster, the appropriate pod is scheduled on that node automatically.

## Example DaemonSet YAML

```yaml
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: fluentd-daemonset
spec:
  selector:
    matchLabels:
      app: fluentd
  template:
    metadata:
      labels:
        app: fluentd
    spec:
      containers:
      - name: fluentd
        image: fluent/fluentd:v1.12-1
        ports:
        - containerPort: 24224
        volumeMounts:
        - mountPath: /fluentd/etc
          name: fluentd-config
  volumes:
  - name: fluentd-config
    configMap:
      name: fluentd-configmap
```

This example creates a DaemonSet that runs a `fluentd` container on every node in the cluster.
## DaemonSet Scaling and Management

DaemonSets automatically manage pod scheduling, so **scaling** is generally not needed. However, you can control the behavior by using:

- **Node selectors**: Limit where pods are deployed.
- **Tolerations**: Schedule pods on nodes with specific taints.
- **Update strategy**: Control how DaemonSet pods are updated when the specification changes (rolling updates).
### Example: Node Selector

You can use `nodeSelector` to schedule DaemonSet pods on specific nodes:

```yaml
spec:
  template:
    spec:
      nodeSelector:
        disktype: ssd
```

### Example: Toleration (for tainted nodes)

You can use tolerations to allow pods to be scheduled on tainted nodes:

```yaml
spec:
  template:
    spec:
      tolerations:
      - key: "dedicated"
        operator: "Equal"
        value: "gpu-node"
        effect: "NoSchedule"
```

### Conclusion

- **DaemonSets** are ideal for workloads that need to run on every node, like monitoring or logging agents.
- Pods are automatically distributed across nodes and can be managed using selectors, tolerations, and update strategies.

---
## Monitoring
Using Built-In metrics server (in memory solution).
- Installing Metrics-Server
```bash
## Minikube
minikube addons enable metrics-server

## Cluster
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
## -f: View live
## ContianerName: Only mandatory if your pod had multiple containers
```
---
## Jobs-CronJobs

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

2. **For Jobs**:
    - Use `backoffLimit` to control retries and avoid infinite loops.
    - Define resource requests/limits for Pods to prevent overloading nodes.
3. **For CronJobs**:
    - Test the Job template separately to ensure it behaves as expected.
    - Keep the `successfulJobsHistoryLimit` and `failedJobsHistoryLimit` reasonable to avoid clutter.
    - Use descriptive names for CronJobs for better identification.
4. **Monitoring**:
    - Monitor Job and CronJob statuses using `kubectl get jobs` and `kubectl get cronjobs`.
    - Enable logging to debug failures effectively.
---
## Secrets
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
## Multi-Containers

**There are 3 common patterns:**
- **Sidecar pattern**: An extra container in your pod to **enhance** or **extend** the functionality of the main container.
- **Ambassador pattern**: A container that **proxy the network connection** to the main container.
- **Adapter pattern**: A container that **transform output** of the main container.
## initContainer
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
## Maintenance
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

> - Pods will not fall over to their main node automatically, But when pods gets rescheduled they will be created on it
> - Pods that aren't part of a replicaset isn't drained, you have to use --force

## Software-Releases
Software version in k8s consists of 3 parts:
```txt
v1.11.3
Major.Minor.Patch

## Minor = [Features,Functionalities]
## Patch = [BugFixes]
```
>**Notes**: 
>Kubernetes only support 3 minor releases.
>It's advised to upgrade version 1 minor version at a time.

## Cluster-Upgrade

### Control Plane Upgrade
```sh
## 1. Drain control plane node
kubectl drain controlplane --ignore-daemonsets

## 2. Add Kubernetes repository
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee -a /etc/apt/sources.list.d/kubernetes.list

## 3. Update kubeadm
sudo apt-cache madison kubeadm # Get the desired version
sudo apt-mark unhold kubeadm
sudo apt-get update
sudo apt-get install -y kubeadm='1.31.0-1.1' # Replace version with desired version from madison cache
sudo apt-mark hold kubeadm

## 4. Apply upgrade
sudo kubeadm upgrade plan v1.31.0
sudo kubeadm upgrade apply v1.31.0

## 5. Update kubelet and kubectl
sudo apt-cache madison kubelet # Get the desired version
sudo apt-mark unhold kubectl kubelet
sudo apt-get update
sudo apt-get install -y kubectl='1.31.0-1.1' kubelet='1.31.0-1.1' # Replace version with desired version from madison cache
sudo apt-mark hold kubectl kubelet

## 6. Restart services
sudo systemctl daemon-reload
sudo systemctl restart kubelet

## 7. Uncordon node
kubectl uncordon controlplane
```
### Worker Node Upgrade
```sh
## 1. Drain worker node (replace <NODE> with node name)
kubectl drain <NODE> --ignore-daemonsets

## 2. Add Kubernetes repository
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee -a /etc/apt/sources.list.d/kubernetes.list

## 3. Update kubeadm
sudo apt-cache madison kubeadm
sudo apt-mark unhold kubeadm
sudo apt-get update
sudo apt-get install -y kubeadm='1.31.0-1.1'
sudo apt-mark hold kubeadm

## 4. Update kubelet and kubectl
sudo apt-cache madison kubelet # Get the desired version
sudo apt-mark unhold kubectl kubelet
sudo apt-get update
sudo apt-get install -y kubectl='1.31.0-1.1' kubelet='1.31.0-1.1'  # Replace version with desired version from madison cache
sudo apt-mark hold kubectl kubelet

## 5. Restart services
sudo systemctl daemon-reload
sudo systemctl restart kubelet

## 6. Uncordon node (run from control plane)
kubectl uncordon <NODE>
```
## Backup-and-Restore

- Backup resource configs
```bash
kubectl get all -A -o yaml > all-deploy-services.yml
```

- Backup ETCD
```bash
ETCDCTL_API=3 etcdctl snapshot save snapshot.db \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```

- Restore Snapshot
```bash
ETCDCTL_API=3 etcdctl snapshot restore snapshot.db \
  --data-dir=/var/lib/etcd-restored \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/kubernetes/pki/etcd/ca.crt \
  --cert=/etc/kubernetes/pki/etcd/server.crt \
  --key=/etc/kubernetes/pki/etcd/server.key
```
Now update the ETCD configuration file to point to the new data directory
```bash
## /etc/kubernetes/manifests/etcd.yaml
--data-dir=/var/lib/etcd-restored

## Using sed
sed -i 's|/var/lib/etcd|/var/lib/etcd-restored|' /etc/kubernetes/manifests/etcd.yaml
```
Finally restart the ETCD container
```bash
kubectl get pods -n kube-system
kubectl delete pod <etcd-pod-name> -n kube-system
```
Verify the ETCD status
```bash
kubectl describe pod <etcd-pod-name> -n kube-system | grep 'data-dir'
```

## Node-Debugging

If a node is not working properly, you can debug it by checking the following:

- **Check kubelet logs**:
```bash
journalctl -u kubelet
```
- **Check kubelet status**:
```bash
systemctl status kubelet
```
- **Check kubelet configuration**:
```bash
ps aux | grep kubelet
```
- **Check kubelet configuration file**:
```bash
cat /var/lib/kubelet/config.yaml
```

---
## Security
## API-Groups

## What Are API Groups?

API groups in Kubernetes are a mechanism to organize and version API resources. Kubernetes divides its API into multiple logical groups to manage the vast array of resources efficiently. Each group contains related resources, making it easier to control access, version them, and extend the API.

## Core API Group (Empty API Group)

- **Group**: `""` (empty string)
- **Resources**: Core Kubernetes resources like `pods`, `services`, `configmaps`, `nodes`, etc.
- **Example**:
```yaml
apiVersion: v1
kind: Pod
```
## Named API Groups

Named API groups include additional features and custom resources. They follow the format: `<group>/<version>`.

| **API Group**                    | **Resources**                                                  | **Example `apiVersion`**          |
| -------------------------------- | -------------------------------------------------------------- | --------------------------------- |
| **apps**                         | Deployments, DaemonSets, StatefulSets, ReplicaSets             | `apps/v1`                         |
| **batch**                        | Jobs, CronJobs                                                 | `batch/v1`                        |
| **autoscaling**                  | HorizontalPodAutoscaler                                        | `autoscaling/v1`                  |
| **networking.k8s.io**            | NetworkPolicies, Ingress, IngressClass                         | `networking.k8s.io/v1`            |
| **policy**                       | PodSecurityPolicies                                            | `policy/v1`                       |
| **rbac.authorization.k8s.io**    | Roles, RoleBindings, ClusterRoles, ClusterRoleBindings         | `rbac.authorization.k8s.io/v1`    |
| **storage.k8s.io**               | StorageClasses, VolumeAttachments, CSI drivers                 | `storage.k8s.io/v1`               |
| **admissionregistration.k8s.io** | MutatingWebhookConfigurations, ValidatingWebhookConfigurations | `admissionregistration.k8s.io/v1` |
| **apiextensions.k8s.io**         | CustomResourceDefinitions (CRDs)                               | `apiextensions.k8s.io/v1`         |
| **authentication.k8s.io**        | TokenReviews                                                   | `authentication.k8s.io/v1`        |
| **authorization.k8s.io**         | SubjectAccessReviews                                           | `authorization.k8s.io/v1`         |

## Examples

### 1. Core API Group Resource

Creating a Pod (Core API group, empty `apiVersion` group):

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  containers:
  - name: nginx
    image: nginx
```

### 2. Named API Group Resource

Creating a Deployment (`apps` API group):

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-deployment
spec:
  replicas: 3
  selector:
    matchLabels:
      app: my-app
  template:
    metadata:
      labels:
        app: my-app
    spec:
      containers:
      - name: nginx
        image: nginx
```

## Why API Groups Matter

- **Versioning**: Enables incremental changes to resource definitions without breaking existing functionality.
- **Access Control**: Allows fine-grained RBAC policies by targeting specific groups and resources.
- **Extension**: Lets you add custom resources using CustomResourceDefinitions (CRDs) under your own API groups.

## Using API Groups with RBAC

When defining RBAC rules, specify the API group for the resource.

Example: Grant access to `Deployments` in the `apps` group:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: manage-deployments
rules:
- apiGroups: ["apps"]
  resources: ["deployments"]
  verbs: ["create", "delete", "update", "get", "list"]
```

## Enable API Groups

Add `--runtime-config` flag to the API server configuration file (`/etc/kubernetes/manifests/kube-apiserver.yaml`).

For example, to enable the `rbac.authorization.k8s.io/v1alpha1` API group:

```yaml
--runtime-config=rbac.authorization.k8s.io/v1alpha1
```

## Convert API Versions

Using `kubectl convert` to convert resources to a specific API version:

```bash
curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl-convert
chmod +x kubectl-convert
mv kubectl-convert /usr/local/bin
```

Convert a resource to a specific API version:

```bash
## Without the --output-version flag, it converts to the latest version.
kubectl-convert -f <file.yaml> [--output-version <apiVersion>]
```
### Tips

- Use `kubectl api-resources` to list all available API groups and resources in your cluster:

```bash
kubectl api-resources
## Alternatively
k get storageclasses # when pressing `tab` key it will auto-completet to storageclasses.storage.k8s.io the storage.k8s.io is the api group
```

- Always match the `apiVersion` and `group` with the version supported by your cluster.

---
## CustomResourceDefinitions

## What Are CRDs?

**CustomResourceDefinitions (CRDs)** are a Kubernetes feature that allows you to extend Kubernetes with custom resource types. With CRDs, you can define and manage your own resources (similar to Pods, Services, etc.) tailored to your application requirements. These resources are managed via the Kubernetes API, just like native resources.

## Key Components of CRDs

5. **Custom Resource**:
    - A new resource type created using a CRD.
    - Example: `kind: MyResource`.
6. **CRD Definition**:
    - Defines the schema, versions, and behavior of your custom resource.
    - Managed by the `apiextensions.k8s.io/v1` API group.
7. **Controller**:
    - Custom logic implemented using a controller watches for changes to the custom resources and acts accordingly.

## Why Use CRDs?

- **Extend Kubernetes**: Add resource types that are not available by default.
- **Manage Applications**: Use CRDs to encapsulate application logic in a Kubernetes-native way.
- **Integration**: Integrate third-party tools or APIs directly into Kubernetes.

## Example: Defining a CRD

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: widgets.example.com  # Plural name for the resource
spec:
  group: example.com         # API group
  names:
    plural: widgets          # Plural name of the resource
    singular: widget         # Singular name
    kind: Widget             # Kind of the resource
    shortNames:
      - w                    # Short name for kubectl commands
  scope: Namespaced          # Scope: Namespaced or Cluster
  versions:
  - name: v1
    served: true             # Serves the resource
    storage: true            # Persists the resource
    schema:                  # OpenAPI v3 schema for validation
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              size:
                type: string
              color:
                type: string
    subresources:            # Additional features
      status: {}             # Enables the status subresource
      scale:                 # Enables scale subresource
        specReplicasPath: ".spec.replicas"
        statusReplicasPath: ".status.replicas"
```

## Creating and Using a CRD

### 1. **Create the CRD**

```bash
kubectl apply -f crd-definition.yaml
```

### 2. **Verify CRD**

List all CRDs:

```bash
kubectl get crd
```

Describe the CRD:

```bash
kubectl describe crd widgets.example.com
```
## Example: Creating a Custom Resource

**Custom Resource YAML**:

```yaml
apiVersion: example.com/v1
kind: Widget
metadata:
  name: my-widget
spec:
  size: medium
  color: blue
```

### Apply the Custom Resource

```bash
kubectl apply -f custom-resource.yaml
```

### Verify the Custom Resource

```bash
kubectl get widgets
kubectl describe widget my-widget
```
## Example: Custom Controller for CRD

To manage CRDs, you typically write a custom controller using a framework like **Kubebuilder** or **Operator SDK**. This controller watches for changes to your custom resources and acts upon them.

**Basic Workflow**:

8. Watch for changes to the CRD (e.g., `Widget`).
9. Reconcile the desired state with the current state.
10. Update the status subresource if needed.

### List CRDs

```bash
kubectl get crd
```

### Describe a CRD

```bash
kubectl describe crd <CRD_NAME>
```

### Delete a CRD

```bash
kubectl delete crd <CRD_NAME>
```
## Advanced Features of CRDs

11. **Validation Schema**:
    
    - Define an OpenAPI schema for your custom resource.
    - Ensures that all instances of the resource follow the specified structure.
12. **Subresources**:
    
    - **`status`**: Manage the resource’s status separately.
    - **`scale`**: Integrate scaling functionality.
13. **Defaulting and Conversion Webhooks**:
    
    - Implement webhooks for default values and API version conversions.
14. **Versions**:
    
    - Support multiple versions of the custom resource for smooth upgrades.

## Use Cases for CRDs

15. **Operators**:
    - Extend Kubernetes with application-specific controllers (e.g., Prometheus Operator, etc.).
16. **Custom Application APIs**:
    - Manage application-specific resources directly via Kubernetes.
17. **Platform Features**:
    - Build platform-specific features like CI/CD pipelines or configuration management tools.
## Best Practices

18. **Define a Validation Schema**:
    
    - Ensure your CRD has an OpenAPI schema to validate custom resources.
19. **Version Control**:
    
    - Support multiple versions for smooth migrations.
20. **Use Namespaces**:
    
    - Scope resources within namespaces unless cluster-wide access is required.
21. **Test Controllers**:
    
    - Thoroughly test custom controllers to ensure they handle all edge cases.

---
## Operators

## What Are Operators?

**Operators** are Kubernetes extensions that use **CustomResourceDefinitions (CRDs)** to manage applications and their components. Operators encapsulate the logic for deploying, configuring, scaling, and maintaining complex stateful applications, automating routine operational tasks.

## Why Use Operators?

22. **Automation**: Simplify operational tasks like upgrades, backups, and failovers.
23. **Custom Logic**: Embed application-specific knowledge and lifecycle management.
24. **Consistency**: Ensure reliable deployment and operation of applications in a Kubernetes-native way.
25. **Declarative Management**: Use Kubernetes-style APIs to manage application resources.

## Key Components of an Operator

26. **CustomResourceDefinition (CRD)**:
    - Defines a new resource type, e.g., `MySQL`, `RedisCluster`.
27. **Custom Resource (CR)**:
    - A specific instance of the CRD, e.g., a MySQL database named `example-db`.
28. **Controller**:
    - Watches for changes to the custom resources and ensures the desired state is maintained.

## Operator Workflow

29. **CRD Creation**:
    - Define the custom resource type for the application.
30. **Custom Resource Creation**
    - Create instances of the CRD using YAML files.
31. **Controller Logic**:
    - The Operator's controller monitors the custom resource and executes application-specific logic to achieve the desired state.
32. **Reconciliation Loop**:
    - Continuously ensures the actual state matches the desired state defined in the custom resource.
## Example: A MySQL Operator

### 1. Define a CRD for MySQL

```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: mysqls.example.com
spec:
  group: example.com
  names:
    plural: mysqls
    singular: mysql
    kind: MySQL
    shortNames:
      - ms
  scope: Namespaced
  versions:
  - name: v1
    served: true
    storage: true
    schema:
      openAPIV3Schema:
        type: object
        properties:
          spec:
            type: object
            properties:
              version:
                type: string
              storage:
                type: string
```

### 2. Create a Custom Resource

```yaml
apiVersion: example.com/v1
kind: MySQL
metadata:
  name: example-db
spec:
  version: "8.0"
  storage: "10Gi"
```

### 3. Operator Logic in Controller

The controller will:

- Watch for changes to `MySQL` resources.
- Create a `Deployment`, `Service`, and `PersistentVolumeClaim` to deploy MySQL with the specified configuration.

## Operator Development Tools

33. **Operator SDK**:
    - Simplifies the creation of Kubernetes Operators.
    - Supports Helm, Ansible, and Go-based development.
    - Website: [Operator SDK](https://sdk.operatorframework.io/)
34. **Kubebuilder**:
    - Framework for building Kubernetes APIs and controllers using Go.
    - Website: [Kubebuilder](https://github.com/kubernetes-sigs/kubebuilder)
35. **Helm**:
    - Use Helm charts to package and deploy applications, and wrap them with operator logic.
## Managing Operators

### Deploying an Operator

Operators are typically deployed as a `Deployment` in the cluster:

```bash
kubectl apply -f operator-deployment.yaml
```

### Installing Community Operators

Use **OperatorHub** or the **OpenShift Console** to discover and install pre-built operators:

```bash
kubectl apply -f https://operatorhub.io/install/operator.yaml
```

### Viewing Installed Operators

```bash
kubectl get csv -n <namespace>
```

## Operator Lifecycle Manager (OLM)

The **Operator Lifecycle Manager (OLM)** is a tool to manage Operators in a Kubernetes cluster. It provides:

- Installation and upgrades of Operators.
- Dependency management.
- Permission management for Operators.

### Install OLM

```bash
curl -sL https://github.com/operator-framework/operator-lifecycle-manager/releases/download/v0.31.0/install.sh | bash -s v0.31.0
```

```

### List CRDs

```bash
kubectl get crds
```

### Create a Custom Resource

```bash
kubectl apply -f custom-resource.yaml
```

### Check Operator Logs

```bash
kubectl logs -l app=<operator-name> -n <namespace>
```

## Use Cases for Operators

36. **Databases**: Automate deployment, scaling, and backups for stateful applications like MySQL, MongoDB, or Cassandra.
37. **Message Queues**: Manage Kafka or RabbitMQ clusters.
38. **Monitoring**: Deploy Prometheus and Grafana with custom configurations.
39. **CI/CD**: Automate workflows and environments for pipelines (e.g., Jenkins Operator).
40. **Backup and Restore**: Automate snapshot creation and restoration for data.

## Benefits of Operators

41. **Kubernetes-Native**: Use CRDs to seamlessly integrate custom logic into Kubernetes.
42. **Automation**: Simplify operational overhead for complex applications.
43. **Scalability**: Automate scaling and resource management.
44. **Reliability**: Ensure consistent application state across environments.

---
## Authorization

### Authorization Modes

Kubernetes supports various modes of authorization for controlling access to API resources.

45. **Node**:
    - Requests from system nodes (e.g., `system:node`) are authorized using the **Node Authorizer**.
46. **ABAC** (Attribute-Based Access Control):
    - Access is controlled via a policy file with user-defined rules.
    - **Note**: Changes require manual editing of the policy file.
47. **RBAC** (Role-Based Access Control):
    - Uses roles and role bindings to manage permissions for users, groups, or service accounts.
48. **Webhook**:
    - Authorization is outsourced to external services like **Open Policy Agent** (OPA).
49. **AlwaysAllow**:
    - Allows all requests unconditionally. Typically used for testing or simple setups.
50. **AlwaysDeny**:
    - Denies all requests unconditionally.
### Note:
If multiple authorization modes are specified, they are evaluated in order.

### Check Auth Modes on a Cluster

```bash
kubectl describe pod kube-apiserver-controlplane -n kube-system
```

## RBAC

### 1. **Create a Role**

Defines the permissions for a set of API resources and operations:

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: developer
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["list", "get", "create", "update", "delete"]
- apiGroups: [""]
  resources: ["configmaps"]
  verbs: ["create"]
  resourceNames: ["Blue-cm", "Orange-cm"]
```

### 2. **RoleBinding**

A `RoleBinding` assigns the role’s permissions to users, groups, or service accounts in a specific namespace.

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: devuser-developer-binding
subjects:
- kind: User # Can also be ServiceAccount or Group
  name: dev-user
  apiGroup: rbac.authorization.k8s.io
  namespace: default
roleRef:
  kind: Role
  name: developer
  apiGroup: rbac.authorization.k8s.io
```

- **ClusterRoleBinding**: Similar to a RoleBinding but grants cluster-wide access.

## Predefined Roles and ClusterRoles

Here’s a table of **predefined roles** in Kubernetes and how to use them:

| **Predefined Role**           | **Scope**    | **Description**                                                                                | **Usage Command**                                                                                |
| ----------------------------- | ------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ |
| **cluster-admin**             | Cluster-wide | Grants superuser access to the cluster. Can perform any action on any resource in the cluster. | `kubectl create clusterrolebinding <NAME> --clusterrole=cluster-admin --user=<USER>`             |
| **admin**                     | Namespace    | Grants full access to a namespace, except managing cluster-wide resources.                     | `kubectl create rolebinding <NAME> --role=admin --user=<USER> -n <NAMESPACE>`                    |
| **edit**                      | Namespace    | Allows read/write access to most objects in a namespace, except managing roles and bindings.   | `kubectl create rolebinding <NAME> --role=edit --user=<USER> -n <NAMESPACE>`                     |
| **view**                      | Namespace    | Grants read-only access to resources in a namespace, excluding secrets.                        | `kubectl create rolebinding <NAME> --role=view --user=<USER> -n <NAMESPACE>`                     |
| **system:node**               | Cluster-wide | Allows nodes to read secrets and create pods assigned to them.                                 | Automatically used by kubelet.                                                                   |
| **system:node-proxier**       | Cluster-wide | Grants permissions for the kube-proxy to manage network rules.                                 | Automatically used by kube-proxy.                                                                |
| **system:discovery**          | Cluster-wide | Allows read-only access to API resources for system components or end-users to discover APIs.  | `kubectl create clusterrolebinding <NAME> --clusterrole=system:discovery --user=<USER>`          |
| **system:public-info-viewer** | Cluster-wide | Grants read-only access to non-sensitive, public cluster information.                          | `kubectl create clusterrolebinding <NAME> --clusterrole=system:public-info-viewer --user=<USER>` |
| **system:aggregate-to-admin** | Cluster-wide | Aggregates roles into the `admin` role to extend its permissions.                              | Automatically applied; no manual usage required.                                                 |
| **system:aggregate-to-edit**  | Cluster-wide | Aggregates roles into the `edit` role to extend its permissions.                               | Automatically applied; no manual usage required.                                                 |
| **system:aggregate-to-view**  | Cluster-wide | Aggregates roles into the `view` role to extend its permissions.                               | Automatically applied; no manual usage required.                                                 |

### Examples of Using Predefined Roles

#### 1. Bind the `view` Role to a User in a Namespace

```bash
kubectl create rolebinding view-binding --role=view --user=john -n development
```

#### 2. Bind the `cluster-admin` Role to a User Cluster-wide

```bash
kubectl create clusterrolebinding admin-binding --clusterrole=cluster-admin --user=john
```

#### 3. Grant `edit` Role to a ServiceAccount in a Namespace

```bash
kubectl create rolebinding edit-binding --role=edit --serviceaccount=development:build-robot -n development
```

#### 4. Bind the `system:discovery` Role to a Group

```bash
kubectl create clusterrolebinding discovery-binding --clusterrole=system:discovery --group=developers
```
## Useful Commands for RBAC

### View Roles and Bindings

```bash
kubectl create [role,clusterrole] <ROLE> --verb=<VERB> --resource=<RESOURCE> -n <NAMESPACE>
kubectl get roles
kubectl get rolebindings
kubectl describe role <ROLE>
kubectl describe rolebinding <ROLEBINDING>
```
### Check Access

```bash
kubectl auth can-i <VERB> <RESOURCE>
kubectl auth can-i create deployments --as <USER>
kubectl auth can-i create deployments --as=system:serviceaccount:<NAMESPACE>:<SERVICE_ACCOUNT>
```

Here’s a comparison table between **Role** and **ClusterRole** in Kubernetes:

| Feature             | **Role**                                                                  | **ClusterRole**                                                                                 |
| ------------------- | ------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| **Scope**           | Namespace-specific: Applies only to a single namespace.                   | Cluster-wide: Applies across all namespaces or cluster-level resources.                         |
| **Resource Types**  | Only namespace-scoped resources (e.g., pods, services, configmaps, etc.). | Both cluster-scoped resources (e.g., nodes, persistentvolumes) and namespace-scoped resources.  |
| **Binding Type**    | Associated with a `RoleBinding`.                                          | Associated with a `ClusterRoleBinding` or `RoleBinding`.                                        |
| **Use Case**        | Used to define permissions within a specific namespace.                   | Used to define permissions for resources across the cluster or to grant cross-namespace access. |
| **Example Use**     | - Grant access to pods in the `dev` namespace.                            | - Grant access to view all nodes in the cluster. - Grant access to manage persistent volumes.   |
| **Command to View** | `kubectl get role -n <namespace>`                                         | `kubectl get clusterrole`                                                                       |
| **Command to Bind** | `kubectl create rolebinding`                                              | `kubectl create clusterrolebinding`                                                             |
| **Flexibility**     | Limited to one namespace per role.                                        | Can span multiple namespaces or target cluster-wide resources.                                  |

### Example Scenarios
1. **Role**:
    - A developer needs to manage pods in the `dev` namespace:
```bash
kubectl create role dev-role --verb=get,list,create --resource=pods -n dev
```
        
2. **ClusterRole**:
    - An admin needs to allow monitoring tools to view logs from all namespaces:
```bash
kubectl create clusterrole view-logs --verb=get,list --resource=pods/log
```
### Great Audit Tools
[**KubiScan**](https://github.com/cyberark/KubiScan) : Scan Kubernetes cluster for risky permissions in Kubernetes's Role-based access control (RBAC) authorization model.
[**kubesploit**](https://github.com/cyberark/kubesploit): Cross-platform post-exploitation HTTP/2 Command & Control server and agent dedicated for containerized environments.

---
## ServiceAccounts

A **ServiceAccount** provides an identity for processes running in a Pod, enabling them to interact with the Kubernetes API securely. By default, every namespace includes a `default` ServiceAccount, but custom ServiceAccounts can be created for specific permissions and tasks.

## Key Points

3. **Naming**: The ServiceAccount name must be a valid DNS subdomain name.
4. **Purpose**: ServiceAccounts are primarily used to grant API access to applications running inside Pods.
5. **Default Behavior**: Pods use the `default` ServiceAccount in their namespace unless another ServiceAccount is specified.

## Example: Applying a ServiceAccount to a Pod

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: my-pod
spec:
  serviceAccountName: build-robot
  automountServiceAccountToken: false
```

- **`serviceAccountName`**: Specifies the ServiceAccount to use.
- **`automountServiceAccountToken`**: Set to `false` if you don’t want the token to be automatically mounted in the Pod.

> **Note**: In deployments, you can include the `serviceAccountName` in the container spec.

### 1. **Create a ServiceAccount**

```bash
kubectl create serviceaccount build-robot
```

### 2. **List ServiceAccounts**

```bash
kubectl get serviceaccounts
kubectl get serviceaccounts -n <NAMESPACE>
```

### 3. **Describe a ServiceAccount**

```bash
kubectl describe serviceaccount <NAME>
kubectl describe serviceaccount <NAME> -n <NAMESPACE>
```

### 4. **Delete a ServiceAccount**

```bash
kubectl delete serviceaccount <NAME>
kubectl delete serviceaccount <NAME> -n <NAMESPACE>
```

### 5. **Bind a ServiceAccount to a Role**

#### Create a RoleBinding for Namespace-Scoped Access:

```bash
kubectl create rolebinding build-robot-binding \
  --role=developer \
  --serviceaccount=default:build-robot \
  -n default
```

#### Create a ClusterRoleBinding for Cluster-Wide Access:

```bash
kubectl create clusterrolebinding build-robot-cluster-binding \
  --clusterrole=cluster-admin \
  --serviceaccount=default:build-robot
```
### 6. **Apply a ServiceAccount to a Running Pod**

You cannot modify an existing Pod to use a different ServiceAccount. You must delete the Pod and recreate it with the desired ServiceAccount:

```bash
kubectl run my-pod --image=nginx --serviceaccount=build-robot
```
### 7. **Get the Token for a ServiceAccount**

To retrieve the token for a ServiceAccount, use the following commands:

#### For Kubernetes 1.24+ with projected tokens:

```bash
kubectl create token build-robot
```
### 8. **Attach a ServiceAccount to a Deployment**

```bash
kubectl set serviceaccount deployment/my-deployment build-robot
```

## Use Cases

6. **Grant Specific Permissions**: Attach a ServiceAccount to a Role/ClusterRole via RoleBinding/ClusterRoleBinding to limit what the Pod can do in the cluster.
7. **Secure API Access**: Prevent unauthorized API access by using scoped ServiceAccounts instead of the default one.
8. **Automation**: Automate tasks like builds or CI/CD workflows using a dedicated ServiceAccount.

## Tips

- Use ServiceAccounts to avoid exposing credentials directly in Pods.
- Always scope permissions to the minimum required using RBAC.
- Consider disabling `automountServiceAccountToken` unless explicitly needed.
---
## Admission-Controllers

## What Are Admission Controllers?

**Admission Controllers** are plugins that intercept API requests to the Kubernetes API server and can modify or validate the requests before they are persisted in etcd. They act as a gatekeeper to enforce policies or augment resources with additional configurations.
## Admission Controller Workflow

1. **Authentication**: The request is authenticated.
2. **Authorization**: The request is authorized.
3. **Admission Control**: The request passes through admission controllers for validation or modification.
	1. **Mutating Admission Controllers**: Modify the request object.
	2. **Validating Admission Controllers**: Validate the request object.
	3. **Webhooks**: External services that can modify or validate requests.
	> **NOTE:** Mutating happens before validating.
4. **Persistence**: If all checks pass, the request is persisted in etcd.

## Types of Admission Controllers

1. **Mutating Admission Controllers**: Modify the incoming request object.
    - Example: Add default labels, inject sidecars (e.g., Istio).
2. **Validating Admission Controllers**: Validate the request but do not modify it.
    - Example: Check if the request adheres to security policies.

## Common Admission Controllers

| **Admission Controller**       | **Description**                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------- |
| **AlwaysDeny**                 | Denies all API requests (testing purposes).                                     |
| **AlwaysPullImages**           | Forces Kubernetes to always pull the image specified in the Pod spec.           |
| **DefaultStorageClass**        | Assigns a default storage class to PersistentVolumeClaims if none is specified. |
| **LimitRanger**                | Enforces resource limits (e.g., CPU, memory) defined in the namespace.          |
| **NamespaceLifecycle**         | Ensures operations in a namespace (e.g., deletion) follow lifecycle rules.      |
| **NodeRestriction**            | Restricts nodes from modifying objects they shouldn't, such as their labels.    |
| **PodSecurity**                | Enforces Pod Security admission policies (replaces PodSecurityPolicy).          |
| **ResourceQuota**              | Ensures resource usage stays within defined quotas in a namespace.              |
| **MutatingAdmissionWebhook**   | Calls external webhooks to modify API objects.                                  |
| **ValidatingAdmissionWebhook** | Calls external webhooks to validate API objects.                                |
| **TaintNodesByCondition**      | Automatically applies taints based on node conditions.                          |
| **PodNodeSelector**            | Assigns Pods to specific nodes based on a configured selector.                  |
| **NamespaceAutoProvision**     | It creates a namespace if it cannot be found. (Deprecated)                      |

## Configuring Admission Controllers

### Check Current Admission Controllers

Admission controllers are enabled via the `--enable-admission-plugins` flag in the Kubernetes API server.

Example:

```bash
kubectl describe pod kube-apiserver-controlplane -n kube-system | grep enable-admission-plugins
```

### Enable Admission Controllers

Edit the API server configuration to include the desired admission controllers:

```bash
## Edit the API server configuration
vim /etc/kubernetes/manifests/kube-apiserver.yaml

## Add the desired admission controllers
--enable-admission-plugins=NamespaceLifecycle,LimitRanger,ResourceQuota
```

### Disable Admission Controllers
Edit the API server configuration to disable the desired admission controllers:

```bash
## Edit the API server configuration
vim /etc/kubernetes/manifests/kube-apiserver.yaml

## Add the desired admission controllers
--disable-admission-plugins=NamespaceLifecycle,LimitRanger,ResourceQuota
```

## Using Webhooks for Admission Control

### 1. Mutating Admission Webhook

Used to modify resources during admission. Example: Injecting a sidecar container.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: MutatingWebhookConfiguration
metadata:
  name: example-mutating-webhook
webhooks:
  - name: example.com
    rules:
      - apiGroups: ["apps"]
        apiVersions: ["v1"]
        resources: ["deployments"]
    clientConfig:
      service:
        name: example-webhook
        namespace: default
        path: "/mutate"
      caBundle: <BASE64_CA_CERT>
```

### 2. Validating Admission Webhook

Used to validate requests against policies.

```yaml
apiVersion: admissionregistration.k8s.io/v1
kind: ValidatingWebhookConfiguration
metadata:
  name: example-validating-webhook
webhooks:
  - name: example.com
    rules:
      - apiGroups: [""]
        apiVersions: ["v1"]
        resources: ["pods"]
    clientConfig:
      service:
        name: example-webhook
        namespace: default
        path: "/validate"
      caBundle: <BASE64_CA_CERT>
```

### List Active Admission Controllers

```bash
kubectl get --raw /api/v1/namespaces/kube-system/configmaps/kubeadm-config | jq '.data["ClusterConfiguration"]' | grep admission
```

### Test a Webhook

Simulate a request and verify the webhook's response:

```bash
kubectl apply -f test-pod.yaml --dry-run=server
```
## Tips

3. Use **MutatingAdmissionWebhook** for automatic configurations like adding sidecars or labels.
4. Use **ValidatingAdmissionWebhook** to enforce security or compliance rules.
5. Combine admission controllers like `LimitRanger` and `ResourceQuota` to enforce resource policies in namespaces.
6. Always test admission controllers and webhooks in a non-production environment before applying them to production.
---
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

---
## NetworkPolicy

| Support network policies | Doesn't support network policies |
| ------------------------ | -------------------------------- |
| kube-router              | Flannel                          |
| calico                   | x                                |
| Romana                   | x                                |
| Weave-net                | x                                |

### Ingress
`namespaceSelector`: Used when you want to allow traffic from another namespace.
7. If you specified a `namespaceSelector` and didn't specify a `podSelector`, then all traffic from that namespace will be allowed.
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
## Volumes-Mounts

## Pod-Volume
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
