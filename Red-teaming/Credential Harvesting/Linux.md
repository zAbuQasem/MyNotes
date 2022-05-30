# Linux
---
# Navigation
1. **[Procdump](#Procdump)**
2. **[Decrypting TLS traffic using TLS key logging Not working on latest firefox and chrome](#Decrypting%20TLS%20traffic%20using%20TLS%20key%20logging%20Not%20working%20on%20latest%20firefox%20and%20chrome)**
3. **[Peeking at shell command-line history files](#Peeking%20at%20shell%20command-line%20history%20files)**
4. **[Command line arguments](#Command%20line%20arguments)**
5. **[Spoofing a credential prompt via zenity on Linux](#Spoofing%20a%20credential%20prompt%20via%20zenity%20on%20Linux)**
---
#  Procdump
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

#  Decrypting TLS traffic using TLS key logging (Not working on latest firefox and chrome)
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

# Peeking at shell command-line history files
- History file location
```bash
/home/<USER>/.bashrc
# Vary depending on the shell type
# Ex: .zshrc
```
---
# Command line arguments
```bash
# "w" will expand the args
ps auxwww
```
---

# Spoofing a credential prompt via zenity on Linux
```bash
PWD=$(zenity --password --text "Ubuntu Update needs your password: " --title "Ubuntu System Update") 2>/dev/null 
```