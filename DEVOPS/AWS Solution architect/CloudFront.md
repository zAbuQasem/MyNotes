# Navigation
- [**CloudFront–Origins**](#CloudFront–Origins)
- [**CloudFront-Geo-Restriction**](#CloudFront-Geo-Restriction)
- [**CloudFront-vs-S3-Cross Region-Replication**](#CloudFront-vs-S3-Cross%20Region-Replication)
- [**CloudFront-Signed-URL--Signed-Cookies**](#CloudFront-Signed-URL--Signed-Cookies)
- [**CloudFront-Multiple-origin**](#CloudFront-Multiple-origin)
- [**CloudFront–Origin-Groups**](#CloudFront–Origin-Groups)
- [**CloudFront–Field-Level-Encryption**](#CloudFront–Field-Level-Encryption)
- [**Unicast-IP-vs-Anycast-IP**](#Unicast-IP-vs-Anycast-IP)
- [**AWS-Global-Accelerator**](#AWS-Global-Accelerator)
# CloudFront
- A Content Delivery Network (CDN)
- DDoS protection, integration withShield, AWS Web Application Firewall  
- Can expose external HTTPS and can talk to internal HTTPS backends
# CloudFront–Origins
- **S3 bucket**
	- For distributing files and caching them at the edge  
	- Enhanced security with CloudFront **Origin Access Identity (OAI)**  
	- CloudFront can be used as an ingress (to upload files to S3)
- **Custom Origin (HTTP)**
	- Application Load Balancer  
	- EC2 instance  
	- S3 website (must first enable the bucket as a static S3 website)  
	- Any HTTP backend you want
# CloudFront-Geo-Restriction
- You can restrict who can access your distribution  
	- **Whitelist**: Allow your users to access your content only if they're in one of the countries on a list of approved countries.  
	- **Blacklist**: Prevent your users from accessing your content if they're in one of the countries on a blacklist of banned countries.
# CloudFront-vs-S3-Cross Region-Replication  
- **CloudFront**:  
	- Global Edge network  
	- Files are cached for a TTL (maybe a day)  
	- **Great for static content that must be available everywhere**  
- **S3 Cross Region Replication**:  
	- Must be setup for each region you want replication to happen  
	- Files are updated in near real-time  
	- Read only  
	- **Great for dynamic content that needs to be available at low-latency in few regions**
# CloudFront-Signed-URL--Signed-Cookies
 You want to distribute paid shared content to premium users over the world  
 - **We can use CloudFront Signed URL / Cookie. We attach a policy with**:  
	 - Includes URL expiration  
	 - Includes IP ranges to access the data from  
	 - Trusted signers (which AWS accounts can create signed URLs)  
 - **How long should the URL be valid for?**  
	 - `Shared content` (movie, music): make it short (a few minutes)  
	 - `Private content` (private to the user): you can make it last for years  
 - Signed URL = access to individual files (one signed URL per file)  
 - Signed Cookies = access to multiple files (one signed cookie for many files)
#  CloudFront-Multiple-origin
- To route to different kind of origins based on the content type
- Based on path pattern:
	- `/images/*`
	- `/api/*`
	- `/*`
# CloudFront–Origin-Groups  
- To increase high-availability and do failover  
- **Origin Group**: one primary and one secondary origin  
- If the primary origin fails, the second one is used
# CloudFront–Field-Level-Encryption  
- Protect user sensitive information through application stack  
- Adds an additional layer of security along with HTTPS  
- Sensitive information encrypted at the edge close to user  
- Uses asymmetric encryption  
- **Usage**:  
	- Specify set of fields in POST requests that you want to be encrypted (up to 10 fields)  
	- Specify the public key to encrypt them
# Unicast-IP-vs-Anycast-IP
- **Unicast**: One server holds one ip address.
- **Anycast**: All servers hold the same ip address ad the client is routed to the nearest one.
# AWS-Global-Accelerator
- Works with Elastic IP, EC2 instances, ALB, NLB, public or private  
- **Consistent Performance**  
	- Intelligent routing to lowest latency and fast regional failover  
	- No issue with client cache (because the IP doesn’t change)  
	- Internal AWS network  
- **Health Checks**  
	- Global Accelerator performs a health check of your applications  
	- Helps make your application global (failover less than 1 minute for unhealthy)  
	- Great for disaster recovery (thanks to the health checks)  
- **Security**  
	- only 2 external IP need to be whitelisted  
	- DDoS protection thanks to AWS Shield
# AWS-Global-Accelerator-vs-CloudFront  
- They both use the AWS global network and its edge locations around the world  
- Both services integrate with AWS Shield for DDoS protection.  
- **CloudFront**  
	- Improves performance for both cacheable content (such as images and videos)  
	- Dynamic content (such as API acceleration and dynamic site delivery)  
	- Content is served at the edge  
- **Global Accelerator**  
	- Improves performance for a wide range of applications over TCP or UDP  
	- Proxying packets at the edge to applications running in one or more AWS Regions.  
	- Good fit for non-HTTP use cases, such as gaming (UDP), IoT (MQTT), or Voice over IP  
	- Good for HTTP use cases that require static IP addresses  
	- Good for HTTP use cases that required deterministic, fast regional failover