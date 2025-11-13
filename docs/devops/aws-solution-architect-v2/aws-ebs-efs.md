# Navigation
- [**EBS-Volume**](#EBS-Volume)
- [**EBS-Volume-Types**](#EBS-Volume-Types)
- [**EBS-behaviour-when-an-EC2-instance-terminates**](#EBS-behaviour-when-an-EC2-instance-terminates)
- [**Encrypt-unencrypted-EBS-volume**](#Encrypt-unencrypted-EBS-volume)
- [**EFS**](#EFS)
- [**EFS-vs-EBS**](#EFS-vs-EBS)
# EBS-Volume  
- Elastic Block Store
- It’s a network drive (i.e. not a physical drive)  
	- It uses the network to communicate the instance, which means there might be a bit of  latency  
	- It can be detached from an EC2 instance and attached to another one quickly  
- It’s locked to an Availability Zone (AZ)  
	- An EBS Volume in us-east-1a cannot be attached to us-east-1b  
	- To move a volume across, you first need to snapshot it  
- Have a provisioned capacity (size in GBs, and IOPS)  
	- You get billed for all the provisioned capacity  
	- You can increase the capacity of the drive over time

# EBS-Volume-Types  
- EBS Volumes come in 6 types  
	- **gp2 / gp3 (SSD)**: General purpose SSD volume that balances price and performance for  a wide variety of workloads  
	- **io1 / io2 (SSD)**: Highest-performance SSD volume for mission-critical low-latency or high-throughput workloads  
	- **st1 (HDD)**: Low cost HDD volume designed for frequently accessed, throughput- intensive workloads  
	- **sc1 (HDD)**: Lowest cost HDD volume designed for less frequently accessed workloads
- Only **gp2/gp3** and **io1/io2** can be used as boot volumes.
# EBS-behaviour-when-an-EC2-instance-terminates 
- By default, the root EBS volume is deleted (attribute enabled)  
- By default, any other attached EBS volume is not deleted (attribute disabled)
- **Use case**: 
	- Preserve root volume when instance is terminated
![Summary](https://i.imgur.com/RaPaE3T.png)

# Encrypt-unencrypted-EBS-volume  
- Create an EBS snapshot of the volume  
- Encrypt the EBS snapshot ( using copy )  
- Create new ebs volume from the snapshot ( the volume will also be encrypted )  
- Now you can attach the encrypted volume to the original instance
# EFS 
- Elastic File System  
- Managed **NFS** (network file system) that can be mounted on many EC2  
- EFS works with EC2 instances in multi-AZ  
- Highly available, scalable, expensive (3x gp2), pay per use
- Compatible with Linux based AMI (not Windows) 
- Encryption at rest using KMS
- **Use cases**: 
	- Content management
	- Web serving
	- Data sharing
	- Wordpress

# EFS-vs-EBS
- **EBS :
	- Can be attached to only one instance at a time  
	- Are locked at the Availability Zone (AZ) level  
	- **gp2**: IO increases if the disk size increases  
	- **io1**: can increase IO independently  
	- **To migrate an EBS volume across AZ**:
		- Take a snapshot  
		- Restore the snapshot to another AZ  
		- Backups use IO and you shouldn’t run them while your application is handling a lot of traffic
	- Root EBS Volumes of instances get terminated by default if the EC2 instance gets terminated.  (you can disable that)
- **EFS**
- Mounting 100s of instances across AZ  
 - EFS share website files (WordPress)  
- Only for Linux Instances (POSIX)  
- EFS has a higher price point than EBS  
- Can leverage EFS-IA for cost savings 