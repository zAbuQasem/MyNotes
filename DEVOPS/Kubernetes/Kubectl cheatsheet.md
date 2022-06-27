# Navgation
- [**Installing and runinng minikube**](#Installing%20and%20runinng%20minikube)
- [**List Nodes**](#List%20Nodes)
- [**Create a deployment**](#Create%20a%20deployment)
- [**Ports work**](#Ports%20work)
- [**Managing PODS**](#Managing%20PODS)
- [**YAML**](#YAML)
---
# Installing and runinng minikube
```bash
# On debian x86_64
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start minikube with virtualbox driver
minikube start --driver=virtualbox

# If you faced some issues related to VTS on windows 11 (while it's enabled) 
minikube start --no-vtx-check --driver virtualbox
```
> **Important Notes**:
> - On failure run `minikube delete && minikube start` if it didn't work then follow the traceback instructions
> - [**Click me for other distros installation guide**](https://minikube.sigs.k8s.io/docs/start/) 

---
#  List Nodes
```bash
kubectl get nodes
```
---
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
---
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
---
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
---
# YAML
It is a good practice to declare resource requests and limits for both [memory](https://kubernetes.io/docs/tasks/configure-pod-container/assign-memory-resource/) and [cpu](https://kubernetes.io/docs/tasks/configure-pod-container/assign-cpu-resource/) for each container. This helps to schedule the container to a node that has available resources for your Pod, and also so that your Pod does not use resources that other Pods needs.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: abuqasem-firstpod # Always lowercase
  labels: 
    app: myapp
    type: server
    env: production
    tier: frontend
spec:
  containers:
  - name: abuqasem-nginx-container # Always lowercase
    image: nginx
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