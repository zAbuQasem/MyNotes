# Amazon EC2  
- EC2 = Elastic Compute Cloud = Infrastructure as a Service  
- **It mainly consists in the capability of** :  
	- Renting virtual machines (EC2)  
	- Storing data on virtual drives (EBS)  
	- Distributing load across machines (ELB)  
	- Scaling the services using an auto-scaling group (ASG)

## Security Groups  
- Can be attached to multiple instances  
- Locked down to a region / VPC combination  
- Does live “outside” the EC2 – if traffic is blocked the EC2 instance won’t see it  
- It’s good to maintain one separate security group for SSH access  
- If your application is not accessible (time out), then it’s a security group issue  
- If your application gives a “connection refused“ error, then it’s an application  
error or it’s not launched  
- All inbound traffic is blocked by default  
- All outbound traffic is authorised by default

## EC2 Instances Purchasing Options  
- **On-Demand Instances** – short workload, predictable pricing, pay by second  (**Costy**)
- **Reserved (1 & 3 years)**
	- Up to 72% discount
	- Reserved Instances – long workloads  
	- Convertible Reserved Instances – long workloads with flexible instances  
	- Recommended for steady-state usage applications (think database)
- **Savings Plans (1 & 3 years)** –commitment to an amount of usage, long workload  
- **Spot Instances** – short workloads, cheap, can lose instances (less reliable) 
	- Can get a discount of up to 90% compared to On-demand  
	- Instances that you can “lose” at any point of time if your max price is less than the  
	current spot price  
	- The MOST cost-efficient instances in AWS
	- Useful for workloads that are resilient to failure  
		- Batch jobs  
		- Data analysis  
		- Image processing  
		- Any distributed workloads  
		- Workloads with a flexible start and end time
- **Dedicated Hosts** – book an entire physical server, control instance placement  (Highly expensive)
- **Dedicated Instances** – no other customers will share your hardware 
	- Instances run on hardware that’s  dedicated to you  
	- May share hardware with other  instances in same account  
	- No control over instance placement  (can move hardware after Stop / Start)
- **Capacity Reservations** – reserve capacity in a specific AZ for any duration
	- You always have access to EC2 capacity when you need it  
	- No time commitment (create/cancel anytime), no billing discounts  
	- Combine with Regional Reserved Instances and Savings Plans to benefit  
	from billing discounts  
	- You’re charged at On-Demand rate whether you run instances or not  
	- Suitable for short-term, uninterrupted workloads that needs to be in a  
	specific AZ


## Elastic IPs  
- When you stop and then start an EC2 instance, it can change its public IP.  
- If you need to have a fixed public IP for your instance, you need an Elastic IP  
- An Elastic IP is a public IPv4 IP you own as long as you don’t delete it  
- You can attach it to one instance at a time
- You can only have 5 Elastic IP in your account (you can ask AWS to increase  
that).  
- **Overall, try to avoid using Elastic IP**:  
	- They often reflect poor architectural decisions  
	- Instead, use a random public IP and register a DNS name to it  
	- Or, as we’ll see later, use a Load Balancer and don’t use a public IP

## Placement Groups
### Cluster
- Same AZ same rack
- **Pros**: 
	- Great network (10 Gbps bandwidth between instances with Enhanced Networking enabled - recommended)  
- **Cons**: 
	- If the rack fails, all instances fails at the same time  
- **Use case**:  
	- Big Data job that needs to complete fast  
	- Application that needs extremely low latency and high network throughput
	
### Spread
- **Pros**:  
	- Can span across Availability Zones (AZ)  
	- Reduced risk is simultaneous failure  
	- EC2 Instances are on different physical hardware  
- **Cons**:  
	- Limited to 7 instances per AZ  per placement group  
- **Use case**:  
	- Application that needs to maximize high availability  
	- Critical Applications where each instance must be isolated from failure from each other

### Partition
- **Pros**:
	- Up to 7 partitions per AZ  
	- Can span across multiple AZs in the  same region  
	- Up to 100s of EC2 instances  
	- The instances in a partition do not share racks with the instances in the  other partitions  
	- A partition failure can affect many EC2 but won’t affect other partitions  
- **Cons**:
	- EC2 instances get access to the partition information as metadata  
- **Use cases**:
	- HDFS, HBase, Cassandra, Kafka

## EC2 – Understanding vCPU  
- Multiple threads can run on one CPU (multithreading)  
- Each thread is represented as a virtual CPU (vCPU)
- **Example**: `m5.2xlarge`  
	- 4 CPU  
	- 2 threads per CPU  
	- => 8 vCPU in total

## EC2 – Capacity Reservations  
- Capacity Reservations ensure you have EC2 Capacity when needed  
- Manual or planned end-date for the reservation  
- No need for 1 or 3-year commitment  
- Capacity access is immediate, you get billed as soon as it starts  
- **Specify**:  
	- The Availability Zone in which to reserve the capacity (only one)  
	- The number of instances for which to reserve capacity  
	- The instance attributes, including the instance type, tenancy, and platform/OS  
- Combine with Reserved Instances and Savings Plans to do cost saving