# Navigation
- [**CloudFront–Origins**](#CloudFront–Origins)
- [**CloudFront-Geo-Restriction**](#CloudFront-Geo-Restriction)
- [**CloudFront-vs-S3-Cross Region-Replication**](#CloudFront-vs-S3-Cross%20Region-Replication)
- [**CloudFront-Signed-URL--Signed-Cookies**](#CloudFront-Signed-URL--Signed-Cookies)
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
