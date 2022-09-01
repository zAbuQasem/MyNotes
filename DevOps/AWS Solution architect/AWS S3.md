# Navigation
- [**Amazon-S3-Overview-Buckets**](#Amazon-S3-Overview-Buckets)
	- [S3-Encryption-for-Objects](#S3-Encryption-for-Objects)
- [**Advanced-Amazon-S3**](#Advanced-Amazon-S3)
	- [S3-MFA-Delete](#S3-MFA-Delete)
	- [S3-Access-log-Warning](#S3-Access-log-Warning)
	- [S3-Replication](#S3-Replication)
	- [S3-Replication–Notes](#S3-Replication–Notes)
	- [S3-Pre-Signed-URLs](#S3-Pre-Signed-URLs)
- [**S3-Storage-Classes**](#S3-Storage-Classes)
- [**S3-Lifecycle-Rules**](#S3-Lifecycle-Rules)
- [**S3-Performance**](#S3-Performance)
	- [S3-Performance–S3-Byte-Range-Fetches](#S3-Performance–S3-Byte-Range-Fetches)
- [**S3-Select-and-Glacier-Select**](#S3-Select-and-Glacier-Select)
- [**S3-Event-Notifications**](#S3-Event-Notifications)
	- [S3-Event-Notifications-with-Amazon-EventBridge](#S3-Event-Notifications-with-Amazon-EventBridge)
- [**S3–Requester-Pays**](#S3–Requester-Pays)
- [**Amazon-Athena**](#Amazon-Athena)
- [**S3-Object-Lock**](#S3-Object-Lock)
---
# Amazon-S3-Overview-Buckets  
- Amazon S3 allows people to store objects (files) in “buckets” (directories)  
- Buckets must have a globally unique name  
- Buckets are defined at the region level  
- Naming convention  
- No uppercase  
- No underscore  
- 3-63 characters long  
- Not an IP  
- Must start with lowercase letter or number
- Object values are the content of the body:  
- **Max Object Size is 5TB (5000GB)**  
- If uploading more than 5GB, must use "multi-part upload"


## S3-Encryption-for-Objects  
- **There are 4 methods of encrypting objects in S3**  
	- **SSE-S3**: encrypts S3 objects using keys handled & managed by AWS  
		- Object is encrypted server side  
		- AES-256 encryption type  
		- Must set header: “x-amz-server-side-encryption": "AES256
	- **SSE-KMS**: leverage AWS Key Management Service to manage encryption keys  
		- KMS Advantages: user control + audit trail  
		- Object is encrypted server side  
		-  Must set header: “x-amz-server-side-encryption": ”aws:kms"
	- **SSE-C**: when you want to manage your own encryption keys
		- Amazon S3 does not store the encryption key you provide  
		- HTTPS must be used  
		- Encryption key must provided in HTTP headers, for every HTTP request made  
	- **Client Side Encryption**
		- Client library such as the Amazon S3 Encryption Client  
	- Clients must encrypt data themselves before sending to S3  
	- Clients must decrypt data themselves when retrieving from S3  
	- Customer fully manages the keys and encryption cycle
# Advanced-Amazon-S3
## S3-MFA-Delete
- You will need MFA to
	- Permanently delete an object version
	- Suspend versioning on the bucket
- You won’t need MFA for:
	- Enabling versioning
	- Listing deleted versions
- **Only the bucket owner (root account) can enable/disable MFA-Delete**
- MFA-Delete currently can only be enabled using the CLI
## S3-Access-log-Warning
- Don't set your logging bucket to be the monitored bucket as it will create a logging loopback, and the bucket will grow exponentially.
## S3-Replication
- Must enable versioning in source and destination  
- Cross Region Replication (**CRR**)  
- Same Region Replication (**SRR**)  
- Buckets can be in different accounts  
- Copying is asynchronous  
- Must give proper IAM permissions to S3  
- **CRR - Use cases**: compliance, lower latency access, replication across accounts  
- **SRR – Use cases**: log aggregation, live replication between production and test accounts
  
## S3-Replication–Notes  
- After activating, only new objects are replicated  
- Optionally, you can replicate existing objects using **S3 Batch Replication**  
	- Replicates existing objects and objects that failed replication  
- **For DELETE operations**:  
	- Can replicate delete markers from source to target (optional setting)  
	- Deletions with a version ID are not replicated (to avoid malicious deletes)  
- **There is no "chaining" of replication**  
	- If bucket 1 has replication into bucket 2, which has replication into bucket 3  
	- Then objects created in bucket 1 are not replicated to bucket 3
## S3-Pre-Signed-URLs  
- Can generate pre-signed URLs using SDK or CLI  
- For downloads (easy, **can use the CLI**)  
- For uploads (harder, **must use the SDK**)  
- Valid for a default of **3600** seconds, can change timeout with --expires-in [TIME_BY_SECONDS] argument  
- Users given a pre-signed URL **inherit the permissions** of the person who generated the URL for GET / PUT  
- **Examples** :  
	- Allow only logged-in users to download a premium video on your S3 bucket  
	- Allow an ever changing list of users to download files by generating URLs dynamically  
	- Allow temporarily a user to upload a file to a precise location in our bucket

# S3-Storage-Classes
- **Amazon S3 Standard - General Purpose**
	-  Used for frequently accessed data  
	-  Low latency and high throughput  
	-  Sustain 2 concurrent facility failures  
- **Amazon S3 Standard-Infrequent Access (IA)**  
	- For data that is less frequently accessed, but requires rapid access when needed  
	- Lower cost than S3 Standard
	- 99.9% Availability  
	- Use cases: Disaster Recovery, backups
- **Amazon S3 One Zone-Infrequent Access**
	- High durability (99.999999999%) in a single AZ; data lost when AZ is destroyed  
	- 99.5% Availability  
	- Use Cases: Storing secondary backup copies of on premises data, or data you can recreate  
- **Amazon S3 Glacier Instant Retrieval**  
	- Millisecond retrieval, great for data accessed once a quarter  
	- Minimum storage duration of 90 days
- **Amazon S3 Glacier Flexible Retrieval**  
	- Expedited (1 to 5 minutes), Standard (3 to 5 hours), Bulk (5 to 12 hours) – free  
	- Minimum storage duration of 90 days
- **Amazon S3 Glacier Deep Archive** - (long term storage)
	- Standard (12 hours), Bulk (48 hours)  
	- Minimum storage duration of 180 days
- **Amazon S3 Intelligent Tiering** 
	- Small monthly monitoring and auto-tiering fee  
	- Moves objects automatically between AccessTiers based on usage  
	- There are no retrieval charges in S3 Intelligent-Tiering

> **Note**: Can move between classes manually or using S3 Lifecycle configurations

# S3-Lifecycle-Rules
- **Transition actions**: It defines when objects are transitioned to another storage class.  
	- Move objects to Standard IA class 60 days after creation  
	- Move to Glacier for archiving after 6 months  
- **Expiration actions**: configure objects to expire (delete) after some time  
	- Access log files can be set to delete after a 365 days  
	- **Can be used to delete old versions of files** (if versioning is enabled)  
	- Can be used to delete incomplete multi-part uploads
- Rules can be created for a certain prefix (ex - s3://mybucket/mp3/\*)  
- Rules can be created for certain objects tags (ex - Department: Finance)
# S3-Performance
- **Multi-Part upload**:  
	- Recommended for files > `100MB`
	- Must use for files > `5GB`  
	- Can help parallelize uploads (speed up transfers)  
	![Multipart](https://i.imgur.com/fZFsZpS.png)

- **S3 Transfer Acceleration**  
	- Increase transfer speed by transferring file to an AWS edge location which will forward the data to the S3 bucket in the target region  
	- Compatible with multi-part upload
![TransferAcceleration](https://i.imgur.com/q9DKtBb.png)

## S3-Performance–S3-Byte-Range-Fetches
- Parallelize GETs by requesting specific byte ranges  
- Better resilience in case of failures
- Can be used to retrieve only partial data (for example the head of a file)
- Can be used to speed up downloads
# S3-Select-and-Glacier-Select
- Retrieve less data using SQL by performing server side filtering  
- Can filter by rows & columns (simple SQL statements)  
- Less network transfer, less CPU cost client-side
![Glacierselect](https://i.imgur.com/bo96AQI.png)

# S3-Event-Notifications
- S3:ObjectCreated, S3:ObjectRemoved, S3:ObjectRestore, S3:Replication....etc
- Object name filtering possible (\*.jpg)
- Use case: generate thumbnails of images uploaded to S3  
- Can create as many “S3 events” as desired
## S3-Event-Notifications-with-Amazon-EventBridge
- **Advanced filtering** options with JSON rules (metadata, object size, name...)  
- **Multiple Destinations** – ex Step Functions, Kinesis Streams / Firehose...  
- **EventBridge Capabilities** – Archive, Replay Events, Reliable delivery
![](https://i.imgur.com/nTbRYyB.png)

# S3–Requester-Pays
Helpful when you want to share large datasets with other accounts.
![](https://i.imgur.com/seu8uwU.png)
> **Important note**: The requester must be authenticated in AWS (cannot be anonymous)

# Amazon-Athena
Serverless query service to perform analytics against S3 objects  
- Uses standard SQL language to query the files  
- Supports` CSV`,`JSON`,`ORC`, `Avro`, and `Parquet` (built on Presto)  
- Pricing: `$5.00` per TB of data scanned  
- Use compressed or columnar data for cost-savings (less scan)  
- **Use cases**: 
	- Business intelligence
	- Analytics
	- Reporting
	- Analyze & query VPC Flow Logs
	- ELB Logs
	- CloudTrail trails
	- etc...  
> **Exam Tip**: Analyze data in S3 using serverless SQL, use  -> Athena

![](https://i.imgur.com/oWyAlPD.png)

# Glacier-Vault-Lock
Adopt a WORM (Write Once Read Many) model  
- Lock the policy for future edits (can no longer be changed)  
- Helpful for compliance and data retention
# S3-Object-Lock
Adopt a WORM (Write Once Read Many) model  
- Block an object version deletion for a specified amount of time  
- **Object retention**:  
	- **Retention Period**: specifies a fixed period  
	- **Legal Hold**: same protection, no expiry date  
- **Modes**:  
	- **Governance mode**: users can't overwrite or delete an object version or alter its lock settings unless they have special permissions  
	- **Compliance mode**: a protected object version can't be overwritten or deleted by any user, including the root user in your AWS account. When an object is locked in compliance mode, its retention mode can't be changed, and its retention period can't be shortened