# PortForwarding
## Chisel
- Server
```bash
chisel --reverse --host <IP> --port <PORT> --reverse
```
- Client
```bash
chisel client <SERVER-IP>:<SERVER-PORT> R:ATTACKER-PORTFWD:<VICTIM-IP>:VICTIM-PORTFWD
```