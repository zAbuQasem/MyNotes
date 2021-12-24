# LDAP
---
# What's LDAP?
Lightweight directory access protocol (LDAP) is a protocol that makes it possible for applications to query user information rapidly.
Companies store usernames, passwords, email addresses, printer connections, and other static data within directories. LDAP is an open, vendor-neutral application protocol for accessing and maintaining that data. LDAP can also tackle authentication, so users can sign in just once and access many different files on the server.
 
## Dumping LDAP Objects 
 ```bash
 #install -> pip install ldapdomaindump
 ldapdomaindump <IP> [-r <IP>] -u '<domain>\<username>' -p '<password>' [--authtype SIMPLE] --no-json --no-grep [-o /path/dir]
 ```
## Adding records
- Preferred Tool [**dnstoolpy**](https://github.com/dirkjanm/krbrelayx/blob/master/dnstool.py)
```bash
dnstool.py -u DOMAIN\\USERNAME -p PASSWORD -r FAKESYSTEM.FQDN -a add -d YOUR_IP [DC_HOSTNAME/VICTIM-IP]
```

# Further reading
- https://www.okta.com/identity-101/what-is-ldap/
- https://book.hacktricks.xyz/pentesting/pentesting-ldap