# Navgation
- [**Installing and runinng minikube**](#Installing%20and%20runinng%20minikube)
- [**List Nodes**](#List%20Nodes)
- [**Create a deployment**](#Create%20a%20deployment)
- [**Ports work**](#Ports%20work)
- [**Managing PODS**](#Managing%20PODS)
- [YAML intro](#YAML%20intro)
	- [YAML examples](#YAML%20examples)
---
# Installing and runinng minikube
```bash
# On debian x86_64
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start minikube with virtualbox driver
minikube start --driver=virtualbox
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
- Getting daetailed pod information
```bash
kubectl describe pod
```
- Delete a pod
```bash
kubectl delete pod <PodName>
```
---
# YAML intro
- TODO
## YAML examples
- TODO