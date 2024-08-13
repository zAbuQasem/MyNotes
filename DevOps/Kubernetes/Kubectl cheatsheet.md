# Navigation
- [**Installing-and-runinng-minikube**](#Installing-and-runinng-minikube)
- [**EKS**](#EKS)
- [**NameSpaces**](#NameSpaces)
- [**Managing-PODS**](#Managing-PODS)
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
- [**Commands**](#Commands)
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
	- This will delete the current `ReplicaSet` and replace it with new updated one.
	- Usable in dev/staging environments (Downtime)
	- Not the best choice in a production environment
```yaml
spec:
  replicas: 3
  strategy:
    type: Recreate	
```

- **RollingUpdate**
	- Will create a new version of `ReplicaSet` and when it's ready, the old version will be deleted
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

- Rollout commands
```sh
kubectl rollout status <DEPLOYMENT>
kubectl rollout history <DEPLOYMENT>
kubectl rollout undo <DEPLOYMENT>
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

## Taints-and-Tolerations
Supposing a node have a taint called blue, no pods can be placed on it  except ones which is tolerant to blue.

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

## NodeSelector-and-NodeAffinity
Control how the schedular will place pods on specifc nodes based on pre-defined attributes.
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: with-node-affinity
spec:
  affinity:
    nodeAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        nodeSelectorTerms:
        - matchExpressions:
          - key: topology.kubernetes.io/zone
            operator: In
            values:
            - antarctica-east1
            - antarctica-west1
      preferredDuringSchedulingIgnoredDuringExecution:
      - weight: 1
        preference:
          matchExpressions:
          - key: another-node-label-key
            operator: In
            values:
            - another-node-label-value
  containers:
  - name: with-node-affinity
    image: k8s.gcr.io/pause:2.0
```
### Reference
- https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/

## Daemon-Sets
ReplicaSet ensures that the number of pods of an application is running on the correct scale as specified in the conf file. Whereas in the case of DaemonSet it will ensure that **one copy of pod defined in our configuration will always be available on every worker node.**
```yml
apiVersion: v1
kind: DaemonSet
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
# Commands
Commands in manifest override `ENTRYPOINT` and `CMD` in Dockerfile
```yml
apiVersion: v1
kind: Pod
metadata:
  name: command-demo
  labels:
    purpose: demonstrate-command
spec:
  containers:
  - name: command-demo-container
    image: debian
    command: ["printenv"]
    args: ["HOSTNAME", "KUBERNETES_PORT"]
    restartPolicy: OnFailure
#   command:
#     - "sleep"
#     - "5000"
```
> **Note**: You cannot change command while the pod is running

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
    hostPath:    # Mount on the host machine
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