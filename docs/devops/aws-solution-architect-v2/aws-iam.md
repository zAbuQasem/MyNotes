# IAM Summary
- **Users**: mapped to a physical user, has a password for AWS Console  
- **Groups**: contains users only  
- **Policies**: JSON document that outlines permissions for users or groups  
- **Roles**: for EC2 instances or AWS services  
- **Security**: MFA + Password Policy  
- **Access** **Keys**: access AWS using the CLI or SDK  
- **Audit**: IAM Credential Reports & IAM Access Advisor

## IAM Guidelines & Best Practices  
- Don’t use the root account except for AWS account setup  
- One physical user = One AWS user  
- Assign users to groups and assign permissions to groups  
- Create a strong password policy  
- Use and enforce the use of Multi Factor Authentication (MFA)  
- Create and use Roles for giving permissions to AWS services  
- Use Access Keys for Programmatic Access (CLI / SDK)  
- Audit permissions of your account with the IAM Credentials Report  
- Never share IAM users & Access Keys

## IAM Security Tools  
- **IAM Credentials Report (account-level)**  
	- a report that lists all your account's users and the status of their various  
	credentials  
- **IAM Access Advisor (user-level)**  
	- Access advisor shows the service permissions granted to a user and when thoseservices were last accessed.  
	- You can use this information to revise your policies.

# CLI
## List policies
```bash
aws iam list-policies --max-items 2
```
## Create a user
```bash
aws iam create-user  --user-name <NAME> --permissions-boundary <POLICY ARN>
```

## Observations
- CLI creds are stored in plain at:
```bash
/home/$USER/.aws/credentials
```
# References
- [CLI interface doc.](https://docs.aws.amazon.com/cli/latest/reference/iam/)