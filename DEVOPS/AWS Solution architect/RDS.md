# RDS - Relational Database Service
It allows to create databases in the cloud that are managed by AWS
- Postgres  
- MySQL  
- MariaDB  
- Oracle  
- Microsoft SQL Server  
- Aurora (AWS Proprietary database)

# Advantage over using RDS versus deploying DB on EC2
- **RDS is a Managed service**
	- Automated provisioning, OS patching  
		- Continuous backups and restore to specific timestamp (Point in Time Restore)!  
	- Monitoring dashboards  
	- Read replicas for improved read performance  
	- Multi AZ setup for DR (Disaster Recovery)
> **Note**: You can't ssh into them

# RDS Read Replicas - read scalability (important)
- Replicas can be promoted to their own db (The read replica becomes a DB)
- **Use cases**
	- You have a production database that is taking on normal load
	- You want to run a reporting application to run some analytics 
	- You create a Read Replica to run the new workload there  
	- The production application is unaffected  
	- Read replicas are used for `SELECT `(=read) only kind of statements (not INSERT, UPDATE, DELETE)
- **Cost**:
	- For free except cross-region
# RDS Multi AZ (Disaster recovery)
- **SYNC** replication
- Not used for scaling
- *Multi-Az replicartion is free*
> **Important Note**: (Common exam question)
> - Read replicas can be setup as Multi-AZ for disaster recovery (DR) = YES

## RDS -From single-AZ to Multi-AZ (Important)
- Zero downtime operation (no need to stop the DB)
- Just click `modify` for the DB
- **The following happens internally**:  
	- A snapshot is taken  
	- A new DB is restored from the snapshot in a new AZ  
	- Synchronization is established between the two databases
# RDS Encryption
- **At rest**:
	- Possibility to encrypt the master & read replicas with `AWS KMS - AES-256 `encryption  
	- Encryption has to be defined at launch time  
	- **If the master is not encrypted, the read replicas cannot be encrypted**  
	- Transparent Data Encryption (TDE) available for Oracle and SQL Server
- **In-flight**:
- SSL/TLS ecryption
- **To enforce SSL**:
- PostgreSQL 
- In the AWS RDS Console (Parameter Groups)
 ```sql 
rds.force_ssl=1
``` 
- MySQL: 
 Within the DB
```sql
GRANT USAGE ON *.* TO 'mysqluser'@'%' REQUIRE SSL;
```

> **Important Notes**:
> - Snapshots of un-encrypted RDS databases are un-encrypted  
>  - Snapshots of encrypted RDS databases are encrypted  
>  - Can copy a snapshot into an encrypted one

# RDS security
- **Network Security**  
	- RDS databases are usually deployed within a **private** subnet, not in a public one  
	- RDS security works by leveraging security groups (the same concept as for EC2 instances) – it controls which IP / security group can communicate with RDS
- **IAM Authentication**
	- Works with `MySQL` `and PostgresQL`
	- Use auth token obtained through IAM & RDS Api calls (*15 min lifetime*)
	- **Benefits**:
		- Network in/out must be SSL/TLS encrypted
# Elastic Cache - DB Cache
Caches are in-memory databases with really high performance, low  
latency  
- Helps reduce load off of databases for read intensive workloads  
- Helps make your application stateless  
- AWS takes care of OS maintenance / patching, optimizations, setup, configuration, monitoring, failure recovery and backups  
- Using ElastiCache involves heavy application code changes
## ElastiCache – Redis vs Memcached
![](https://i.imgur.com/mxu1kgm.png)
> **More**: [Memcached vs Redis](https://www.instaclustr.com/blog/redis-vs-memcached/)

## ElasticCache Security
- All caches in ElastiCache:  
	- Do not support IAM authentication  
	- IAM policies on ElastiCache are only used for AWS API-level security  
- **Redis AUTH**:  
	- You can set a “password/token” when you create a Redis cluster  
	- This is an extra level of security for your cache (on top of security groups)  
	- Support SSL in flight encryption  
- **Memcached**:  
	- Supports SASL-based authentication (advanced)