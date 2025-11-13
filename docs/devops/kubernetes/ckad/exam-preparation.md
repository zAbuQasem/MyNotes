# Init-Containers
Init Containers are specialized containers that run before app containers in a Pod. They can contain utilities or setup scripts not present in an app image. Once the Init Container completes successfully, it is removed, and the main application containers start.

## Commands 
- **Examples**:
```yaml
  initContainers:
    - name: init-myservice
      image: busybox
      command: ['sh', '-c', 'echo Initializing...; sleep 5']
```

This snippet runs a simple `busybox` container that waits for 5 seconds, simulating an initialization task before the main containers start.

## Troubleshooting
- **Viewing Init Container logs**:
```bash
kubectl logs <pod-name> -c <init-container-name>
```
- **Debugging Init Containers**:
```bash
kubectl describe pod <pod-name>
```
---
# Pod-Design

### Definition

A Pod in Kubernetes is the smallest deployable unit. It can contain one or more containers, each designed to work together and share storage/networking resources. Good Pod design involves:

- Grouping containers that share resources and are tightly coupled.
- Ensuring each Pod has a single, clearly defined purpose (e.g., run a service, handle a batch job).
## Commands

- **Creating a Pod**:
```bash
kubectl apply -f my-pod.yaml
```
- **Describing a Pod**:
```bash
kubectl describe pod <pod-name>
```
- **Viewing Pod logs**:
```bash
kubectl logs <pod-name> -c <container-name>
```

# State-Persistence

## StatefulSets

A StatefulSet manages the deployment and scaling of a group of Pods while maintaining the identity and state of each Pod. They are commonly used for stateful applications like databases, messaging queues, or any service that must remember data even if it’s rescheduled on different nodes.

### Usage

- Each Pod in a StatefulSet has a unique identifier (ordinal index).
- Pods keep a stable network identity, ensuring consistent DNS names.
- PersistentVolumeClaims (PVCs) are often used to retain data across Pod restarts.
### Commands

- **Deploying a StatefulSet**:
```bash
kubectl apply -f my-statefulset.yaml
```
- **Scaling a StatefulSet**:
```bash
kubectl scale statefulset my-db --replicas=3
```
- **Checking StatefulSet status**:
```bash
kubectl get statefulset
```
## Headless-Services

A Headless Service is a Service with no ClusterIP assigned. It allows you to directly reach Pods by their hostnames. This is useful for:

- Applications requiring direct Pod-to-Pod communication.
- Enabling service discovery mechanisms that rely on DNS records for each Pod.

## Usage

- Typically used in conjunction with StatefulSets.
- Provides DNS records for each Pod with a consistent pattern like `<pod-name>.<service-name>.<namespace>.svc.cluster.local`.

### Commands

- **Creating a Headless Service**:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: my-service
spec:
  clusterIP: None
  selector:
	app: my-app
  ports:
	- port: 80
```
- **Verifying**
```bash
kubectl get svc my-service
# Output shows 'None' for the ClusterIP
```
# Security

## Admission-Controls

Admission Controllers are plugins in the Kubernetes API Server that process requests before objects are persisted. They can modify or reject requests to enforce policies:

- **PodSecurityPolicy** (deprecated, replaced by Pod Security Admission).
- **ResourceQuota** to limit resource usage.
- **MutatingWebhook** or **ValidatingWebhook** for custom admission logic.

## API-Security

Securing the Kubernetes API involves:

- Role-Based Access Control (RBAC): Restricting access based on roles and cluster roles.
- Certificates & TLS: Ensuring communication with the API server is encrypted.
- Enforcing strong authentication/authorization mechanisms and limiting who can issue commands.

## CRDs

Custom Resource Definitions (CRDs) allow you to create custom resources in Kubernetes. This extends Kubernetes capabilities without modifying the core code:

- **Usage**:
    - Define a new resource type (e.g., `CronTab`, `FooBar`).
    - Interact with it using `kubectl` and controllers/operators.
- **Example CRD**:
    
```yaml
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: crontabs.example.com
spec:
  group: example.com
  versions:
	- name: v1
	  served: true
	  storage: true
  scope: Namespaced
  names:
	plural: crontabs
	singular: crontab
	kind: CronTab
```
