
# Scalability 
- Scalability means that an application / system can handle greater loads  by adapting.  
- There are two kinds of scalability:  
- **Vertical Scalability**  
	- Increasing the size of the instance  
	- Vertical scalability is very common for non distributed systems, such as a database.  
	- `RDS`, `ElastiCache` are services that can scale vertically.  
	- There’s usually a limit to how much you can vertically scale (hardware limit)
- **Horizontal Scalability (elasticity)**
	- Increasing the number of instances / systems for your application  
	- Horizontal scaling implies distributed systems.  
	- This is very common for web applications / modern applications

# High Availability  
- High Availability usually goes hand in hand with `horizontal scaling`
- High availability means running your application / system in at least 2 data centers (AZ)
- **Passive**:
	- Example: `RDS Multi AZ`
- **Active**:
	- Example: `Horizontal scaling`
# Load Balancer
Servers that forward traffic to multiple servers downstream
## Why use a load balancer?  
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
## Types of load balancer on AWS  
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
- **Gateway Load Balancer**  
	- Operates at layer 3 (Network layer) – IP Protocol  
- Overall, it is recommended to use the newer generation load balancers as they  provide more features  
- Some load balancers can be setup as `internal (private)` or `external (public) ELBs)`
![](https://i.imgur.com/Ienfe21.png)

