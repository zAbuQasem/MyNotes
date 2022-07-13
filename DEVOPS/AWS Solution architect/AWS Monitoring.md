# Navigation
- [**CloudWatch-Mertics**](#CloudWatch-Mertics)
	- [CloudWatch-Custom-Metrics](#CloudWatch-Custom-Metrics)
	- [CloudWatch-Dashboards](#CloudWatch-Dashboards)
	- [CloudWatch-Logs](#CloudWatch-Logs)
	- [CloudWatch-Logs-Metric-Filter](#CloudWatch-Logs-Metric-Filter)
	- [CloudWatch-Logs–S3Export](#CloudWatch-Logs–S3Export)
	- [CloudWatch-Logs-Agent-and-Unified-Agent](#CloudWatch-Logs-Agent-and-Unified-Agent)
- [**EC2-Detailed-monitoring**](#EC2-Detailed-monitoring)
	- [CloudWatch-Logs-EC2](#CloudWatch-Logs-EC2)
- [**CloudWatch-Alarm-Targets**](#CloudWatch-Alarm-Targets)
- [**Amazon-EventBridge**](#Amazon-EventBridge)
	- [Schema-Registry](#Schema-Registry)
	- [Resource-based-Policy](#Resource-based-Policy)
	- [EventBridge-vs-CloudWatch-Events](#EventBridge-vs-CloudWatch-Events)
- [**AWS-CloudTrail**](#AWS-CloudTrail)
	- [CloudTrail-Events](#CloudTrail-Events)
	- [CloudTrail-Events-Retention](#CloudTrail-Events-Retention)
- [**AWS-Config**](#AWS-Config)
	- [Config Rules](#Config%20Rules)
	- [Remediation](#Remediation)
	- [Notifications](#Notifications)
- [**Summary**](#Summary)
	- [Elastic-LoadBalancer](#Elastic-LoadBalancer)
# CloudWatch-Mertics
- CloudWatch provides metrics for every services in AWS
- Up to 10 dimensions per metric  
- Metrics have timestamps  
- Can create CloudWatch dashboards of metrics
## CloudWatch-Custom-Metrics
- Possibility to define and send your own custom metrics to CloudWatch  
	- Example: memory (RAM) usage, disk space, number of logged in users ...  
- Use API call **PutMetricData**  
- Ability to use dimensions (attributes) to segment metrics  
	- Instance.id  
	- Environment.name  
- Metric resolution (StorageResolution API parameter – two possible value):  
	- Standard: 1 minute (60 seconds)  
	- High Resolution: 1/5/10/30 second(s) – Higher cost  
- **Note**: Accepts metric data points two weeks in the past and two hours in the future (make sure to configure your EC2 instance time correctly)
# CloudWatch-Dashboards
- Great way to setup custom dashboards for quick access to key metrics and alarms  
- **Dashboards are global**  
- **Dashboards can include graphs from different AWS accounts and regions**  
- You can change the time zone & time range of the dashboards  
- You can setup automatic refresh (10s, 1m, 2m, 5m, 15m)  
- **Dashboards can be shared with people who don’t have an AWS account** (public, email address, 3 rd party SSO provider through Amazon Cognito)
## CloudWatch-Logs
- **Log groups**: arbitrary name, usually representing an application  
- **Log stream**: instances within application / log files / containers  
- Can define log expiration policies (never expire, 30 days, etc..)  
- **CloudWatch Logs can send logs to**:  
	- Amazon S3 (exports)  
	- Kinesis Data Streams  
	- Kinesis Data Firehose  
	- AWS Lambda  
	- ElasticSearch
## CloudWatch-Logs-Metric-Filter
- CloudWatch Logs can use filter expressions  
	- For example, find a specific IP inside of a log  
	- Or count occurrences of “ERROR” in your logs  
- Metric filters can be used to trigger CloudWatch alarms  
- CloudWatch Logs Insights can be used to query logs and add queries to CloudWatch Dashboards
## CloudWatch-Logs–S3Export
- Log data can take **up to 12 hours** to become available for export  
- The API call is **CreateExportTask**  
> **Note**: Not near-real time or real-time... use Logs Subscriptions instead
## CloudWatch-Logs-Agent-and-Unified-Agent
- For virtual servers (EC2 instances, on-premises servers...)  
- **CloudWatch Logs Agent**  
	- Old version of the agent  
	- Can only send to CloudWatch Logs  
- **CloudWatch Unified Agent**  
	- Collect additional system-level metrics such as RAM, processes, etc...  
	- Collect logs to send to CloudWatch Logs  
	- Centralized configuration using SSM Parameter Store
	- - Collected directly on your Linux server / EC2 instance  
	- CPU (active, guest, idle, system, user, steal)  
	- Disk metrics (free, used, total), Disk IO (writes, reads, bytes, iops)  
	- RAM (free, inactive, used, total, cached)  
	- Netstat (number of TCP and UDP connections, net packets, bytes)  
	- Processes (total, dead, bloqued, idle, running, sleep)  
	- Swap Space (free, used, used %)  
	- **Reminder**: out-of-the box metrics for EC2 – disk, CPU, network (high level)
# EC2-Detailed-monitoring
- EC2 instance metrics have metrics “every 5 minutes”  
- With detailed monitoring (for a cost), you get data “every 1 minute”  
- Use detailed monitoring if you want to scale faster for your ASG!  
- The AWS Free Tier allows us to have 10 detailed monitoring metrics  
> **Note**: EC2 Memory usage is by default not pushed (must be pushed  from inside the instance as a custom metric)
## CloudWatch-Logs-EC2
- By default, no logs from your EC2 machine will go to CloudWatch  
- You need to run a CloudWatch agent on EC2 to push the log filesyou want  
- Make sure IAM permissions are correct  
- The CloudWatch log agent can be setup on-premises too
# CloudWatch-Alarm-Targets
- Stop,Terminate,Reboot or Recover an EC2 instance
- Trigger Auto Scaling group
- Send Notification from SNS
-  Period: 
	- Length of time in seconds to evaluate the metric
	- **High resolution custom metrics: 10 sec, 30 sec or multiples of 60 sec**
# Amazon-EventBridge
- EventBridge is the next evolution of CloudWatch Events  
- **Default Event Bus** – generated by AWS services (CloudWatch Events)  
- **Partner Event Bus** – receive events from SaaS service or applications (Zendesk, DataDog, Segment, Auth0...)  
- **Custom Event Buses** – for your own applications  
- Event buses can be accessed by other AWS accounts  
- You can archive events (all/filter) sent to an event bus (indefinitely or set period)  
- Ability to replay archived events
## Schema-Registry
- EventBridge can analyze the events in your bus and infer the schema  
- The **Schema Registry** allows you to generate code for your application, that will know in advance how data is structured in the event bus  
- Schema can be versioned
## Resource-based-Policy
- Manage permissions for a specific Event Bus
- **Example**: Allow/deny events from another AWS account or AWS region
- **Use case**:
	- Aggregate all events from your AWS Organization in a single AWS account or AWS region.
## EventBridge-vs-CloudWatch-Events
- Amazon EventBridge *builds upon and extends CloudWatch Events*.  
- It uses the same service API and endpoint, and the same underlying service infrastructure.  
- EventBridge allows extension to add event buses for your custom applications and your third-party SaaS apps.  
- Event Bridge has the Schema Registry capability  
- EventBridge has a different name to mark the new capabilities  
- Over time, the CloudWatch Events name will be replaced with EventBridge
# AWS-CloudTrail
- Provides governance, compliance and audit for your AWS Account  
- CloudTrail is enabled by default!  
- **Get a history of events / API calls made within your AWS Account by**:  
	- Console  
	- SDK  
	- CLI  
	- AWS Services  
- Can put logs from CloudTrail into CloudWatch Logs or S3  
- A trail can be applied to All Regions (default) or a single Region.  
> **Note**:If a resource is deleted in AWS, investigate CloudTrail first!
## CloudTrail-Events
- **Management Events**:  
- Operations that are performed on resources in your AWS account....Examples:  
	- Configuring security (IAM AttachRolePolicy)  
	- Configuring rules for routing data (Amazon EC2 CreateSubnet)  
	- Setting up logging (AWS CloudTrail CreateTrail)  
- **By default, trails are configured to log management events**.  
- Can separate **Read Events** (that don’t modify resources) from **Write Events** (that may modify resources)  
- **Data Events**:  
	- **By default, data events are not logged** (because high volume operations)  
	- Amazon S3 object-level activity (ex: GetObject, DeleteObject, PutObject): can separate Read and Write Events  
	- AWS Lambda function execution activity (the Invoke API)
## CloudTrail-Insights
- **Enable CloudTrail Insights to detect unusual activity in your account:**  
	- inaccurate resource provisioning  
	- hitting service limits  
	- Bursts of AWS IAM actions  
	- Gaps in periodic maintenance activity  
- CloudTrail Insights analyzes normal management events to create a baseline and then **continuously analyzes write events to detect unusual patterns**  
	- Anomalies appear in the CloudTrail console  
	- Event is sent to Amazon S3  
	- An EventBridge event is generated (for automation needs)
![](https://i.imgur.com/Hf1nYDi.png)

## CloudTrail-Events-Retention
- Events are stored for 90 days
- To keep events beyond this period, log them to S3 and use Athena
# AWS-Config
- Helps with auditing and recording compliance of your AWS resources  
- Helps record configurations and changes over time  
- **Questions that can be solved by AWS Config**:  
	- Is there unrestricted SSH access to my security groups?  
	- Do my buckets have any public access?  
	- How has my ALB configuration changed over time?  
- You can receive alerts (SNS notifications) for any changes  
- AWS Config is a per-region service  
- Can be aggregated across regions and accounts  
- Possibility of storing the configuration data into S3 (analyzed by Athena)
## Config Rules
- Can use AWS managed config rules (over 75)  
- Can make custom config rules (must be defined in AWS Lambda)  
	- Ex: evaluate if each EBS disk is of type gp2  
	- Ex: evaluate if each EC2 instance is t2.micro  
- Rules can be evaluated / triggered:  
	- For each config change  
	- And / or: at regular time intervals  
- **AWS Config Rules does not prevent actions from happening** (no deny)
## Remediation
- Automate remediation of non-compliant resources using **SSM Automation Documents**  
- Use AWS-Managed Automation Documents or create custom Automation Documents  
- Tip: you can create custom Automation Documents that invokes Lambda function  
- You can set Remediation Retries if the resource is still non-compliant after auto-remediation
## Notifications
- Use EventBridge to trigger notifications when AWS resources are non-compliant
![](https://i.imgur.com/45XSF6M.png)
- Ability to send configuration changes and compliance state notifications to SNS (all events – use SNS Filtering or filter at client-side)
![](https://i.imgur.com/7u91eqE.png)

# Summary  
- **CloudWatch**  
	- Performance monitoring (metrics, CPU, network, etc...) & dashboards  
	- Events & Alerting  
	- Log Aggregation & Analysis  
- **CloudTrail**  
	- Record API calls made within your Account by everyone  
	- Can define trails for specific resources  
	- Global Service  
- **Config**  
	- Record configuration changes  
	- Evaluate resources against compliance rules  
	- Get timeline of changes and compliance
## Elastic-LoadBalancer
- **CloudWatch:**  
	- Monitoring Incoming connections metric  
	- Visualize error codes as % over time  
	- Make a dashboard to get an idea of your load balancer performance  
- **Config:**  
	- Track security group rules for the Load Balancer  
	- Track configuration changes for the Load Balancer  
	- Ensure an SSL certificate is always assigned to the Load Balancer (compliance)  
- **CloudTrail:**  
	- Track who made any changes to the Load Balancer with API calls