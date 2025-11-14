# Remote procedure call
---
## What's RPC?
Remote Procedure Call (RPC) is a protocol that one program can use to request a service from a program located in another computer on a network without having to understand the network's details. RPC is used to call other processes on the remote systems like a local system. A procedure call is also sometimes known as a _function call_ or a _subroutine call_.
## Enumerating RPC
```bash
#Connecting
rpcclient <ip> -U <username>

#Enumerate domain users
enumdomusers

#Enumerate domain groups
enumdomgroups
```
>  Commands -> [**RPC**](https://www.blackhillsinfosec.com/password-spraying-other-fun-with-rpcclient/)

## Tools
-  **RPCrecon** -> [https://github.com/m4lal0/RPCrecon](https://github.com/m4lal0/RPCrecon)

## Further reading
- https://searchapparchitecture.techtarget.com/definition/Remote-Procedure-Call-RPC
- https://book.hacktricks.xyz/pentesting/135-pentesting-msrpc