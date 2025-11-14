# DevOps Tips and Tricks

Useful DevOps techniques and best practices.

## Navigation
 - [Distroless Containers](#distroless-containers)

---

## Debug Network Connections
You can use nsenter to enter the network namespace of a running container for debugging network issues.

1. Get the container’s PID:
```
docker inspect --format '{{.State.Pid}}' <container_name_or_id>
```
2. Enter the container’s network namespace and check active connections:
```
sudo nsenter -n -t <PID> ss -pant
```
This allows you to run network debugging commands like `ss`, `netstat`, or `curl` even in Distroless containers where shell tools are not available.

## Send Signals
Since containers run in child PID namespaces, processes in the container are visible from the host. You can find the host PID and send signals directly:
```bash
## 1. Find the process on the host:
ps aux | grep <process_name>

## 2. Check process IDs in both namespaces:
cat /proc/<host_pid>/status | grep NSpid
## NSpid: <host_pid> <container_pid>

## 3. Send the signal using the host PID:
sudo kill -SIGALRM <host_pid>
```

### References
- [Docker Container Execute Commands with nsenter - iximiuz Labs](https://labs.iximiuz.com/challenges/docker-container-execute-commands-with-nsenter)
- [nsenter Gist by fmarchioni](https://gist.github.com/fmarchioni/5f1faf6586e6f371974a22078234fb09)
- [Sending a Signal From the Host](https://www.baeldung.com/linux/docker-send-signals-to-process#sending-a-signal-from-the-host)
