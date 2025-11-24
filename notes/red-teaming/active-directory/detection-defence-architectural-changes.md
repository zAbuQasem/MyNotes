# Detection & Defense: Architectural Changes

Defensive architecture and security controls for Active Directory.

---

## Local Administrator Password Solution (LAPS)
- Centralized storage of passwords in AD with periodic randomization where read permissions are access controlled.
- Computer objects have two new attributes `ms-mcs-AdmPwd` and `ms-mcs-AdmPwdExpirationTime` controls the password change.
- Storage is in clear text and transmission is encrypted.
- With careful enumeration, it is possible to retrieve which users can access the clear text password providing a list of attractive targets.
- An attacker can now dump LAPS from linux using [LapsDumper](https://github.com/n00py/LAPSDumper)

> **Further reading** : https://www.n00py.io/2020/12/dumping-laps-passwords-from-linux/
## Credential guard
- Now called `Windows Defender Credential Guard` it uses virtualization based security to isolate secrets so that only privileged system software can access them.
- Effective in stopping `PTH` and `Over-PTH` attacks by restricting access to NTLM hashes and TGTs.As of `windows 10 1709` it is not possible to write kerbroas tickets into memory **even** if you have credentials.

## Important notes about credential guard
1. Credentials for local accounts in SAM and Service account credentials from LSA secrets are **NOT** protected.
2. Credential guard **cannot be enabled on a domain controller** as it breaks authentication there.
3. ONly available on the windows 10 enterprise edition and server 2016.
4. It has proved **possible to relay service account credentials** even if credential guard is enabled.

## Device guard
- Now called `Windows Defender Device Guard` it's a group of features **designed to harden a system against malware attacks** .it focus on preventing malicious code from running by ensuring only known good code can run.
- **Three primary components:**
	1. Configurable Code Integrity (CCI) - Configure only trusted code to run.
	2. Virtual Secure Mode Protected Code Integrity - Enforces CCI with kernel Mode (KMCI) and User Mode (UMCI).
	3. Platform and UEFI secure boot - Ensures boot binaries and firmware integrity.
## Protected Users Group
	- Is  a group introduced in server 2012 R2 for **better protection against credential theft** by not caching credentials in insecure ways. **A user added to this group:**
		- Cannot use `CredSSP` and `WDigest` - No more clear text credentials caching.
		- NTLM hash is not cached.
		- Kerberos doesn't use DES and RC4 keys - No caching of clear text and long term keys.
	- **If the domain functional level is server  2012 R2:**
		- No NTLM authentication
		- No DES or RC4 in Kerberos pre-authentication.
		- No delegation.
		- No renewal of TGT beyond initial for hour lifetime - Hardcoded, unconfigurable `Maximum lifetime for user ticket` and `Maximum lifetime for user ticket renewal`.
	- Needs all domain control to be at least server 2008 or  later (because AES keys).
	- Not Recommended by MS to add DAs ad EAs to this group without testing the **potential impact of lock out**.
	- No cached logon (offline sign-on)
	- Having computer and service accounts in this group is useless as their credentials will always be present on the host machine.

## Privileged Administrative Workstations (PAWs)
- A hardened workstation for performing sensitive tasks like administration of domain controllers,cloud infrastructure,sensitive business function etc..
- Can provides protection from phishing attacks, OS vulnerabilities, credential replay attacks.
- Admin Jump servers to be accessed only from a PAW, multiple strategies.
	- Separate privilege and hardware for administrative and normal tasks.
	- Having a VM on a PAW for user tasks.

## Active Directory Tier Model
- **Composed of three levels only for administrative accounts**:
	1. **Tier 0**: Accounts, Groups ad computers which have privileges across the enterprise like domain controllers, domain admins, enterprise admins.
	2. **Tier 1**: Accounts, Groups ad computers which have access to resources having significant amount of business value. A common example role is server administrators who maintain these operating systems with the ability to impact all enterprise services.
	3. **Tier 2**: Administrator accounts which have administrative control of a significant amount of business value that is hosted on user workstations and devices. Examples include Help Desk and computer support administrators because they can impact the integrity of almost any user data.
- Control Restrictions - What admins control.
- Logon Restrictions - Where admins can log-on to.
--- 
## Enhanced Security Admin Environment (ESAE)
- Dedicated administrative forest for managing critical assets like administrative users, groups ad computers.
- Since a forest is considered a security boundary rather than a domain, this model provides enhanced security controls.
- The administrative forest is called `Red Forest`.
- Administrative users in production forest are used as standard non-privileged users in the administrative forest.
- Selective authentication to the Red Forest enables stricter security controls on logon of users from non-administrative forests.