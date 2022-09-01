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
- [**Security-Groups-And-NACLs**](#Security-Groups-And-NACLs)
	- [Default-NACL](#Default-NACL)
	- [Summary](#Summary)
- [**VPC-Reachability-Analyzer**](#VPC-Reachability-Analyzer)
- [**VPC-Peering**](#VPC-Peering)
- [**VPC-Endpoints-PrivateLink**](#VPC-Endpoints-PrivateLink)
	- [Types-Of-Endpoints](#Types-Of-Endpoints)
- [**VPC-FLow-Logs**](#VPC-FLow-Logs)
- [**AWS-Site-to-Site-VPN**](#AWS-Site-to-Site-VPN)
- [**AWS-VPN-CloudHub**](#AWS-VPN-CloudHub)
- [**Direct-Connect**](#Direct-Connect)
	- [Direct-Connect-Gateway](#Direct-Connect-Gateway)
		- [Direct-Connect-Encryption](#Direct-Connect-Encryption)
- [**Transit-Gateway**](#Transit-Gateway)
	- [Site-to-Site-VPN-ECMP](#Site-to-Site-VPN-ECMP)
	- [VPC-Traffic-Mirroring](#VPC-Traffic-Mirroring)
- [**Egress-Only-Internet-Gateway**](#Egress-Only-Internet-Gateway)
- [**VPC-Summary**](#VPC-Summary)
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

# Security-Groups-And-NACLs
- NACL are like a firewall which control traffic from and to subnets  
- One NACL per subnet, new subnets are assigned the Default NACL  
- **You define NACL Rules**:
	- Rules have a number (1-32766), higher precedence with a lower number
	- First rule match will drive the decision  
	- Example: if you define #100 ALLOW 10.0.0.10/32 and #200 DENY 10.0.0.10/32, the IP address will be allowed because 100 has a higher precedence over 200  
	- The last rule is an asterisk (\*) and denies a request in case of no rule match  
	- AWS recommends adding rules by increment of 100  
- Newly created NACLs will deny everything  
- NACL are a great way of blocking a specific IP address at the subnet level
![](https://i.imgur.com/qqDaQKi.png)
## Default-NACL
- Accepts everything inbound/outbound with the subnets it’s associated with  
> **Note**: Do NOT modify the Default NACL, instead create custom NACLs
![](https://i.imgur.com/Rrep2Gy.png)
## Summary
![](https://i.imgur.com/ZjQNeag.png)
# VPC-Reachability-Analyzer
- A network diagnostics tool that troubleshoots network connectivity between two endpoints in your VPC(s)  
- It builds a model of the network configuration, then checks the reachability based on these configurations (it doesn’t send packets)
- When the destination is reachable – it produces hop-by-hop details of the virtual network path.  
- Not reachable – it identifies the blocking component(s) (e.g., configuration issues in SGs, NACLs, Route Tables, ...)  
- **Use cases**: troubleshoot connectivity issues, ensure network configuration is as intended
# VPC-Peering
- Privately connect two VPCs using AWS network  
- Make them behave as if they were in the same network  
- Must not have overlapping CIDRs  
- VPC Peering connection is **NOT transitive** (must be established for each VPC that need to communicate with one another)  
- **You must update route tables in each VPC’s subnets to ensure EC2 instances can communicate with each other**
- Can Create a connection between between VPCs in **different AWS accounts/regions**
- You can reference a security group in a peered VPC (work accross accounts - same region)
# VPC-Endpoints-PrivateLink
- Every AWS service is publicly exposed (public URL)  
- **VPC Endpoints (powered by AWS PrivateLink) allows you to connect to AWS services using a private network instead of using the public Internet**
- They’re redundant and scale horizontally  
- They remove the need of IGW, NATGW .... to access AWS Services 
- **Most secure & scalable way to expose a service to 1000s of VPC (own or other accounts)**  
- Does not require VPC peering, internet gateway, NAT, route tables...  
- Requires a network load balancer (Service VPC) and ENI (Customer VPC) or GWLB  
- **If the NLB is in multiple AZ, and the ENIs in multiple AZ, the solution is fault tolerant!**
- **In case of issues**:  
	- Check DNS Setting Resolution in your VPC  
	- Check Route Tables
![](https://i.imgur.com/Y2w32Z6.png)
## Types-Of-Endpoints
- **Interface Endpoints**
	- Provisions an ENI (private IP address) as an entry point (must attach a Security Group)  
	- Supports most AWS services
- **Gateway Endpoints**
	-  Provisions a gateway and must be used as a target in a route table  
	- Supports both S3 and DynamoDB
![](https://i.imgur.com/GY5EunJ.png)
# VPC-FLow-Logs
- **Capture information about IP traffic going into your interfaces**:  
	- VPC Flow Logs  
	- Subnet Flow Logs  
	- Elastic Network Interface (ENI) Flow Logs  
- Helps to monitor & troubleshoot connectivity issues  
- Flow logs data can go to S3 / CloudWatch Logs  
- Captures network information from AWS managed interfaces too: ELB, RDS, ElastiCache, Redshift, WorkSpaces, NATGW, Transit Gateway...
# AWS-Site-to-Site-VPN
- **Virtual Private Gateway (VGW)**  
	- VPN concentrator on the AWS side of the VPN connection  
	- VGW is created and attached to the VPC from which you want to create the Site-to-Site VPN connection  
	- Possibility to customize the ASN (Autonomous System Number)  
- **Customer Gateway (CGW)**  
	- Software application or physical device on customer side of the VPN connection
- **Customer Gateway Device (On-premises)**  
	- **What IP address to use?**  
		- Public Internet-routable IP address for your Customer Gateway device  
		- If it’s behind a NAT device that’s enabled for NAT traversal (NAT-T), use the public IP address of the NAT device
	- **Important step: enable Route Propagation for the Virtual Private Gateway in the route table that is associated with your subnets**  
	- If you need to ping your EC2 instances from on-premises, make sure you add the ICMP protocol on the inbound of your security groups
# AWS-VPN-CloudHub  
- Provide secure communication between multiple sites, if you have multiple VPN connections  
- **Low-cost hub-and-spoke model for primary or secondary network connectivity between different locations (VPN only)**
- It’s a VPN connection so it goes over the public Internet
- To set it up, connect multiple VPN connections on the same VGW, setup dynamic routing and configure route tables
![](https://i.imgur.com/s5UaCrr.png)
# Direct-Connect
- DX = Direct Connect
- Provides a dedicated private connection from a remote network to your VPC  
- Dedicated connection must be setup between your DC and AWS Direct Connect locations  
- You need to setup a Virtual Private Gateway on your VPC  
- Access public resources (S3) and private (EC2) on same connection  
- **Use Cases**:  
	- Increase bandwidth throughput - working with large data sets – lower cost  
	- More consistent network experience - applications using real-time data feeds  
	- Hybrid Environments (on prem + cloud)
- Support both IPv4 and IPv6
![](https://i.imgur.com/hdqJB5A.png)
## Direct-Connect-Gateway
- If you want to setup a Direct Connect to one or more VPC in many different regions (same account), **you must use a Direct Connect Gateway**.
- **Connection Types**:
	- **Dedicated Connections**: 1Gbps and 10 Gbps capacity  
		- Physical ethernet port dedicated to a customer  
		- Request made to AWS first, then completed by AWS Direct Connect Partners  
	- **Hosted Connections**: 50Mbps, 500 Mbps, to 10 Gbps  
		- Connection requests are made via AWS Direct Connect Partners  
		- Capacity can be added or removed on demand  
		- 1, 2, 5, 10 Gbps available at select AWS Direct Connect Partners  
	- Lead times are often longer than 1 month to establish a new connection.
### Direct-Connect-Encryption
- Data in transit is not encrypted but is private.
- AWS Direct Connect + VPN provides an IPSEC-encrypted private connection.
- Good for an extra level of security, but slightly more complex to put in a place.
# Transit-Gateway
For having transitive peering between thousands of VPC and on-premises, hub-and-spoke (star) connection  
- Regional resource, can work cross-region  
- Share cross-account using Resource Access Manager (RAM)  
- You can peer Transit Gateways across regions  
- **Route Tables: limit which VPC can talk with other VPC**  
- Works with Direct Connect Gateway, VPN connections  
- Supports IP Multicast (not supported by any other AWS service)
## Site-to-Site-VPN-ECMP
- ECMP = Equal-cost multi-path routing  
- Routing strategy to allow to forward a packet over multiple best path
- **Use case**: create multiple Site-to-Site VPN connections to increase the bandwidth of your connection to AWS
![](https://i.imgur.com/L95aT8a.png)
## VPC-Traffic-Mirroring
- Allows you to capture and inspect network traffic in your VPC  
- Route the traffic to security appliances that you manage
- **Capture the traffic**
	- From (Source) – ENIs  
	- To (Targets) – an ENI or a Network Load Balancer  
- Capture all packets or capture the packets of your interest (optionally, truncate packets)  
- Source and Target can be in the same VPC or different VPCs (VPC Peering)
- **Use cases**: content inspection, threat monitoring, troubleshooting
# Egress-Only-Internet-Gateway
- **Used for IPv6 only**
- - Allows instances in your VPC outbound connections over IPv6 while preventing the internet to initiate an IPv6 connection to your instances  
- **You must update the Route Tables**
# VPC-Summary
- **CIDR** – IP Range  
- **VPC – Virtual Private Cloud** => we define a list of IPv4 & IPv6 CIDR  
- **Subnets** – tied to an AZ, we define a CIDR  
- **Internet Gateway** – at the VPC level, provide IPv4 & IPv6 Internet Access  
- **Route Tables** – must be edited to add routes from subnets to the IGW, VPC Peering Connections, VPC Endpoints, ...  
- **Bastion Host** – public EC2 instance to SSH into, that has SSH connectivity to EC2 instances in private subnets  
- **NAT Instances** – gives Internet access to EC2 instances in private subnets. Old, must be setup in a public subnet, disable Source / Destination check flag  
- **NAT Gateway** – managed by AWS, provides scalable Internet access to private EC2 instances, IPv4 only  
- **Private DNS + Route 53** – enable DNS Resolution + DNS **Hostnames (VPC NACL** – stateless, subnet rules for inbound and outbound, don’t forget Ephemeral Ports  
- **Security Groups** – stateful, operate at the EC2 instance level  
- **Reachability Analyzer** – perform network connectivity testing between AWS resources  
- **VPC Peering** – connect two VPCs with non overlapping CIDR, non-transitive  
- **VPC Endpoints** – provide private access to AWS Services (S3, DynamoDB, CloudFormation, SSM) within a VPC  
- **VPC Flow Logs** – can be setup at the VPC / Subnet / ENI Level, for ACCEPT and REJECT traffic, helps identifying attacks, analyze using Athena or CloudWatch Logs Insights  
- **Site-to-Site VPN** – setup a Customer Gateway on DC, a Virtual Private Gateway on VPC, and site-to-site VPN over public Internet  
- **AWS VPN CloudHub** – hub-and-spoke VPN model to connect your sites
- **Direct Connect** – setup a Virtual Private Gateway on VPC, and establish a direct private connection to an AWS Direct Connect Location  
- **Direct Connect Gateway** – setup a Direct Connect to many VPCs in different AWS regions  
- **AWS PrivateLink / VPC Endpoint Services:**  
	- Connect services privately from your service VPC to customers VPC  
	- Doesn’t need VPC Peering, public Internet, NAT Gateway, Route Tables  
	- Must be used with Network Load Balancer & ENI  
	- ClassicLink – connect EC2-Classic EC2 instances privately to your VPC  
- **Transit Gateway** – transitive peering connections for VPC, VPN & DX  
- **Traffic Mirroring** – copy network traffic from ENIs for further analysis  
- **Egress-only Internet Gateway** – like a NAT Gateway, but for IPv6