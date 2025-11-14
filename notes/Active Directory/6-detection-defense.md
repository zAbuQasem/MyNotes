# Detection & Defense
---
# Navigation
- **[Domain admins](#Domain%20admins)**
- **[Golden Ticket](#Golden%20Ticket)**
- **[Silver Ticket](#Silver%20Ticket)**
- **[Skeleton Key](#Skeleton%20Key)**
- **[DSRM](#DSRM)**
- **[Malicious SSP](#Malicious%20SSP)**
- **[Kerberoast](#Kerberoast)**
- **[Delegation](#Delegation)**
- **[ACL attacks](#ACL%20attacks)**
- **[Trust Tickets](#Trust%20Tickets)**

---
# Domain admins
1. Do not allow or limit login of DAs to any other machine other than the Domain Controllers.If login to some servers is necessary;do not allow other administrators to login to that machine.
2. ***Try to*** never run a service with a DA.Many credential theft protections are rendered useless in case of a service account.
3. Check out temporary Group Memebership! (Requires **privileged access management** feature to be enabled which can't be turned off later).
```powershell
#Adding abuqasem to domain admins group for 20 minutes
Add-ADGroupMember -Identity 'Domain Admins' -Members abuqasem -MemberTimeToLive (New-Timespan -Minutes 20)
```
---
# Golden Ticket
**Important Event IDs:**
1. `4624:Account Logon`
2. `4672:Admin Logon`
```powershell
Get-WinEvent -FilterHashtable @{Logname='Security';ID=4672} -MaxEvents 1 | Format-List -Property *
```
---
# Silver Ticket
**Important Event IDs:**
1. `4624:Account Logon`
2. `4634:Account Logoff`
3. `4672:Admin Logon`
```powershell
Get-WinEvent -FilterHashtable @{Logname='Security';ID=4672} -MaxEvents 1 | Format-List -Property *
```
---
# Skeleton Key
**Events:**
- `7045:System Event ID` - A service was installed in the system.(Type Kernel Mode driver).

**Events ("Audit privilege use" must be enabled)**
1. `4673:Security Event ID` - Sensitive privilege use.
2. `4611`- A trusted logon process has been registered with the ***Local Security Authority***.
```powershell
Get-WinEvent -FilterHashtable @{Logname='System';ID=7045} | ?{$_.message -like "*Kernel Mode Driver*"}
```
**Mitigation**
1. Running `lsass.exe` as a protected process is really handy as it forces an attacker to load a kernel mode driver.
2. Make sure that you test it thoroughly as many drivers and plugins may not load with the protection.
```powershell
New-ItemProperty HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\ -Name RunAsPPL -Value 1 -Verbose
```
3. Verify after a reboot
```powershell
Get-WinEvent -FilterHashtable @{Logname='System';ID=12} | ?{$_.message -like "*protected process*"}
```
---
# DSRM
**Events**:
- `4657` - Audit creation/change of:
```powershell
HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\DsrmAdminLogonBehaviour
```
---
# Malicious SSP
**Events**:
- `4657` - Audit creation/change of:
```powershell
HKLM:\SYSTEM\CurrentControlSet\Control\Lsa\SecurityPackages
```
---
# Kerberoast
**Events**:
- `4769:Security Event`- A kerberoast ticket was requested.

**Mitigation**:
1. Service Account Passwords should be hard to guess (greater than 25 characters).
2. Use Managed Service Accounts (Automatic change of password periodically and delegated SPN Management).

**Since 4769 is logged very frequently o a DC. we may like to filter results based on the following information:**
1. Service name should not be `krbtgt`.
2. Service name does not end with `$` (To filter out machine accounts used for services).
3. Account name should not be `machine@domain` (To filter out requests from machines).
4. Failure code is `0x0`
5. Most importantly, ticket encryption type is `0x17`
```powershell
#One-liner for quick testing
Get-WinEvent -FilterHashtable @{Logname='Security';ID=4769} -MaxEvents 1000 | ?{$_.Message.Split("`n")[8] -ne 'krbtgt' -and $_.Message.Split("`n")[8] -ne '*$' -and $_.Message.Split("`n")[3] -notlike '$@' -and $_.Message.Split("`n")[18] -like '*0x0*' -and $_.Message.Split("`n")[17] -like "*0x17*"} | select -ExpandProperty message
```

---
# Delegation
- Limit DA/Admin logins to specific servers.
- Set "Account is sensitive and cannot be delegated" for privileged accounts.
---
# ACL attacks
**Events**:
1. `4622:Security Event`(Audit Policy for object must be enabled) - An operation was performed on an object.
2. `5136:Security Event`(Audit Policy for object must be enabled) - A directory service object was modified.
3. `4670:Security Event`(Audit Policy for object must be enabled) - Permissions on an object were changed.
> **Useful Tool:**
> [ADACLScanner](https://github.com/canix1/ADACLScanner)

---
# Trust Tickets
**SID Filtering**
- Avoid attacks which abuse SID history attribute across forest trust.
- Enabled by default on all inter-forest trusts. Intra-forest trusts are assumed secured by default (MS considers forest and not the domain to be a security boundary).
- But,since SID filtering has potential to break applications ad user access,it is often disabled.

**Selective Authentication**
- In an inter-forest trust, if Selective Authentication is configured, users between the trusts will not be automatically authenticated. Individual access to domains and servers in the trusting domain/forest should be given.