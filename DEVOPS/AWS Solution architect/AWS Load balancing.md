# Navigation
- [**Scalability**](#Scalability)
- [**High-Availability**](#High-Availability)
- [**Load-Balancer**](#Load-Balancer)
	- [Why-use-a-load-balancer](#Why-use-a-load-balancer)
	- [Types-of-load-balancer](#Types-of-load-balancer)
- [**Sticky-Sessions**](#Sticky-Sessions)
	- [Cookie-Names](#Cookie-Names)
- [**Cross-Zone-load-balancing**](#Cross-Zone-load-balancing)
- [**Load-balancer-SSL-Certs**](#Load-balancer-SSL-Certs)
- [**SNI-Server-Name-Indication**](#SNI-Server-Name-Indication)
- [**Auto-Scaling-Group**](#Auto-Scaling-Group)
- [**ASG-with-load-balancer**](#ASG-with-load-balancer)
# Scalability 
- Scalability means that an application / system can handle greater loads  by adapting.  
- **There are two kinds of scalability**:
	- **Vertical Scalability**  
		- Increasing the size of the instance  
		- Vertical scalability is very common for non distributed systems, such as a database.  
		- `RDS`, `ElastiCache` are services that can scale vertically.  
		- There’s usually a limit to how much you can vertically scale (hardware limit)
	- **Horizontal Scalability (elasticity)**
		- Increasing the number of instances / systems for your application  
		- Horizontal scaling implies distributed systems.  
		- This is very common for web applications / modern applications

# High-Availability  
- High Availability usually goes hand in hand with `horizontal scaling`
- High availability means running your application / system in at least 2 data centers (AZ)
- **Passive**:
	- Example: `RDS Multi AZ`
- **Active**:
	- Example: `Horizontal scaling`
# Load-Balancer
Servers that forward traffic to multiple servers downstream
## Why-use-a-load-balancer?  
- Spread load across multiple downstream instances  
- Expose a single point of access (DNS) to your application  
- Seamlessly handle failures of downstream instances  
- Do regular health checks to your instances  
- Provide SSL termination (HTTPS) for your websites  
- Enforce stickiness with cookies  
- High availability across zones  
- Separate public traffic from private traffic.
- It is integrated with many AWS offerings / services  
	- EC2, EC2 Auto Scaling Groups, Amazon ECS  
	- AWS Certificate Manager (ACM), CloudWatch  
	- Route 53, AWS WAF, AWS Global Accelerator
> **Note**: 
> It costs less to setup your own load balancer but it will be a lot more effort on your end.
## Types-of-load-balancer  
- AWS has 4 kinds of managed Load Balancers  
- **Classic Load Balancer (v1 - old generation)**  
	- HTTP, HTTPS, TCP, SSL (secure TCP)  
- **Application Load Balancer (v2 - new generation)**  
	- HTTP, HTTPS, WebSocket 
	- Routing tables to different target groups:  
	- Routing based on path in URL (`example.com/users` & `example.com/posts`)  
	- Routing based on hostname in URL (`one.example.com` & `other.example.com`)  
	- Routing based on Query String, Headers (`example.com/users?id=123&order=false`)
	- ![](https://i.imgur.com/KHZS02L.png)
	- **Target Groups**
		- EC2 instances (can be managed by an Auto Scaling Group) – HTTP  
		- ECS tasks (managed by ECS itself) – HTTP  
		- IP Addresses – must be **private IPs**  
		- ALB can route to multiple target groups  
		- Health checks are at the target group level
	- Fixed hostname (`XXX.region.elb.amazonaws.com`)  
	- The application servers **don’t** see the IP of the client directly  
	- The true IP of the client is inserted in the header `X-Forwarded-For` 
	- We can also get Port (`X-Forwarded-Port`) and proto (`X-Forwarded-Proto`)
- **Network Load Balancer (v2 - new generation)**
	 - TCP, TLS (secure TCP), UDP 
	 - Has one static IP per AZ, and supports assigning Elastic IP (helpful for whitelisting specific IP)
	 - NLB are used for extreme performance, TCP or UDP traffic
	 - **Target groups**:
		 - EC2 instances  
		- IP Addresses – must be private IPs  
		- Application Load Balancer
- **Gateway Load Balancer**  
	- Operates at layer 3 (Network layer) – IP Protocol Deploy,  scale, and manage a fleet of 3 rd party network virtual appliances in AWS  
	- **Example**: 
		- Firewalls
		- Intrusion Detection and Prevention Systems
		- Deep Packet Inspection 
		- Systems, payload manipulation ...  
	- **Combines the following functions**:  
		- Transparent Network Gateway – single entry/exit for all traffic  
		- Load Balancer – distributes traffic to your virtual appliances  
		- Uses the **GENEVE** protocol on port **6081**
- Overall, it is recommended to use the newer generation load balancers as they  provide more features  
- Some load balancers can be setup as `internal (private)` or `external (public) ELBs)`
![](https://i.imgur.com/Ienfe21.png)

# Sticky-Sessions  
- It is possible to implement stickiness so that the same client is always redirected to the same instance behind a load balancer  
- This works for Classic Load Balancers & Application Load Balancers
- The "cookie" used for stickiness has an expiration date you control  
- **Use case**: 
	- Make sure the user doesn’t lose his session data  
>**Note**: Enabling stickiness may bring imbalance to the load over the backend EC2 instances

## Cookie-Names  
- Application-based Cookies  
- **Custom cookie**  
	- Generated by the target  
	- Can include any custom attributes required by the application  
	- Cookie name must be specified individually for each target group  
	- Don’t use `AWSALB`, `AWSALBAPP`, or `AWSALBTG` (**reserved for use by the ELB**)  
- **Application cookie**  
	- Generated by the load balancer  
	- Cookie name is `AWSALBAPP`  
- **Duration-based Cookies**  
	- Cookie generated by the load balancer  
	- **Cookie name is**:
		- **ALB** -> `AWSALB`
		- **CLB** ->  `AWSELB`

# Cross-Zone-load-balancing
- **Application Load Balancer**  
	- Always on (can’t be disabled)  
	- No charges for inter AZ data  
- **Network Load Balancer**  
	- Disabled by default  
	- You pay charges ($) for inter AZ data if enabled  
- **Classic Load Balancer**  
	- Disabled by default  
	- No charges for inter AZ data if enabled
# Load-balancer-SSL-Certs
The load balancer uses an `X.509 certificate` (SSL/TLS server certificate)
- You can manage certificates using **ACM** (**AWS Certificate Manager**)  
- You can create upload your own certificates alternatively  
- **HTTPS listener**:  
	- You must specify a default certificate  
	- You can add an optional list of certs to support multiple domains  
	- Clients can use **SNI** (**Server Name Indication**) to specify the hostname they reach  
	- Ability to specify a security policy to support older versions of SSL / TLS (legacy clients)
- **Classic Load Balancer (v1)**  
	- Support only one SSL certificate  
	- Must use multiple CLB for multiple hostname with multiple SSL certificates  
- **Application Load Balancer (v2)**  
	- Supports multiple listeners with multiple SSL certificates  
	- Uses Server Name Indication (SNI) to make it work  
- **Network Load Balancer (v2)**  
	- Supports multiple listeners with multiple SSL certificates  
	- Uses Server Name Indication (SNI) to make it work
# SNI-Server-Name-Indication
**SNI** solves the problem of loading multiple SSL certificates onto one web server (to serve multiple websites)  
- It’s a “newer” protocol, and requires the client to indicate the hostname of the target server in the initial SSL handshake  
- The server will then find the correct certificate, or return the default one
> **Notes**:
> -  Only works with `ALB`, `NLB` and `Cloudfront`
> - Default option for `ALB` with no charges
> - You can use it with `NLB`, but with charges

# Auto-Scaling-Group
- Add (scale out ), Remove (scale in), Increase, Decrease the numer of instances for a load balancer.
- ![](https://i.imgur.com/CBXgGyJ.png)
## ASG-with-load-balancer
- It is possible to scale an ASG based on CloudWatch alarms  
- An Alarm monitors a metric (such as Average CPU)
- Scaling policies can be on CPU, Network... and can even be on custom metrics or based on a schedule (if you know your visitors patterns)
- To update an ASG, you must provide a new launch configuration / launch template  
- IAM roles attached to an ASG will get assigned to EC2 instances  
- **ASG are free**. You pay for the underlying resources being launched  
- Having instances under an ASG means that if they get terminated for whatever reason, the ASG will automatically create new ones as a replacement. Extra safety!  
- ASG can terminate instances marked as unhealthy by an LB (and hence replace them)
- After a scaling activity happens, you are in the cooldown period (default 300 seconds) 
- During the cooldown period, the ASG will not launch or terminate additional instances (to allow for metrics to stabilize)  
- **Advice**: 
	- Use a ready-to-use AMI to reduce configuration time in order to be serving request fasters and reduce the cooldown period
>  **Note**: Metrics are computed for the overall ASG instances
##  Good-metrics-to-scale-on  
- **CPU Utilization**: Average CPU utilization across your instances  
- **RequestCountPerTarget**: to make sure the number of requests per EC2 instances is stable  
- **Average Network In / Out** (if you’re application is network bound)  
- **Any custom metric** (that you push using CloudWatch)