
# Navigator
- [**AWS-STS**](#AWS-STS)
	- [Assume-Role](#Assume-Role)
	- [Identity-Federation](#Identity-Federation)
	- [Custom-Identity-Broker-Application](#Custom-Identity-Broker-Application)
	- [Web-Identity-Federation](#Web-Identity-Federation)
- [**AWS-Organizations**](#AWS-Organizations)
	- [Service-Control-Policies](#Service-Control-Policies)
	- [Moving-Accounts](#Moving-Accounts)
- [**IAM-Permission-Boundaries**](#IAM-Permission-Boundaries)
- [**AWS-Resource-Access-Manager**](#AWS-Resource-Access-Manager)
	- [AWS-SSO](#AWS-SSO)
# AWS-STS
- STS = Security Token Service
- Allows to grant limited and temporary access to AWS resources.  
- Token is valid for up to one hour (must be refreshed)  
- **AssumeRole**  
	- *Within your own account:* for enhanced security  
	- *Cross Account Access*: assume role in target account to perform actions there  
- **AssumeRoleWithSAML**  (old way)
	- Return credentials for users logged with SAML  
	- Needs to setup a trust between AWS IAM and SAML (both ways)  
	- SAML 2.0 enables web-based, cross domain SSO
	- *Amazon Single Sign On (SSO) Federation is the new managed and simpler way* 
- **AssumeRoleWithWebIdentity**  
	- Return creds for users logged with an IdP (Facebook Login, Google Login, OIDC compatible...)  
	- AWS recommends against using this, and using Cognito instead  
- **GetSessionToken**  
	- for MFA, from a user or AWS account root user
## Assume-Role
- Define an IAM Role within your account or cross-account  
- Define which principals can access this IAM Role  
- Use AWS STS (Security Token Service) to retrieve credentials and impersonate the IAM Role you have access to (AssumeRole API)  
- **Temporary credentials can be valid between 15 minutes to 1 hour**
## Identity-Federation
- Federation lets users outside of AWS to assume temporary role for accessing AWS resources.  
- These users assume identity provided access role.  
- **Federations can have many flavors**:  
	- SAML 2.0  (old way)
	- Custom Identity Broker  
	- Web Identity Federation with Amazon Cognito  
	- Web Identity Federation without Amazon Cognito  
	- Single Sign On - SSO (New easier managed way)  
	- Non-SAML with AWS Microsoft AD  
> **Note**: Using federation, you don’t need to create IAM users (user management is outside of AWS
## Custom-Identity-Broker-Application
- Use only if identity provider is not compatible with SAML 2.0  
- **The identity broker must determine the appropriate IAM policy**  
- Uses the STS API: `AssumeRole` or `GetFederationToken`
## Web-Identity-Federation
- Uses the STS API: `AssumeRoleWithWebIdentity`
- Not recommended by AWS - use `Cognito` instead
# AWS-Directory-Services
- **AWS Managed Microsoft AD**  
	- Create your own AD in AWS, manage users locally, supports MFA  
	- Establish “trust” connections with your on-premises AD  
- **AD Connector**  
	- Directory Gateway (proxy) to redirect to on-premises AD, supports MFA  
	- Users are managed on the on-premises AD  
- **Simple AD**  
	- AD-compatible managed directory on AWS  
	- Cannot be joined with on-premises AD
# AWS-Organizations
- Global service  
- Allows to manage multiple AWS accounts  
- The main account is the master account – you can’t change it  
- Other accounts are member accounts  
- Member accounts can only be part of one organization  
- Consolidated Billing across all accounts - single payment method  
- Pricing benefits from aggregated usage (volume discount for EC2, S3...)  
- API is available to automate AWS account creation
## Service-Control-Policies
- **SCP** = Service Control Policies
- Whitelist or blacklist IAM actions  
- Applied at the OU or Account level  
- Does not apply to the Master Account  
- SCP is applied to all the Users and Roles of the Account, including Root user  
- **The SCP does not affect service-linked roles**  
	- Service-linked roles enable other AWS services to integrate with AWS Organizations and can't be restricted by SCPs.  
- **SCP must have an explicit Allow (does not allow anything by default)**  
- **Use cases:**  
	- Restrict access to certain services (for example: can’t use EMR)  
	- Enforce PCI compliance by explicitly disabling services
## Moving-Accounts
- **To migrate accounts from one organization to another**  
	1. Remove the member account from the old organization
	2. Send an invite to the new organization
	3. Accept the invite to the new organization from the member account
- **If you want the master account of the old organization to also join the new organization, do the following**:  
	1. Remove the member accounts from the organizations using procedure above
	2. Delete the old organization  
	3. Repeat the process above to invite the old master account to the new org
# IAM-Permission-Boundaries
- IAM Permission Boundaries are supported for users and roles (**not groups**)  
- Advanced feature to use a managed policy to set the maximum permissions an IAM entity can get.
- **Use cases**  
	- Delegate responsibilities to non administrators within their permission boundaries, for example create new IAM users  
	- Allow developers to self-assign policies and manage their own permissions, while making sure they can’t “escalate” their privileges (= make themselves admin)  
	- Useful to restrict one specific user (instead of a whole account using Organizations & SCP)
![](https://i.imgur.com/HXNdcxJ.png)

# AWS-Resource-Access-Manager
- **RAM**: AWS Resource Access Manager
- Share AWS resources that you own with other AWS accounts  
- Share with any account or within your Organization  
- Avoid resource duplication!  
- **VPC Subnet**s:  
	- Allow to have all the resources launched in the same subnets  
	- Must be from the same AWS Organizations.  
	- **Cannot share security groups and default VPC**  
	- Participants can manage their own resources in there  
	- Participants can't view, modify, delete resources that belong to other participants or the owner  
- **AWS Transit Gateway**  
- **Route53 Resolver Rules**  
- **License Manager Configurations**
## AWS-SSO
- Centrally manage Single Sign-On to access multiple accounts and 3rd -party business applications.  
- Integrated with AWS Organizations  
- Supports SAML 2.0 markup  
- Integration with on-premises Active Directory  
- Centralized permission management  
- Centralized auditing with CloudTrail