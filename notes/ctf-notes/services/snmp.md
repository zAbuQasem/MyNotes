# SNMP

## Enumeration

look for leaked creds, emails ..etc

```
snmpbulkwalk -c internal -v2c <IP> | tee -a snmp-strings | grep -i string
snmpbulkwalk -c public -v2c <IP> | tee -a snmp-strings | grep -i string
```

## Privesc

Look for creds in conf files

```
grep -EHi "create|user|pass|cred" /etc/snmp/*
```

