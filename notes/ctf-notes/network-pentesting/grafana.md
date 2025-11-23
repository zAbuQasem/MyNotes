# Grafana

Notes when attacking grafana

## CVE-2021-43798

Affects versions => `Grafana 8.0.0-beta1 to 8.3.0`

Recommended Exploit POC => <https://github.com/pedrohavay/exploit-grafana-CVE-2021-43798>

### Interesting files to read

```
/conf/defaults.ini
/conf/grafana.ini
/etc/grafana/grafana.ini
/home/grafana/.bash_history
/home/grafana/.ssh/id_rsa
/usr/local/etc/grafana/grafana.ini
/var/lib/grafana/grafana.db
```

Search for clear text passwords of data sources in `grafana.db` file.

