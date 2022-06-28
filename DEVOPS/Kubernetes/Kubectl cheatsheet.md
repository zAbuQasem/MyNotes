# Navgation
- [**Installing and runinng minikube**](#Installing%20and%20runinng%20minikube)
- [**Create a deployment**](#Create%20a%20deployment)
- [**Namepaces**](#Namepaces)
- [**Managing PODS**](#Managing%20PODS)
- [**Ports work**](#Ports%20work)
- [**YAML**](#YAML)
- [**Replicas**](#Replicas)

# Installing and runinng minikube
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


# Create a deployment
A **Kubernetes Deployment** is used to tell Kubernetes how to create or modify instances of the pods that hold a containerized application. Deployments can scale the number of replica pods, enable rollout of updated code in a controlled manner, or roll back to an earlier deployment version if necessary. [**More info**](https://www.vmware.com/topics/glossary/content/kubernetes-deployment.html)
```bash
# Creating the deployment
kubectl create deployment hello-minikube --image=k8s.gcr.io/echoserver:1.4

# Checking the deployment
kubectl get deployment

# Listing services
kubectl get services # All
kubectl get services hello-minikube # Specific

# Delete a service
kubectl delete services hello-minikube

# Delete all minikube clusters
minikube delete --all
```
> **Note**:
> Creating a deployment will have a replica set to 1; so when you delete a pod -> a new pod will be initiated. To override this you must set the `restartPolicy` to `Never`.
---
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
# Managing PODS
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
# Change an image for a pod
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
# Ports work
- Exposing a port
```bash
kubectl expose deployment hello-minikube --type=NodePort --port=8080

# Get the Exposed port access URL
minikube service hello-minikube --url
```
- PortForwarding
```bash
# Local:Remote 
kubectl port-forward service/hello-minikube 7080:8080 
```
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
- List `ReplicaSet`
```bash
kubectl get replicaset
```
- Delete replicasets
```bash
kubectl delete replicasets/<SET>
```
- Describe replicasets
```bash
kubectl describe replicasets/<SET>
```