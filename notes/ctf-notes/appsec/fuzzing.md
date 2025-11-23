# Fuzzing

Fuzzing approach

## Directory Bruteforce

### Dirsearch Wordlist

```
# Nonrecursive (Preferred)
feroxbuster -u http://example.com -w /usr/share/seclists/Discovery/Web-Content/dirsearch.txt -n
```

## Virtual Hosts

* **Gobuster**

```
gobuster vhost -u http://www.example.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt --append-domain -t 50 -r
```

* **FFUF**

```
ffuf -H "Host: FUZZ.example.com" -c -w "/usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt" -u http://example.com -mc all
```

* **WFUZZ**

```
wfuzz -c -f subdomains.txt -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-110000.txt -u "http://example.com/" -H "Host: FUZZ.example.com"
```

## API Fuzzing

```
feroxbuster -u http://example.com/FUZZ -w /usr/share/seclists/Discovery/Web-Content/api/api-endpoints.txt -m GET,POST,PUT
```

* Useful wordlists

```
/usr/share/seclists/Discovery/Web-Content/raft-medium-directories.txt
/usr/share/seclists/Discovery/Web-Content/api/*
```

