# Group Policy Preferences
---
# What's GPP?
**Group Policy Preferences** is a collection of Group Policy client-side extensions that deliver preference settings to domain-joined computers running Microsoft Windows desktop and server operating systems. Preference settings are administrative configuration choices deployed to desktops and servers. Preference settings differ from policy settings because users have a choice to alter the administrative configuration. Policy settings administratively enforce setting, which restricts user choice.
# Understanding MS14-025
Embedding credentials in group policy preferences solved a lot of problems for administrators. A GPP could be used to easily apply a common local administrator password to all workstations etc..
While the functionality of GPPs is very powerful, the mechanism of storing those credentials was compromised in a way that made them trivial to decrypt.
  > **Importatnt Note**: GPPs are stored on the domain controller in the SYSVOL share, this means that at a minimum all domain users can access the encrypted credentials.

# Attacking GPPs
Finding `*.xml`and extracting the `cpassword` hash,Then decrypting it with `gpp-decrypt`
```bash
gpp-decrypt <HASH>
```
Using Metasploit
```bash
use smb_enum_gpp
```
Search in _**C:\ProgramData\Microsoft\Group Policy\history**_ or in _**C:\Documents and Settings\All Users\Application Data\Microsoft\Group Policy\history**_ _(previous to W Vista)_ for these files:
-   Groups.xml
-   Services.xml
-   Scheduledtasks.xml    
-   DataSources.xml
-   Printers.xml
-   Drives.xml
# Further reading
- https://www.rapid7.com/blog/post/2016/07/27/pentesting-in-the-real-world-group-policy-pwnage/
- https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/dn581922(v=ws.11)