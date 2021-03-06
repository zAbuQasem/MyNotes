# Phase 1: Domain Enumeration
---
## Navigation
- **[Computers Enumeration](#Computers%20Enumeration)**
- **[Domain Name Enumeration](#Domain%20Name%20Enumeration)**
- **[Domain Policy Enumeration](#Domain%20Policy%20Enumeration)**
- **[Domain Controller Enumeration](#Domain%20Controller%20Enumeration)**
- **[User Enumeration](#User%20Enumeration)**
- **[User hunting](#User%20hunting)**
- **[Groups Enumeration](#Groups%20Enumeration)**
- **[Group Policy GPO](#Group%20Policy%20GPO)**
- **[Access Control Model](#Access%20Control%20Model)**
- **[Trusts](#Trusts)**
- **[BloodHound](#BloodHound)**
## Preffered Tools:
**Note:** This can be done with any other  tool but we are presenting those only
- [**PowerView**](https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon)
- [**ADModule**](https://github.com/samratashok/ADModule)
# Computers Enumeration
### Get alist of computers in the current domain
```powershell
#Powerview
Get-NetComputer
Get-NetComputer -OperatingSystem
Get-NetComputer -ping
Get-NetComputer -FullData
#ActiveDirectory Module
Get-ADComputer -Filter * | select Name
Get-ADComputer -Filter 'OperatingSystem -like "*Server 2016*"' -Properties OperatingSystem | select Name,OperatingSystem
Get-ADComputer -Filter * -Properties DNSHostName | %{Test-Connection -count 1 -ComputerName $_.DNSHostName}  #May give false positives
Get-ADComputer -Filter * -Properties *
```
---
# Domain Name Enumeration
### Get current domain
```powershell
#Using .NET classes
$ADClass = [System.DirectoryServices.ActiveDirectory.Domain]
$ADClass::GetCurrentDomain()
#Powerview
Get-NetDomain
#ActiveDirectory Module
Get-ADDomain
```
### Get Object of another domain
```powershell
#Powerview
Get-NetDomain -Domain <DOMAIN>
#ActiveDirectory Module
Get-ADDomain -Identity <DOMAIN>
```

### Get domain SID for the current domain
```powershell
Get-DomainSID
#(Active Directory module)
(GET-ADDomain).DomainSID 
```
---

# Domain Policy Enumeration
### Get domain policy for the current domain
```powershell
(Get-DomainPolicy)."system access" #(between quotes can be Kerberos policy ..etc)
```

### Get domain policy for another domain
```powershell
(Get-DomainPolicy -domain <DOMAIN>."system access" #(between quotes can be Kerberos policy ..etc)
```
---
# Domain Controller Enumeration
### Get domain controllers for the current domain
```powershell
#Powerview
Get-NetDomainController
#ActiveDirectory Module
Get-ADDomainController 
```
### Get domain controller for another domain
```powershell
#Powerview
Get-NetDomainController -Domain <DOMAIN> 
#ActiveDirectory Module
Get-ADDomainController -DomainName <DOMAIN> -Discover
```
---
# User Enumeration
### Get a list of users in the current domain
```powershell
#Powerview
Get-NetUser 
Get-NetUser -Username omar1 
#ActiveDirectory Module
Get-ADuser -Filter * -Properties *  
```
### Get list of all properties for users in the current domain
```powershell
Get-UserProperty
Get-UserProperty -Properties pwdlastset
#(Active Directory module)
Get-ADUser -Filter * -Properties * | select -First 1 | Get-Member -MemberType *Property | select Name
Get-ADUser -Filter * -Properties * | select name, @{expression {[datetime]::fromfiletime($_.pwdlastset)}}   
```
### Get information about passwords
```powershell
#Last time a password was changed
Get-UserProperty -Properties pwdlastset
#Bad password count
Get-UserProperty -Properties badpwdcount
#Filtering inactive users
Get-UserProperty -Properties logoncount
#Searching for passwords in user's description
Find-UserField -SearchField Description -SearchTerm "built"
Get-ADUser - Filter 'Description -like "*built*"' -Properties Description | select name,Description
```
#### Note:
- Searching for passwords in user's description is a thing because users may have to change their passwords frequently so they include it in the description so they don't have to memorize it.
---
# Groups Enumeration
- [**Groups Explained**](http://www.harmj0y.net/blog/activedirectory/a-pentesters-guide-to-group-scoping/)
### Get all the groups in the current domain
```powershell
#Powerview
Get-NetGroup -Domain <DOMAIN>
Get-NetGroup -FullData
Get-NetGroup *admin* #Only containing admin in groupname
#ActiveDirectory Module
Get-ADGroup -Filter * | select Name
Get-ADGroup -Filter * -Properties *
Get-ADGroup -Filter 'Name -like "*admin*"' | select Name  #Only containing admin in groupname
```
### Get all memebers of the domain Admins group
```powershell
#Powerview
Get-NetGroupMember -GroupName "Domain Admins" -Recurse
Get-NetGroupMember -Username "khaled1" #To get the group membership for a specific user
#ActiveDirectory Module
Get-ADGroupMember -Identity "Domain Admins" -Recursive
Get-ADPrincipalGroupMembership -Identity khaled1  #To get the group membership for a specific user
```
### List all local groups on a machine
- Needs admin priviliges or non-dc machines
```powershell
#Powerview
Get-NetLocalGroup -ComputerName <NAME> -ListGroups
#To get member of all local groups on a machine
Get-NetLocalGroup -ComputerName <NAME> -Recurse
```
- Find shares on hosts in current domain
 ```powershell
 Invoke-ShareFinder -Verbose
 ```
- Find Sesitive files on computers in the domain
```powershell
Invoke-FileFinder -Verbose
```
- Get all fileservers of the domain

```powershell
Get-NetFileServer
```
---

# Group Policy (GPO)
#### Provides the ability to manage configuration and changes easily and centraly in AD.
### Allows control of:
- Security settings.
- Registery-based policy settings.
- Group policy preferences like startup/shutdown/log-on/logff/scripts/settings
**Note:** Can be abused for various attacks like PrivESC,backdoors,persistence ..etc.
### Get list of GPO in current domain
```powershell
#Powerview
Get-NetGPO
Get-NetGPO -ComputerName <COMPUTER-NAME>

#GroupPolicy module
Get-GPO -All
Get-GPReusltSetOfPolicy -ReportType Html -Path C:\Users\Administrator\report.html  #(Provides RSoP)
```
### Get GPO(s) which user Restricted Groups or groups.xml for interesting users
```powershell
#Powerview
Get-NetGPOGroup
```
### Get users in local group of machine using GPO
```powershell
Find-GPOComputerAdmin -ComputerName <Computer-Name>
```
### Get machines where the given user is member of a specific group
```powershell
Find-GPOLocation -UserName <user> -Verbose
```
### Get OUs in domain
```powershell
#Powerview
Get-NetOU -FullData
Get-ADorganizationalUnit -Filter * -Properties *
```
### Get GPO applied on an OU
**Note:**Read GPOname from gplink attribute from  `Get-NetOU`
```powershell
#Powerview
Get-NetOU -GPOname "{STRING}"

#GroupPoicy Module
Get-GPO -Guid "STRING" #without brackets
```
---
# Access Control Model
#### Enabels control on the ability of a process to access objects and other resources in an AD based on:
- Access Tokens (Security context of a process-identity and privs of a user)
- Security Descriptors (SID of the owner,Discretionary ACL (DACL) and system ACL (SACl))

![[Pentesting/Active Directory/attachments/ACl.png]]
### Get the ACLs associated with the specified object
```powershell
Get-ObjectAcl -SamAccountName <User-Name> -ResloveGUIDs

#Active Directory Module (Doesn't resolve GUIDs)
(Get-ACL 'AD:\CN=Administrator,CN=Users,DC=<Domain-controller>,DC=<Current-Domain>,DC=local').Access
```
### Get the ACLs associated with the specified prefix to be used for search
```powershell
Get-ObjectAcl -ADSprefix 'CN=Administrator,CN=Users' -Verbose
```
### Get ACLs associated with the specified LDAP path to be used for search 
```powershell
Get-ObjectAcl -ADSpath "LDAP://CN=Domain Admins,CN=Users,DC=<Domain-controller>,DC=<Current-Domain>,DC=local" -ResolveGUIDs -Verbose
```
### Search for interesting ACEs
```powershell
Invoke-ACLScanner -ResolveGUIDs
```
### Get the ACLs associated with the specified path
```powershell
Get-PathAcl -Path "\\<Current Domain\sysvol"
```
---
# Trusts
### Get a list of all domain trusts for the current domain
```powershell
#Powerview
Get-NetDomainTrust
Get-NetDomainTrust -Domain <Domain>

#Active Directory module
Get-ADTrust
Get-ADTrust -Identity <Domain>
```
## Forest mapping
### Get detail about thr current forest
```powershell
#Powerview
Get-NetForest
Get-NetForest -Forest <Forest>

#Active Directory Module
Get-ADForest
Get-ADForest -Identity <Forest>
```
### Get all domoains in the current forest
```powershell
GetNetForestDomain
GetNetForestDomain -Forest  <Forest>

#Active Directory Module
(Get-ADForest).Domains
```

### Get all global catalogs for the current forest
```powershell
Get-NetForestCatalog
Get-NetForestCatalog -Forest <forest>

#Active Directory module
Get-ADForest | select -ExpandProperty GlobalCatalogs
```
### Map trusts of a forest
```powershell
#Powerview
Get-NetForest
Get-NetForest -Forest <forest>

#Active Directory module
Get-ADTrust
Get-ADTrust -Filter 'msDS-TrustForestTrustInfo -ne "$null"'
```
---
# User hunting
### Find all machines on the current domain (Where the current user has ***local admin access***)
```powershell
Find-LocalAdminAccess -Verbose
```
Above function queries the DC the current or provided domain for a list of computers **Get-NetComputer** and then use multi-threaded  **Invoke-CheckLocalAdminAccess **on each machine. (Very Noisy)

![[enumeratelocaladmin.png]]

This can also be done with the help of remote administration tools like WMI and PowerShell remoting because when **SMB** and **RPC** are disabled the `FindLocalAdminAccess` is blocked.
- Use [**Find-WMILocalAdminAccess.ps1**](https://github.com/admin0987654321/admin1/blob/master/Find-WMILocalAdminAccess.ps1) (Very Noisy)
```powershell 
Find-WMILocalAdminAccess.ps1 -ComputerFile <listofcomputers>  #Get the list with Get-NetComputer
```
### Find local admins on all machines of the domain (Needs admin privs for non-dc machines).
```powershell
Invoke-EnumerateLocalAdmin -Verbose
```
Above function queries the DC the current or provided domain for a list of computers `Get-NetComputer` and then use multi-threaded  `GetNetLocalGroup` on each machine. (Very Noisy)
- Same concept as the above pic.
### Find Computers where a domain admin (or specified user/group) has sessions
```powershell
Invoke-UserHunter
INvoke-UserHunter -GroupName "RDPUsers"
```
Above function queries the DC the current or provided domain for given group (**Domain admin by default**) using **Get-NtGroupMember**, gets a list of computers (**Get-NetComputer**) and list sessions and logged on users (**Get-NetSession/GetNetLoggedon**) from each machine. (Very Noisy)
### To confirm admin access
```powershell
Invoke-UserHunter -CheckAccess
```
### Find computers where a domain admin is logged-in
```powershell
Invoke-UserHunter -Stealth
```
Above option queries of the DC of the current or provided domain for members of the given group (Domain Admins by default) using **Get-NetGroupMember**,gets a list **only** of high traffic servers (DC,File Servers and Distributed File Servers) for less traffic generation and list sessions and logged on users (**Get-NetSession/Get-NetLoggedon**) for each machine.

---
# BloodHound
- Supply data to BloodHound
```powershell
C:\PATH\BloodHound-master\Ingestors\SharpHound.ps1
Invoke-BloodHound -CollectionMethod All -Verbose
#If it didn't collect Sessions you can get them easily by:
Invoke-BloodHound -CollectionMethod LoggedOn -Verbose
#The generated archive can be uploaded to the BloodHound application

#To avoid detections like ATA
Invoke-BloodHound -CollectionMethod All -ExcludeDC -Verbose

#From linux
crackmapexec smb <TARGET[s]> -u <USERNAME> -p <PASSWORD> -d <DOMAIN> -M bloodhound
```
