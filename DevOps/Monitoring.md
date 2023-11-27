
# Ubuntu 22.04|20.04|18.04
### Grafana Setup
```bash
# Adding Repository 
sudo apt install -y gnupg2 curl software-properties-common
curl -fsSL https://packages.grafana.com/gpg.key|sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/grafana.gpg
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
# Installing grafana
sudo apt update
sudo apt -y install grafana
sudo systemctl enable --now grafana-server

# Check if every thing is good
sudo systemctl status grafana-server.service 

# Access Grafana on port 3000.
# Default logins are:
Username: admin
Password: admin
```
### Prometheus Setup
- Prerequisites
```bash
sudo groupadd --system prometheus
sudo useradd -s /sbin/nologin --system -g prometheus prometheus
#sudo mkdir /etc/prometheus
sudo mkdir /var/lib/prometheus
for i in rules rules.d files_sd; do sudo mkdir -p /etc/prometheus/${i}; done
```
Install Prometheus
```bash
sudo apt update
sudo apt -y install wget curl vim
mkdir -p /tmp/prometheus && cd /tmp/prometheus

# Download the latest binary file
curl -s https://api.github.com/repos/prometheus/prometheus/releases/latest | grep browser_download_url | grep linux-amd64 | cut -d '"' -f 4 | wget -qi 

# Extract the file
tar xvf prometheus*.tar.gz
cd prometheus*/
sudo mv prometheus promtool /usr/local/bin/

# Verify the installation
prometheus --version
promtool --version

# Moving Configuration files
sudo mv prometheus.yml /etc/prometheus/prometheus.yml
sudo mv consoles/ console_libraries/ /etc/prometheus/
cd $HOME
```
Create a Prometheus service file
```bash
sudo tee /etc/systemd/system/prometheus.service<<EOF
[Unit]
Description=Prometheus
Documentation=https://prometheus.io/docs/introduction/overview/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecReload=/bin/kill -HUP \$MAINPID
ExecStart=/usr/local/bin/prometheus \
  --config.file=/etc/prometheus/prometheus.yml \
  --storage.tsdb.path=/var/lib/prometheus \
  --web.console.templates=/etc/prometheus/consoles \
  --web.console.libraries=/etc/prometheus/console_libraries \
  --web.listen-address=0.0.0.0:9090 \
  --web.external-url=

SyslogIdentifier=prometheus
Restart=always

[Install]
WantedBy=multi-user.target
EOF
```
Change Directory Permissions
```bash
for i in rules rules.d files_sd; do sudo chown -R prometheus:prometheus /etc/prometheus/${i}; done
for i in rules rules.d files_sd; do sudo chmod -R 775 /etc/prometheus/${i}; done
sudo chown -R prometheus:prometheus /var/lib/prometheus/
```
Start the service
```bash
sudo systemctl daemon-reload
sudo systemctl start prometheus
sudo systemctl enable prometheus
systemctl status prometheus
```
### Exporters
- [Nginx Exporter](https://github.com/nginxinc/nginx-prometheus-exporter)
```
#In /etc/nginx/nginx.conf

server {
        listen 0.0.0.0:8080;
        location /stub_status {
                stub_status on;
        }
        }
```
### Alerting
For this one i will use [node-exporter](https://samber.github.io/awesome-prometheus-alerts/rules.html#host-and-hardware)
```sh
curl https://raw.githubusercontent.com/zAbuQasem/Misc/main/node-exporter-prom-alerts.yml -o alerts.yml
cp alerts.yml /etc/prometheus/
# Verify with promtool
promtool check rules alerts.yml
```
Finally load it with:
```yml
global:
  scrape_interval: 15s

rule_files:
  - alerts.yml

scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets: ['172.17.0.1:9100']
```

- [Node Exporter](https://devopscube.com/monitor-linux-servers-prometheus-node-exporter/)
- [BlackBox Exporter](https://devconnected.com/how-to-install-and-configure-blackbox-exporter-for-prometheus/) : Probing legend
