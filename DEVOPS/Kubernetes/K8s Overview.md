# Kubernetes
Kubernetes is a container orchestration technology the most popular of it all – is a bit difficult to setup and get started but provides a lot of options to customize deployments and supports deployment of complex architectures. Kubernetes is now supported on all public cloud service providers like GCP, Azure and AWS.
## Kubernetes components
Kubernetes follows a **client-server** architecture. In Kubernetes, multiple master nodes control multiple worker nodes. Each master and worker has a set of components that are required for the cluster to work correctly.
**A master node generally has the following:** 
- **kube-apiserver**  : A control-plane component that validates and configures data for objects such as pods, services, and controllers. It interacts with objects using REST requests.
- **etcd storage**: A high-availability key-value store used to store data such as configuration, state, and metadata. The watch functionality of etcd provides Kubernetes with the ability to listen for updates to configuration and make changes accordingly.
- **kube-controller-manager** : A combination of the core controllers that watch for state updates and make changes to the cluster accordingly. 
	- **Replication controller**: Maintains correct number of pods for every replication. 
	- **Node controller**: Monitor changes to the nodes.
	- **Endpoints controller**: Populates the endpoint object, which is responsible for joining the service object and the pod object.
	- **Service accounts and tokens controller**: Creates default accounts and API tokens for new namespaces.
- **cloud-controller-manager**: It runs controllers to interact with the underlying cloud providers.
- **kube-scheduler** : Watches for newly created pods and assigns pods to the nodes. The scheduler first filters a set of nodes on which the pod can run. Filtering includes creating a list of possible nodes based on available resources and policies set by the user. Once this list is created, the scheduler ranks the nodes to find the most optimal node for the pod.

**The worker nodes have the following:** 
- **kubelet**: kubelet runs on every node. It registers the node with the API server. It monitors pods created using Podspecs and ensures that the pods and containers are healthy.
- **kube-proxy**: A networking proxy that runs on each node. It manages the networking rules on each node and forwards or filters traffic based on these rules.
- **Container Runtime Interface (CRI)** 
- **Container Storage Interface (CRI)**

![**Structure Diagram**](https://lh3.googleusercontent.com/fcma7jkaqVAht_xXrIachkI_hnh6CmOHTNCoMVT1dMEpNcjdEXtPkFCDO2jJQs1-dL4WZhhApKVql_2Waxuq4ag8VDAGd9s1N0WyNL2zEXvsN63vz-hI9Pq7baiKLQcaYV3hTbB8)