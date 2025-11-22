# Ansible

Configuration management and automation with Ansible.

---

## Inventory

The simplest inventory is a single file with a list of hosts and groups. The default location for this file is `/etc/ansible/hosts`. You can specify a different inventory file at the command line using the `-i <path>` option or in configuration using `inventory`.

## INI
Suitable for small infrastructure.
### Basic
```
localhost ansible_connection=local

[webservers]
web1 ansible_host=192.168.1.10  ansible_user=myuser ansible_ssh_pass=mypassword

[dbservers]
db1 ansible_host=192.168.1.11 ansible_user=myuser ansible_ssh_pass=mypassword
db2 ansible_host=192.168.1.12 ansible_user=myuser ansible_ssh_pass=mypassword

## Range from 192.168.1.13 - 192.168.1.20
db3 ansible_host=192.168.1.[13:20] ansible_user=myuser ansible_ssh_pass=mypassword
```
### Parent-Child
```
[all_servers:children]
webservers
dbservers
```
## YAML
Suitable for big infrastructures.
### Basic
```yaml
ungrouped:
  hosts:
    mail.example.com
webservers:
  hosts:
    foo.example.com
    bar.example.com
dbservers:
  hosts:
    one.example.com
    two.example.com
    three.example.com
```
### Parent-Child
```yaml
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: 192.168.1.10
          ansible_user: myuser
          ansible_ssh_pass: mypassword
    dbservers:
      hosts:
        db1:
          ansible_host: 192.168.1.11
          ansible_user: myuser
          ansible_ssh_pass: mypassword
        db2:
          ansible_host: 192.168.1.12
          ansible_user: myuser
          ansible_ssh_pass: mypassword
```
### References
- https://docs.ansible.com/ansible/latest/inventory_guide/intro_inventory.html#inventory-basics-formats-hosts-and-groups
# 