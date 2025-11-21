# Kubernetes Security

Container and cluster security best practices.

---

## Docker

### Volumes-vs-Mounts
|Volumes|Mounts|
|-|-|
|Easier to backup/migrate|Harder to backup/migrate|
|work on both Linux and Windows containers|Linux Only|
|More safely shared among multiple containers|X|
|Much higher performance|X|
|Can't be mounted as ReadOnly|Can be mounted as ReadOnly|
- Volume Syntax
```bash
docker run -v <CurrentFolder>:<Destination>
```
- Mount Syntax (Preferred)
```bash
docker service create \
    --mount 'type=volume,src=<VOLUME-NAME>,dst=<CONTAINER-PATH>,volume-driver=local,volume-opt=type=nfs,volume-opt=device=<nfs-server>:<nfs-path>,"volume-opt=o=addr=<nfs-address>,vers=4,soft,timeo=180,bg,tcp,rw"' \
    --name myservice \
    <IMAGE>
```

### References
- [best-practices-for-securing-containers](https://medium.com/@axbaretto/best-practices-for-securing-containers-8bf8ae0d9952)
## Privileged-Containers

- **Full Host Access**: A privileged container essentially has the same privileges as processes running on the host. This means it has unrestricted access to the host system's resources, including devices, filesystems, and kernel capabilities.
- **Mounting Filesystems**: Privileged containers can mount arbitrary filesystems, including special ones such as `sysfs`, `proc`, and `tmpfs`. They can also mount volumes from the host system.
- **Mount Namespace**: Privileged containers are not restricted by the mount namespace of the container runtime. This means they can see all mounts on the host system.    
- **Full Filesystem Access**: They can access and manipulate any file on the host system that the user running the container has permissions to access.
## Non-Privileged Containers

- **Limited Host Access**: A non-privileged container is constrained and does not have direct access to host resources. It runs with reduced capabilities and permissions compared to the host system.
    
- **Filesystem Restrictions**: Non-privileged containers have restrictions on mounting certain filesystems. They typically cannot mount `sysfs`, `proc`, or `tmpfs` without specific configuration or elevated permissions.
    
- **Mount Namespace Isolation**: Non-privileged containers operate within their own mount namespace, which means they cannot see or interact with mounts outside of their namespace. This provides a level of isolation and security.
    
- **Filesystem Access**: Non-privileged containers have limited access to the host system's filesystem. They can access only the files and directories that are explicitly shared with them through volumes or bind mounts.