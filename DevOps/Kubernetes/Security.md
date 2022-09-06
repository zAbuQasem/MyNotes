# Navigation
- [**Docker**](#Docker)
# Docker
## Volumes-vs-Mounts
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
- Mount Syntax
```bash
docker service create \
    --mount 'type=volume,src=<VOLUME-NAME>,dst=<CONTAINER-PATH>,volume-driver=local,volume-opt=type=nfs,volume-opt=device=<nfs-server>:<nfs-path>,"volume-opt=o=addr=<nfs-address>,vers=4,soft,timeo=180,bg,tcp,rw"' \
    --name myservice \
    <IMAGE>
```
https://medium.com/@axbaretto/best-practices-for-securing-containers-8bf8ae0d9952
https://docs.docker.com/storage/bind-mounts/
https://docs.docker.com/storage/volumes/