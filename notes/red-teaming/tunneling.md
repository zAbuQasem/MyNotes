# Tunneling and Port Forwarding

Network tunneling techniques for penetration testing.

## Chisel
- Server
```bash
chisel --reverse --host <IP> --port <PORT> --reverse
```
- Client
```bash
chisel client <SERVER-IP>:<SERVER-PORT> R:ATTACKER-PORTFWD:<VICTIM-IP>:VICTIM-PORTFWD
```
> **Note**: Both server and client must be the same version

## References
- https://0xdf.gitlab.io/2020/08/10/tunneling-with-chisel-and-ssf-update.html
