# Navigation
# Disaster recovery
**What kind of disaster recovery?**  
	- **On-premise => On-premise:** traditional DR, and very expensive  
	- **On-premise => AWS Cloud**: hybrid recovery  
	- **AWS Cloud Region A** => AWS Cloud Region B
- **Two terms needs to be deifned**:
	- **RPO**: Recovery Point Objective
	- **RTO**: Recovery Time Objective
# Strategies
- Backup and Restore
- Pilot Light
- Warm Standby
- Hot Site / Multi Site Approach
## Backup-and-Restore
![](https://i.imgur.com/Qs0DjsJ.png)

## Pilot-Light
- A small version of the app is always running in the cloud  
- Useful for the critical core (pilot light)  
- Very similar to Backup and Restore  
- **Faster than Backup and Restore as critical systems are already up**
 ![](https://i.imgur.com/GoelaTt.png)
 ## Warm-Standby
 - Full system is up and running, but at maximum size
 - Upon disaster, we can scale to production load
![](https://i.imgur.com/GR1oQTu.png)
## Multi-Site
- Also called `Hot Site Approach`
- **Very low RTO (minutes or seconds) – very expensive**  
- Full Production Scale is running AWS and On Premise
![](https://i.imgur.com/b16UOi0.png)

# All-AWS-Multi-Region
![](https://i.imgur.com/MgQqwxf.png)
# Disaster Recovery
- **Backup**  
	- EBS Snapshots, RDS automated backups / Snapshots, etc...  
	- Regular pushes to S3 / S3 IA / Glacier, Lifecycle Policy, Cross Region Replication  
	- From On-Premise: Snowball or Storage Gateway  
- **High Availability**  
	- Use Route53 to migrate DNS over from Region to Region  
	- RDS Multi-AZ, ElastiCache Multi-AZ, EFS, S3  
	- Site to Site VPN as a recovery from Direct Connect  
- **Replication**  
	- RDS Replication (Cross Region), AWS Aurora + Global Databases  
	- Database replication from on-premises to RDS  
	- Storage Gateway  
- **Automation**  
	- CloudFormation / Elastic Beanstalk to re-create a whole new environment  
	- Recover / Reboot EC2 instances with CloudWatch if alarms fail  
	- AWS Lambda functions for customized automations  
- **Chaos**  
	- Netflix has a “simian-army” randomly terminating EC2
# Database-Migration-Service
- Quickly and securely migrate databases to AWS, resilient, self healing  
- The source database remains available during the migration  
- **Supports**:  
	- Homogeneous migrations: ex Oracle to Oracle  
	- Heterogeneous migrations: ex Microsoft SQL Server to Aurora  
- Continuous Data Replication using CDC  
- You must create an EC2 instance to perform the replication tasks
## DMS-Sources-Targets
- **Sources**:
	- **On-Premise and EC2 instances databases**: 
		- Oracle
		- MS SQL Server
		- MariaDB
		- PostgreSQL
		- MongoDB
		- SAP
		- DB2  
	- **Azure**: 
		- Azure SQL Database  
	- **Amazon RDS**: 
		- All including Aurora  
	- **Amazon S3**
- **Targets**:
	- On-Premise and EC2 instances databases: Oracle, MS SQL Server, MySQL, MariaDB, PostgreSQL, SAP  
	- Amazon RDS  
	- Amazon Redshift  
	- Amazon DynamoDB  
	- Amazon S3  
	- ElasticSearch Service  
	- Kinesis Data Streams  
	- DocumentDB
## AWS-Schema-Convertion-Tool
- **SCT** = AWS Schema Convertion Tool
- Convert your Database’s Schema from one engine to another  
- **Example OLTP**: (SQL Server or Oracle) to MySQL, PostgreSQL, Aurora  
- **Example OLAP**: (Teradata or Oracle) to Amazon Redshift  
- Prefer compute-intensive instances to optimize data conversions
![](https://i.imgur.com/eI4eqip.png)
## Continuos-Replication
![](https://i.imgur.com/joJvi8V.png)
# On-Premise-Strategy-with-AWS
- **Ability to download Amazon Linux 2 AMI as a VM (.iso format)**  
	- VMWare, KVM, VirtualBox (Oracle VM), Microsoft Hyper-V  
- **VM Import / Export**  
	- Migrate existing applications into EC2  
	- Create a DR repository strategy for your on-premises VMs  
	- Can export back the VMs from EC2 to on-premises  
- **AWS Application Discovery Service**  
	- Gather information about your on-premises servers to plan a migration  
	- Server utilization and dependency mappings  
	- Track with AWS Migration Hub  
- **AWS Database Migration Service (DMS)**  
	- replicate On-premise => AWS , AWS => AWS, AWS => On-premise  
	- Works with various database technologies (Oracle, MySQL, DynamoDB, etc..)  
- **AWS Server Migration Service (SMS)**  
	- Incremental replication of on-premises live servers to AWS
# AWS-DataSync
- Move large amount of data from on-premises to AWS  
- **Can synchronize to**: 
	- Amazon S3 (any storage classes – including  Glacier),
	- Amazon EFS
	- Amazon FSx (Windows, Lustre...)  
- Move data from your NAS or file system via NFS or SMB  
- Replication tasks can be scheduled hourly, daily, weekly  
- Leverage the DataSync agent to connect to your systems  
- Can setup a bandwidth limit
![](https://i.imgur.com/gHcxsGf.png)
# AWS-Backup
- Fully managed service  
- Centrally manage and automate backups across AWS services  
- No need to create custom scripts and manual processes  
- **Supported services**:
	- Amazon EC2 / Amazon EBS  
	- Amazon S3  
	- Amazon RDS (all DBs engines) / Amazon Aurora / Amazon DynamoDB  
	- Amazon DocumentDB / Amazon Neptune  
	- Amazon EFS / Amazon FSx (Lustre & Windows File Server)  
	- AWS Storage Gateway (Volume Gateway)  
- **Supports cross-region backups**  
- **Supports cross-account backups**
- **Supports PITR for supported services**  
- On-Demand and Scheduled backups  
- Tag-based backup policies  
- **You create backup policies known as Backup Plans**  
	- Backup frequency (every 12 hours, daily, weekly, monthly, cron expression)  
	- Backup window  
	- Transition to Cold Storage (Never, Days, Weeks, Months, Years)  
	- Retention Period (Always, Days, Weeks, Months, Years)
![](https://i.imgur.com/SMUWZAP.png)

## Vault-Lock
- Enforce a WORM (Write Once Read Many) state for all the backups that you store in your AWS Backup Vault  
- Additional layer of defense to protect yourbackups against:  
	- Inadvertent or malicious delete operations  
	- Updates that shorten or alter retention periods  
- Even the root user cannot delete backups when enabled
# Transferring-large-amount-of-data-into-AWS  
- Example: transfer 200 TB of data in the cloud. We have a 100 Mbps internet connection.  
- **Over the internet / Site-to-Site VPN:**  
	- Immediate to setup  
	- Will take 200(TB)*1000(GB)*1000(MB)*8(Mb)/100 Mbps = 16,000,000s = 185d  
- **Over direct connect 1Gbps:**  
	- Long for the one-time setup (over a month)  
	- Will take 200(TB)*1000(GB)*8(Gb)/1 Gbps = 1,600,000s = 18.5d  
- **Over Snowball:**  
	- Will take 2 to 3 snowballs in parallel  
	- Takes about 1 week for the end-to-end transfer  
	- Can be combined with DMS  
- For on-going replication / transfers: Site-to-Site VPN or DX with DMS or DataSync
