# AWS-CloudFormation
- CloudFormation is a declarative way of outlining your AWS  Infrastructure, for any resources (most of them are supported).  
- **For example, within a CloudFormation template, you say**:  
	- I want a security group  
	- I want two EC2 machines using this security group  
	- I want two Elastic IPs for these EC2 machines  
	- I want an S3 bucket  
	- I want a load balancer (ELB) in front of these machines  
	- Then CloudFormation creates those for you, in the right order, with the exact configuration that you specify
## Benefits
- **Infrastructure as code**  
	- No resources are manually created, which is excellent for control  
	- The code can be version controlled for example using git  
	- Changes to the infrastructure are reviewed through code  
- **Cost**  
	- Each resources within the stack is tagged with an identifier so you can easily see how much a stack costs you  
	- You can estimate the costs of your resources using the CloudFormation template  
	- Savings strategy: In Dev, you could automation deletion of templates at 5 PM and recreated at 8 AM, safely
- **Productivity**  
	- Ability to destroy and re-create an infrastructure on the cloud on the fly  
	- Automated generation of Diagram for your templates!  
	- Declarative programming (no need to figure out ordering and orchestration)  
- **Separation of concern: create many stacks for many apps, and many layers. Ex**:  
	- VPC stacks  
	- Network stacks  
	- App stacks  
- **Don’t re-invent the wheel**  
	- Leverage existing templates on the web!  
	- Leverage the documentation
## CloudFormation-WorkFLow
- Templates have to be uploaded in S3 and then referenced in  CloudFormation  
- **To update a template, we can’t edit previous ones. We have to re-upload a new version of the template to AWS**  
- Stacks are identified by a name  
- Deleting a stack deletes every single artifact that was created by CloudFormation.
## Deploying
- **Manual way**:  
	- Editing templates in the CloudFormation Designer  
	- Using the console to input parameters, etc  
- **Automated way**:  
	- Editing templates in a YAML file  
	- Using the AWS CLI (Command Line Interface) to deploy the templates  
	- Recommended way when you fully want to automate your flow
## Building-Blocks
**Templates components**  
1. Resources: your AWS resources declared in the template (MANDATORY)  
2. Parameters: the dynamic inputs for your template  
3. Mappings: the static variables for your template  
4. Outputs: References to what has been created  
5. Conditionals: List of conditions to perform resource creation  
6. Metadata  
**Templates helpers**:  
1. References  
2. Functions
## StackSets
- Create, update, or delete stacks across multiple accounts and regions with a single operation  
- Administrator account to create StackSets  
- Trusted accounts to create, update, delete stack instances from StackSets  
- When you update a stack set, all associated stack instances are updated throughout all accounts and regions.
# AWS-StepFunctions  
- Build serverless visual workflow to orchestrate your Lambda functions  
- Represent flow as a JSON state machine  
- Features: sequence, parallel, conditions, timeouts, error handling...  
- Can also integrate with EC2, ECS, On premise servers, API Gateway  
- Maximum execution time of 1 year  
- Possibility to implement human approval feature  
- **Use cases**:  
	- Order fulfillment  
	- Data processing  
	- Web applications  
	- Any workflow
![](https://i.imgur.com/iDIfEcE.png)
# AWS-SWF
- Coordinate work amongst applications  
- **Code runs on EC2 (not serverless)**  
- 1 year max runtime  
- Concept of “activity step” and “decision step”  
- Has built-in “human intervention” step  
- Example: order fulfilment from web to warehouse to delivery  
- **Step Functions is recommended to be used for new applications, except**:  
	- If you need external signals to intervene in the processes  
	- If you need child processes that return values to parent processes
# Amazon EMR  
- EMR stands for “Elastic MapReduce”  
- EMR helps creating **Hadoop clusters (Big Data)** to analyze and process vast amount of data  
- The clusters can be made of hundreds of EC2 instances  
- Also supports Apache Spark, HBase, Presto, Flink...  
- EMR takes care of all the provisioning and configuration  
- Auto-scaling and integrated with Spot instances  
- **Use cases**: 
	- Data processing
	- Machine learning
	- Web indexing
	- Big data... 
# AWS Opsworks  
- Chef & Puppet help you perform server configuration automatically, or repetitive actions  
- They work great with EC2 & On Premise VM  
- AWS Opsworks = Managed Chef & Puppet  
- It’s an alternative to AWS SSM  
- No hands on here, no knowledge of chef and puppet needed  
> **Important Note**: In the exam: Chef & Puppet needed => AWS Opsworks

# AWS WorkSpaces  
- **Managed, Secure Cloud Desktop**  
- **Great to eliminate management of on-premises VDI (Virtual Desktop Infrastructure)**  
- On Demand, pay per by usage  
- Secure, Encrypted, Network Isolation  
- Integrated with Microsoft Active Directory
# AWS AppSync  
- Store and sync data across mobile and web apps in real-time  
- **Makes use of GraphQL (mobile technology from Facebook)**  
- Client Code can be generated automatically  
- Integrations with DynamoDB / Lambda  
- Real-time subscriptions  
- Offline data synchronization (replaces Cognito Sync)  
- Fine Grained Security
# Cost Explorer  
- Visualize, understand, and manage your AWS costs and usage over time  
- Create custom reports that analyze cost and usage data.  
- Analyze your data at a high level: total costs and usage across all accounts  
- Or Monthly, hourly, resource level granularity  
- Choose an optimal Savings Plan (to lower prices on your bill)  
- **Forecast usage up to 12 months based on previous usage**
