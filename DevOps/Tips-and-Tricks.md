# Navigation
 - [Distroless Containers](#distroless-containers)

# Distroless Containers
## Debug Network Connections
You can use nsenter to enter the network namespace of a running container for debugging network issues.

1. Get the container’s PID:
```bash
docker inspect --format '{{.State.Pid}}' <container_name_or_id>
```
2. Enter the container’s network namespace and check active connections:
```bash
sudo nsenter -n -t <PID> ss -pant
```
This allows you to run network debugging commands like `ss`, `netstat`, or `curl` even in Distroless containers where shell tools are not available.

### References
- [Docker Container Execute Commands with nsenter - iximiuz Labs](https://labs.iximiuz.com/challenges/docker-container-execute-commands-with-nsenter)
- [nsenter Gist by fmarchioni](https://gist.github.com/fmarchioni/5f1faf6586e6f371974a22078234fb09)