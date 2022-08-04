# Navgation
- [**Installing-and-runinng-minikube**](#Installing-and-runinng-minikube)
- [**Namepaces**](#Namepaces)
- [**Managing-PODS**](#Managing-PODS)
- [**YAML**](#YAML)
	- [Generate-template](#Generate-template)
- [**Replicas**](#Replicas)
	- [Scaling-Replicas](#Scaling-Replicas)
- [**Deployments**](#Deployments)
	- [Deployment-strategies](#Deployment%20strategies)
	- [References](#References)
- [**Services**](#Services)
	- [NodePort](#NodePort)
	- [ClusterIp](#ClusterIp)
	- [LoadBalancer](#LoadBalancer)
- [**Scheduling**](#Scheduling)
# Installing-and-runinng-minikube
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
# Namepaces
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
# Managing-PODS
- Running a Container in a pod
```bash
# Images are pulled from dockerhub
kubectl run nginx --image nginx
```
- Listing pods
```bash
kubectl get pods
kubectl get pods -o wide
# From Namespaces
kubectl get pods <NameSpace>
kubectl get pods --all-namespaces
# Get all containers within a POD
kubectl get pods <POD> -n <NAMESPACE> -o jsonpath='{.spec.containers[*].name}'
kubectl describe pods <POD> -n <NAMESPACE>
kubectl get pods # Ready column 1/2 (1 running container/2 total containers)
 ```
- Change pod spec
```bash
# Change an image for a container
kubectl set image <RESOURCE/RESOURCE_NAME> <CONTAINER_NAME>=<NEW_IMAGE_NAME>
#Example:
kubectl set image pod/redis-container redis-container=redis
```
- Getting detailed pod information
```bash
kubectl describe pod # All pods
kubectl describe pod <PodName>
```
- Delete a pod
```bash
kubectl delete pod <PodName>
kubectl delete -f <Pod.yml>
```
> **Note**: `.yml` or `.yaml` ?.... it doesn't matter, but it's advised for widows users to use `.yml` :)
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
## References:
- [**YAML Structure Explained**](https://www.cloudbees.com/blog/yaml-tutorial-everything-you-need-get-started)
- [**YAML explained - Great resource**](https://learnk8s.io/templating-yaml-with-code#introduction-managing-yaml-files)
- [**Kubernetes for the Absolute beginners**](https://www.udemy.com/share/1013LO3@Wfs8GSg7yXNJf2pneg2OgTWAIXOkIF5-hguWhEg51WfgYYb7vWENhvP50PHfuWji/)
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
  selector:       # A Must in ReplicaSet
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
- **Recreate**
	- This will delete the current replicaset and replace it with new updated one.
	- Usable in dev/staging environments (Downtime)
	- Not the best choice in a production environment
```yaml
spec:
  replicas: 3
  strategy:
    type: Recreate	
```
- **RollingUpdate**
	- Will create a new version of replicaset and when it's ready, the old veriosn will be deleted
	- Convenient for stateful applications that can handle rebalancing of the data
	- Rollout/rollback can take time
	- Supporting multiple APIs is hard
	- No control over traffic
```yaml
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 2        # how many pods we can add at a time
      maxUnavailable: 0  # maxUnavailable define how many pods can be unavailable
                         # during the rolling update
```

## References
- [**Kubernetes-deployment-strategies**](*https://blog.container-solutions.com/kubernetes-deployment-strategies*)
# Services
## NodePort
 A service that forwads traffic from a node to a pod, so users can access the application in a pod from the node ip.
 
 ![https://i.imgur.com/prltTNj.png](https://i.imgur.com/prltTNj.png)
- Create a NodePort service
```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    name: myapp-service
spec:
  type: NodePort
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008 # A port we will connect to
  selector:
    app: myapp
    type: front-end
```
- Create a NodePort service
```bash
kubectl create -f <File.yml>
```
 - Get the Service URL
```bash
# Minikube
minikube service <SERVICE-NAME> --url
# kubernetes cluster
kubectl port-forward svc/<SERVICE-NAME> LOCALPORT:REMOTEPORT -n <NAME>
```
> **Note**: If the label matches multiple instances, the service will distribute the load among them.
> 
## ClusterIp
Exposes the service on a cluster-internal IP. Choosing this value makes the service only reachable from within the cluster.

![](https://i.imgur.com/IoqQzAV.png)
```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    name: back-end
spec:
  type: ClusterIP
  ports:
    - targetPort: 80
      port: 80
  selector:
    app: myapp
    type: back-end
```

## LoadBalancer
On a supporting Cloud platform this will work, but on a non-supporting platform such as virtual box; it will work as a regular **Nodeport**.
```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    name: myapp-service
spec:
  type: LoadBalancer
  ports:
    - targetPort: 80
      port: 80
      nodePort: 30008
```
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
  selector:       # A Must in ReplicaSet
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
