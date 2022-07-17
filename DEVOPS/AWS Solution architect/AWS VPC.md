# Navigation
- [**VPC-Overview**](#VPC-Overview)
	- [IPV4](#IPV4)
- [**Subnet-IPV4**](#Subnet-IPV4)
- [**Internet-Gateway**](#Internet-Gateway)
- [**Bastion-Hosts**](#Bastion-Hosts)
- [**NAT-Instance**](#NAT-Instance)
	- [NAT-Gateway](#NAT-Gateway)
	- [NAT-Gateway-High-Availability](#NAT-Gateway-High-Availability)
- [**DNS-Resolution-VPC**](#DNS-Resolution-VPC)
# VPC-Overview
- VPC = Virtual Private Cloud
- All new AWS accounts have a default VPC  
- New EC2 instances are launched into the default VPC if no subnet is  specified  
	- **Default VPC:** `172.16.0.0 – 172.31.255.255 (172.16.0.0/12)`
- Default VPC has Internet connectivity and all EC2 instances inside it  have public IPv4 addresses  
- We also get a public and a private IPv4 DNS names
## IPV4
- You can have multiple VPCs in an AWS region (*max. 5 per region – soft limit*)
- **Max. CIDR per VPC is 5, for each CIDR:**  
	- Min. size is /28 (16 IP addresses)  
	- Max. size is /16 (65536 IP addresses)  
- Because VPC is private, only the Private IPv4 ranges are allowed:  
	- `10.0.0.0 – 10.255.255.255 (10.0.0.0/8)`
	- `172.16.0.0 – 172.31.255.255 (172.16.0.0/12)`
	- `192.168.0.0 – 192.168.255.255 (192.168.0.0/16)`
# Subnet-IPV4
- **AWS reserves 5 IP addresses (first 4 & last 1) in each subnet**  
- These 5 IP addresses are not available for use and can’t be assigned to an EC2 instance  
- **Example: if CIDR block 10.0.0.0/24, then reserved IP addresses are:**  
	- 10.0.0.0 – Network Address  
	- 10.0.0.1 – reserved by AWS for the VPC router  
	- 10.0.0.2 – reserved by AWS for mapping to Amazon-provided DNS  
	- 10.0.0.3 – reserved by AWS for future use  
	- 10.0.0.255 – Network Broadcast Address. **AWS does not support broadcast in a VPC**,  therefore the address is reserved  
> **Note**:
>  Exam Tip, if you need 29 IP addresses for EC2 instances:  
>  - You can’t choose a subnet of size /27 (32 IP addresses, 32 – 5 = 27 < 29)  
>  - You need to choose a subnet of size /26 (64 IP addresses, 64 – 5 = 59 > 29)
![](https://i.imgur.com/s8bN3LD.png)
# Internet-Gateway
- **IGW** = Internet Gateway 
- Allows resources (e.g., EC2 instances) in a VPC connect to the Internet  
- It scales horizontally and is highly available and redundant  
- Must be created separately from a VPC  
- **One VPC can only be attached to one IGW and vice versa**  
- **Internet Gateways on their own do not allow Internet access.**..  
- Route tables must also be edited!
![](https://i.imgur.com/yIKtmSR.png)
# Bastion-Hosts
- We can use a Bastion Host to SSH into our private EC2 instances  
- The bastion is in the public subnet which is then connected to all other private subnets
- Bastion Host security group must be tightened  
>**Note**: 
>- Exam Tip: Make sure the bastion host only has port 22 traffic from the IP address you need, not from the security groups of your other EC2 instances
![](https://i.imgur.com/FeKMPcS.png)
# NAT-Instance
- Allows EC2 instances in private subnets to connect to the Internet  
- Must be launched in a public subnet  
- **Must disable EC2 setting: Source / destination Check**
- **Must have Elastic IP attached to it**  
- Route Tables must be configured to route traffic from private subnets to the NAT Instance
![](https://i.imgur.com/K6hmkdX.png)
## NAT-Gateway
- AWS-managed NAT, higher bandwidth, high availability, no administration  
- Pay per hour for usage and bandwidth  
- NATGW is created in a specific Availability Zone, uses an Elastic IP  
- Can’t be used by EC2 instance in the same subnet (only from other subnets)  
- Requires an IGW (Private Subnet => NATGW => IGW)  
- 5 Gbps of bandwidth with automatic scaling up to 45 Gbps  
- **No Security Groups to manage / required**
![](https://i.imgur.com/9JDhJBL.png)
## NAT-Gateway-High-Availability
- NAT Gateway is resilient within a single Availability Zone  
- Must create multiple NAT Gateways in multiple AZs for fault-tolerance  
- There is no cross-AZ failover needed because if an AZ goes down it doesn't need NAT
![](https://i.imgur.com/YnkmEiE.png)
# DNS-Resolution-VPC 
- **DNS Resolution (enableDnsSupport)**  
	- Decides if DNS resolution from Route 53 Resolver server is supported for the VPC  
	- **True (default): it queries the Amazon Provider DNS Server at 169.254.169.253 or the reserved IP address at the base of the VPC IPv4 network range plus two (.2)**
![](https://i.imgur.com/7fnGKvW.png)
- DNS Hostnames (enableDnsHostnames)  
	- By default,  
		- `True => default VPC`
		- `False => newly created VPCs`  
	- Won’t do anything unless `enableDnsSupport=true`  
	- If True, assigns public hostname to EC2 instance if it has a public IPv4
![](https://i.imgur.com/gFxTWmP.png)
- **If you use custom DNS domain names in a Private Hosted Zone in Route 53, you must set both these attributes (enableDnsSupport & enableDnsHostname) to true**
![](https://i.imgur.com/q7sucng.png)

