# Navigation
- [**Amazon-FSX**](#Amazon-FSX)
- [**AWS-Storage-Gateway**](#AWS-Storage-Gateway)
	- [File-gateway](#File-gateway)
	- [Volume-gateway](#Volume-gateway)
	- [Tape-gateway](#Tape-gateway)
- [**AWS-Storage-Gateway-Summary**](#AWS-Storage-Gateway-Summary)
# AWS Snow Family
Offline devices to perform data migrations  
- **Data Migration**:
	- Snowcone
	- Snowball Edge
	- Snowmobile
- **Edge computing**:
	- Snowcone
	- Snowball Edge
> If it takes more than a week to transfer over the network, use Snowball devices!
# Amazon-FSX 
- **FSx for Lustre** -> important
	- Machine Learning, High Performance Computing (HPC)  
	- Video Processing, Financial Modeling, Electronic Design Automation  
	- Scales up to 100s GB/s, millions of IOPS, sub-ms latencies
	- Seamless integration with S3  
	- Can “read S3” as a file system (through FSx)  
	- Can write the output of the computations back to S3 (through FSx)  
- Can be used from on-premises servers (VPN or Direct Connect)
- **FSx for windows file server** -> important
	- A fully managed Windows file system share drive  
	- Supports SMB protocol & Windows NTFS  
	- Microsoft Active Directory integration, ACLs, user quotas  
	- Can be mounted on Linux EC2 instances
	- Can be accessed from your on-premises infrastructure (VPN or Direct Connect)  
	- Can be configured to be Multi-AZ (high availability)  
	- Data is backed-up daily to S
- **FSx for NetApp ONTAP**
# AWS-Storage-Gateway
- Bridge between on-premises data and cloud data in S3  
- **Use cases**: disaster recovery, backup & restore, tiered storage  
- **3 types of Storage Gateway**:  -> important
	- File Gateway 
	- Volume Gateway  
	- Tape Gateway
## File-gateway
- Configured S3 buckets are accessible using the NFS and SMB protocol  
- Supports S3 standard, S3 IA, S3 One Zone IA  
- Bucket access using IAM roles for each File Gateway  
- Most recently used data is cached in the file gateway  
- Can be mounted on many servers  
- Integrated with Active Directory (AD) for user authentication
![](https://i.imgur.com/xQTrImQ.png)
## Volume-gateway
- Block storage using iSCSI protocol backed by S3  
- Backed by EBS snapshots which can help restore on-premises volumes!  
- **Cached volumes**: low latency access to most recent data  
- **Stored volumes**: entire dataset is on premise, scheduled backups to S3
![](https://i.imgur.com/8J6iVUk.png)
## Tape-gateway
- Some companies have backup processes using physical tapes (!)  
- With Tape Gateway, companies use the same processes but, in the cloud  
- Virtual Tape Library (VTL) backed by Amazon S3 and Glacier  
- Back up data using existing tape-based processes (and iSCSI interface)  
- Works with leading backup software vendors
![](https://i.imgur.com/3wLg3zQ.png)
# AWS-Storage-Gateway-Summary  
- On-premises data to the cloud => Storage Gateway  
- File access / NFS – user auth with Active Directory => File Gateway (backed by S3)  
- Volumes / Block Storage / iSCSI => Volume gateway (backed by S3 with EBS snapshots)  
- VTL Tape solution / Backup with iSCSI = > Tape Gateway (backed by S3 and Glacier)  
- No on-premises virtualization => Hardware Appliance
# Amazon-FSx-File-Gateway  
- Native access to Amazon FSx for Windows File Server  
- Local cache for frequently accessed data  
- Windows native compatibility (SMB, NTFS, Active Directory...)  
- Useful for group file shares and home directories
![](https://i.imgur.com/YnWRIJV.png)

# AWS-Transfer-Family  
- A fully-managed service for file transfers into and out of Amazon S3 or  Amazon EFS using the FTP protocol  
- **Supported Protocols** :
	- AWS Transfer for FTP (File Transfer Protocol)  
	- AWS Transfer for FTPS (File Transfer Protocol over SSL) 
	- AWS Transfer for SFTP (Secure File Transfer Protocol)
# Storage-Comparison  
- **S3**: Object Storage  
- **Glacier**: Object Archival  
- **EFS**: Network File System for Linux instances, POSIX filesystem  
- **FSx for Windows**: Network File System for Windows servers  
- **FSx for Lustre**: High Performance Computing Linux file system  
- **EBS volumes**: Network storage for one EC2 instance at a time  
- **Instance Storage**: Physical storage for your EC2 instance (high IOPS)  
- **Storage Gateway**: File Gateway, Volume Gateway (cache & stored), Tape Gateway  
- **Snowball / Snowmobile**: to move large amount of data to the cloud, physically  
- **Database**: for specific workloads, usually with indexing and querying
