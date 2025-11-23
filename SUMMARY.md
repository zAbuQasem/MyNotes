# Table of Contents

* [Introduction](readme.md)

## Active Directory

* [Active Directory](notes/active-directory/readme.md)
* [Detection & Defense: Architectural Changes](notes/active-directory/detection-defence-architectural-changes.md)
* [Microsoft ATA (Advanced Threat Analytics).](notes/active-directory/detection-defense-ata.md)
* [Detection & Defense](notes/active-directory/detection-defense.md)
* [Phase 1: Domain Enumeration](notes/active-directory/domain-enumeration.md)
* [Domain Persistence](notes/active-directory/domain-persistence.md)
* [Domain Privesc](notes/active-directory/domain-privesc.md)
* [Lateral Movement](notes/active-directory/lateral-movement.md)
* [Local PrivEsc](notes/active-directory/local-privesc.md)
* Attack Vectors
  * [AD CS (Active Directory Certificate Services)](notes/active-directory/attack-vectors/ad-cs.md)
  * [Group Policy Preferences](notes/active-directory/attack-vectors/group-policy-preferences.md)
  * [Ipv6 DNS Takeover](notes/active-directory/attack-vectors/ipv6-dns-takeover.md)
  * [Kerberoas](notes/active-directory/attack-vectors/kerberoas.md)
  * [LAPS (Local Administrator Password Solution)](notes/active-directory/attack-vectors/laps.md)
  * [LDAP](notes/active-directory/attack-vectors/ldap.md)
  * [Microsoft SQL Server](notes/active-directory/attack-vectors/microsoft-sql-server.md)
  * [Relay attacks](notes/active-directory/attack-vectors/relay-attacks.md)
  * [Remote procedure call](notes/active-directory/attack-vectors/rpc.md)
* Powershell
  * [COM objects](notes/active-directory/powershell/com-objects.md)
  * [Offensive Powershell](notes/active-directory/powershell/offensive-powershell.md)
  * [PowerShell basics](notes/active-directory/powershell/powershell-basics.md)

## AWS Penetration Testing

* [AWS Penetration Testing](notes/aws-pentesting/readme.md)

## DevOps

* [DevOps](notes/devops/readme.md)
* [Github Actions](notes/devops/github-actions.md)
* [Image Signing](notes/devops/image-signing.md)
* [Monitoring](notes/devops/monitoring.md)
* [DevOps Tips and Tricks](notes/devops/tips-and-tricks.md)
* Iac
  * [Ansible](notes/devops/iac/ansible.md)
  * [Terraform](notes/devops/iac/terraform.md)
* Kubernetes
  * [Init-Containers](notes/devops/kubernetes/exam-preparation.md)
  * [Kubernetes](notes/devops/kubernetes/k8s-overview.md)
  * [kubectl Cheatsheet](notes/devops/kubernetes/kubectl-cheatsheet.md)
  * [Kubernetes Security](notes/devops/kubernetes/security.md)
* Open Policy Agent
  * [Rego Basics](notes/devops/open-policy-agent/rego-basics/readme.md)
    * [Rego Basics - Open Policy Agent (OPA)](notes/devops/open-policy-agent/rego-basics/basics.md)
    * [Understanding OPA Eval Results](notes/devops/open-policy-agent/rego-basics/understanding-opa-eval-results.md)

## Golang Programming

* [Golang Programming](notes/golang/readme.md)
* [Arrays and Slices](notes/golang/arrays-and-slices.md)
* [Channels](notes/golang/channels.md)
* [Concurrency (Go-routines)](notes/golang/concurrency.md)
* [Constants](notes/golang/constants.md)
* [Control Flow](notes/golang/control-flow.md)
* [Functions](notes/golang/functions.md)
* [If & Switch](notes/golang/if-switch.md)
* [Looping](notes/golang/looping.md)
* [Maps & Structs](notes/golang/maps-structs.md)
* [Misc](notes/golang/misc.md)
* [Pointers](notes/golang/pointers.md)
* [Primitives](notes/golang/primitives.md)
* [Variables](notes/golang/variables.md)
* Package

