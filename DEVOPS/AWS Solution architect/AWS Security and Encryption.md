# Navigation
- [**AWS-KMS**](#AWS-KMS)
	- [KMS-CMK](#KMS-CMK)
	- [KMS-Automatic-Key-Rotation](#KMS-Automatic-Key-Rotation)
	- [KMS-Manual-Key-Rotation](#KMS-Manual-Key-Rotation)
- [**SSM-Parameter-Store**](#SSM-Parameter-Store)
	- [Parameter-Policies](#Parameter-Policies)
- [**AWS-Secrets-Manager**](#AWS-Secrets-Manager)
- [**AWS-Shield**](#AWS-Shield)
- [**CloudHSM**](#CloudHSM)
	- [High-Availability](#High-Availability)
	- [CloudHSM-vs-KMS](#CloudHSM-vs-KMS)
- [**AWS-WAF**](#AWS-WAF)
- [**AWS-Firewall-Manager**](#AWS-Firewall-Manager)
# AWS-KMS
- **KMS**: Key Management Service
- Easy way to control access to your data, AWS manages keys for us  
- Fully integrated with IAM for authorization
- Three types of Customer Master Keys (CMK):  
	- AWS Managed Service Default CMK: free  
	- User Keys created in KMS: $1 / month  
	- User Keys imported (must be 256-bit symmetric key): $1 / month
- **KMS can only help in encrypting up to 4KB of data per call**  
- **If data > 4 KB, use envelope encryption**
## KMS-CMK
**CMK**: Custom Master Key
- **Symmetric (AES-256)**
	- First offering of KMS, single encryption key that is used to Encrypt and Decrypt  
	- AWS services that are integrated with KMS use Symmetric CMKs
	- Necessary for envelope encryption  
	- You never get access to the Key unencrypted (must call KMS API to use)
- **Asymmetric (RSA & ECC key pairs)**  
	- Public (Encrypt) and Private Key (Decrypt) pair  
	- Used for Encrypt/Decrypt, or Sign/Verify operations  
	- The public key is downloadable, but you can’t access the Private Key unencrypted  
	- **Use case**: encryption outside of AWS by users who can’t call the KMS API
## KMS-Automatic-Key-Rotation
- **For Customer-managed CMK** (not AWS managed CMK)  
- If enabled: automatic key rotation happens every 1 year  
- Previous key is kept active so you can decrypt old data  
- New Key has the same CMK ID (only the backing key is changed)
## KMS-Manual-Key-Rotation
- **When you want to rotate key every 90 days, 180 days, etc...**  
- New Key has a different CMK ID  
- Keep the previous key active so you can decrypt old data  
- Better to use aliases in this case (to hide the change of key for the application)  
- Good solution to rotate CMK that are not eligible for automatic rotation (like asymmetric CMK)
# SSM-Parameter-Store
- Secure storage for configuration and secrets  
- Optional Seamless Encryption using KMS  
- Serverless, scalable, durable, easy SDK  
- Version tracking of configurations / secrets  
- Configuration management using path & IAM  
- Notifications with CloudWatch Events  
- Integration with CloudFormation
## Parameter-Policies
- For Advanced parameters
- **Allow to assign a TTL to a parameter (expiration date) to force updating or deleting sensitive data such as passwords**  
- Can assign multiple policies at a time
# AWS-Secrets-Manager
- Newer service, meant for storing secrets  
- **Capability to force rotation of secrets every X days**  
- Automate generation of secrets on rotation (uses Lambda)  
- Integration with Amazon RDS (MySQL, PostgreSQL, Aurora)  
- Secrets are encrypted using KMS  
- **Mostly meant for RDS integration**
# AWS-Shield
- **AWS Shield Standard:**  
	- *Free service that is activated for every AWS customer*  
	- Provides protection from attacks such as SYN/UDP Floods, Reflection attacks and other layer 3/layer 4 attacks
- **AWS Shield Advanced:**  
	- Optional DDoS mitigation service ($3,000 per month per organization)  
	- Protect against more sophisticated attack on `Amazon EC2`, `Elastic Load  Balancing (ELB)`, `Amazon CloudFront`, `AWS Global Accelerator`, and `Route 53`  
	- 24/7 access to AWS DDoS response team (DRP)  
	- Protect against higher fees during usage spikes due to DDoS
# CloudHSM
- **Dedicated Hardware (HSM = Hardware Security Module)**
- **KMS** => AWS manages the software for encryption  
- **CloudHSM** => AWS provisions encryption hardware    
- **You manage your own encryption keys entirely (not AWS)**  
- HSM device is tamper resistant, FIPS 140-2 Level 3 compliance  
- Supports both symmetric and asymmetric encryption (SSL/TLS keys)  
- No free tier available  
- Must use the CloudHSM Client Software  
- Redshift supports CloudHSM for database encryption and key management 
- Good option to use with SSE-C encryption
## High-Availability
- CloudHSM clusters are spread across Multi AZ
- Great for availability and durability
## CloudHSM-vs-KMS
![](https://i.imgur.com/f7xNEJi.png)
# AWS-WAF
- Deploy on `ALB`, `API Gateway`, `CloudFront`
- **Define Web ACL (Web Access Control List):**  
	- Rules can include: IP addresses, HTTP headers, HTTP body, or URI strings  
	- Protects from common attack - SQL injection and Cross-Site Scripting (XSS)  
	- Size constraints, geo-match (block countries)  
	- Rate-based rules (to count occurrences of events) – for DDoS protection
# AWS-Firewall-Manager
- Manage rules in all accounts of an AWS Organization  
- Common set of security rules  
- WAF rules (Application Load Balancer, API Gateways, CloudFront)  
- AWS Shield Advanced (ALB, CLB, Elastic IP, CloudFront)  
- Security Groups for EC2 and ENI resources in VPC
# AWS-GuardDuty
- Intelligent Threat discovery to Protect AWS Account  
- Uses Machine Learning algorithms, anomaly detection, 3rd party data  
- One click to enable (30 days trial), no need to install software  
- **Input data includes**:  
	- CloudTrail Events Logs – unusual API calls, unauthorized deployments  
		- CloudTrail Management Events – create VPC subnet, create trail, ...  
		- CloudTrail S3 Data Events – get object, list objects, delete object, ...  
	- VPC Flow Logs – unusual internal traffic, unusual IP address  
	- DNS Logs – compromised EC2 instances sending encoded data within DNS queries  
	- Kubernetes Audit Logs – suspicious activities and potential EKS cluster compromises  
- Can setup CloudWatch Event rules to be notified in case of findings  
- CloudWatch Events rules can target AWS Lambda or SNS  
- **Can protect against CryptoCurrency attacks (has a dedicated "finding" for it)**
![](https://i.imgur.com/yf6owLJ.png)
# AWS-Inspector
- Automated Security Assessments  
- **For EC2 instances**  
	- Leveraging the AWS System Manager (SSM) agent  
	- Analyze against unintended network accessibility  
	- Analyze the running OS against known vulnerabilities  
- **For Containers push to Amazon ECR**  
	- Assessment of containers as they are pushed   
- Reporting & integration with AWS Security Hub  
- Send findings to Amazon Event Bridge
> **Note**: Remember that it's only for EC2 instances and container infrastructure. 
# AWS-Macie
- Amazon Macie is a fully managed data security and data privacy service that **uses machine learning and pattern matching to discover and protect your sensitive data in AWS**.  
- Macie helps identify and **alert you to sensitive data, such as personally identifiable information (PII)**
![](https://i.imgur.com/Evf8oDX.png)

# AWS-Shared-Responsibility-Model
- **AWS responsibility - Security of the Cloud**  
	- Protecting infrastructure (hardware, software, facilities, and networking) that runs all the AWS services  
	- Managed services like S3, DynamoDB, RDS, etc.  
- **Customer responsibility - Security in the Cloud**  
	- For EC2 instance, customer is responsible for management of the guest OS (including security patches and updates), firewall & network configuration, IAM  
	- Encrypting application data  
- **Shared controls**:  
	- Patch Management, Configuration Management, Awareness & Training
## RDS-Example
- **AWS responsibility:**  
	- Manage the underlying EC2 instance, disable SSH access  
	- Automated DB patching  
	- Automated OS patching  
	- Audit the underlying instance and disks & guarantee it functions  
- **Your responsibility:**  
	- Check the ports / IP / security group inbound rules in DB’s SG  
	- In-database user creation and permissions  
	- Creating a database with or without public access  
	- Ensure parameter groups or DB is configured to only allow SSL connections  
	- Database encryption setting
## S3-Example
- **AWS responsibility:**  
	- Guarantee you get unlimited storage  
	- Guarantee you get encryption  
	- Ensure separation of the data between different customers  
	- Ensure AWS employees can’t access your data  
- **Your responsibility:**  
	- Bucket configuration  
	- Bucket policy / public setting  
	- IAM user and roles  
	- Enabling encryption
## Diagram
![](https://i.imgur.com/nK7vh8n.png)