## Metasploit Framework

* [Metasploit Framework](notes/metasploit/readme.md)
* [Metasploit Cheatsheet](notes/metasploit/metasploit-cheatsheet.md)

## Red Teaming

* [Red Teaming](notes/red-teaming/readme.md)
* [Powerful Automation](notes/red-teaming/powerfull-automation.md)
* [Tunneling and Port Forwarding](notes/red-teaming/tunneling.md)
* Credential Harvesting
  * [Linux](notes/red-teaming/credential-harvesting/linux.md)
  * [MacOS](notes/red-teaming/credential-harvesting/macos.md)
  * [Miscellaneous](notes/red-teaming/credential-harvesting/misc.md)
  * [Windows](notes/red-teaming/credential-harvesting/windows.md)

## Reverse Engineering

* [Reverse Engineering](notes/reverse-engineering/readme.md)
* [Binary analysis](notes/reverse-engineering/binary-analysis.md)
* [GDB cheat sheet](notes/reverse-engineering/gdb-cheatsheet.md)

## Web Penetration Testing

* [Web Penetration Testing](notes/web-pentesting/readme.md)
* [Authentication Testing](notes/web-pentesting/authentication-testing.md)
* [Authorization Testing](notes/web-pentesting/authorization-testing.md)
* [DNS Rebinding](notes/web-pentesting/dns-rebinding.md)
* [Information Gathering](notes/web-pentesting/information-gathering.md)
* [Proxy Servers](notes/web-pentesting/proxy-servers.md)
* Iis Servers
  * [Untitled](notes/web-pentesting/iis-servers/untitled.md)
* Web Vulns
  * [Cross-Site Tracing Potential](notes/web-pentesting/web-vulns/cross-site-tracing-potential.md)
  * [CSRF](notes/web-pentesting/web-vulns/csrf.md)
  * [HTTP Parameter Pollution](notes/web-pentesting/web-vulns/hpp.md)
  * [HTTP Method Overriding](notes/web-pentesting/web-vulns/http-method-overriding.md)
  * [IMAP & SMTP injection](notes/web-pentesting/web-vulns/imap-smtp-injection.md)
  * [JWT tokens](notes/web-pentesting/web-vulns/jwt-tokens.md)
  * [LDAP Injection](notes/web-pentesting/web-vulns/ldap-injection.md)
  * [LFI bypasses](notes/web-pentesting/web-vulns/lfi.md)
  * [Open Redirect](notes/web-pentesting/web-vulns/open-redirect.md)
  * [SSI (Server Side include)](notes/web-pentesting/web-vulns/ssi-server-side-include.md)
  * [SSRF](notes/web-pentesting/web-vulns/ssrf.md)
  * [Server-Side Template Injection (SSTI)](notes/web-pentesting/web-vulns/ssti.md)
  * [XPath injection](notes/web-pentesting/web-vulns/xpath-injection.md)
  * [Cross Site Scripting](notes/web-pentesting/web-vulns/xss.md)
  * Sqli
    * [Client Side SQLi](notes/web-pentesting/web-vulns/sqli/client-side-sqli.md)
    * [MS Access](notes/web-pentesting/web-vulns/sqli/ms-access.md)
    * [MySQL](notes/web-pentesting/web-vulns/sqli/mysql.md)
    * [NoSQL](notes/web-pentesting/web-vulns/sqli/nosql.md)
    * [Oracle](notes/web-pentesting/web-vulns/sqli/oracle.md)
    * [ORM Injection](notes/web-pentesting/web-vulns/sqli/orm-injection.md)
    * [PostgreSQL](notes/web-pentesting/web-vulns/sqli/postgresql.md)
    * [SQL Server](notes/web-pentesting/web-vulns/sqli/sql-server.md)
    * [SQL Injection](notes/web-pentesting/web-vulns/sqli/sqli-overview.md)

