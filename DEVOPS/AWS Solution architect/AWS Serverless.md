# Navigation
- [**Serverless**](#Serverless)
- [**Amazon-Lambda**](#Amazon-Lambda)
	- [**Lambda-At-Edge**](#Lambda-At-Edge)
- [**Amazon-DynamoDB**](#Amazon-DynamoDB)
	- [Read-Write-Capacity-Modes](#Read-Write-Capacity-Modes)
	- [Accelerator-DAX](#Accelerator-DAX)
	- [Streams](#Streams)
	- [Global-Tables](#Global-Tables)
	- [TTL](#TTL)
	- [Indexes](#Indexes)
	- [Transactions](#Transactions)
- [**Amazon-API-Gateway**](#Amazon-API-Gateway)
	- [Integrations-high-level](#Integrations-high-level)
	- [Endpoint-Types](#Endpoint-Types)
	- [Security](#Security)
	- [Lambda-Authorizer](#Lambda-Authorizer)
- [Amazon Cognito](#Amazon%20Cognito)
	- [Cognito-User-Pools-CUPS](#Cognito-User-Pools-CUPS)
	- [Federated-Identity-Pools](#Federated-Identity-Pools)
	- [Amazon-Serverless-Application-Model-SAM](#Amazon-Serverless-Application-Model-SAM)

# Serverless
- Function as a Service => FaaS
- Serverless does not mean there are no servers...it means you just don’t manage /provision / see them
- **Services:**
	- AWS Lambda  
	- DynamoDB  
	- AWS Cognito  
	- AWS API Gateway  
	- Amazon S3  
	- AWS SNS & SQS  
	- AWS Kinesis Data Firehose  
	- Aurora Serverless  
	- Step Functions  
	- Fargate
# Amazon-Lambda
- Virtual functions – no servers to manage!  
- Limited by time - short executions  
- Run on-demand  
- Scaling is automated!
- Pay per request and compute time
- Integrated with the whole AWS suite services
- Easy monitoring through cloudwatch
- Easy to get more resources (up to 10 gb RAM)
- Increading RAM will improve CPU and network
- **Lambda Container Image**  
	- The container image **must** implement the Lambda Runtime API  
	- ECS / Fargate is preferred for running arbitrary Docker images
- **Pricing**
	- It's very cheap -> very popular
	- Pay per calls
	- Pay per duration
## Lambda-At-Edge
- You have deployed a CDN using CloudFront  
- What if you wanted to run a global AWS Lambda alongside?  
- Or how to implement request filtering before reaching your application?  
- **For this, you can use Lambda@Edge**:  
	- Deploy Lambda functions alongside your CloudFront CDN  
	- Build more responsive applications  
	- You don’t manage servers, Lambda is deployed globally  
	- Customize the CDN content  
	- Pay only for what you use
- **Use Cases**:
	- Website Security and Privacy  
	- Dynamic Web Application at the Edge  
	- Search Engine Optimization (SEO)  
	- Intelligently Route Across Origins and Data Centers  
	- Bot Mitigation at the Edge  
	- Real-time Image Transformation  
	- A/B Testing  
	- User Authentication and Authorization  
	- User Prioritization  
	- User Tracking and Analytics
# Amazon-DynamoDB
- *Fully managed, highly available with replication across multiple AZs*  
- NoSQL database - not a relational database  
- Scales to massive workloads, distributed database  
- Millions of requests per seconds, trillions of row, 100s of TB of storage  
- *Fast and consistent in performance* (low latency on retrieval)  
- Integrated with IAM for security, authorization and administration  
- Enables event driven programming with DynamoDB Streams  
- *Low cost and auto-scaling capabilities*  
- Standard & Infrequent Access (IA) Table Class
## Read-Write-Capacity-Modes
- **Provisioned Mode** (default)  
	- You specify the number of reads/writes per second  
	- You need to plan capacity beforehand  
	- *Pay for provisioned Read Capacity Units (RCU) & Write Capacity Units (WCU)*  
	- Possibility to add auto-scaling mode for RCU & WCU  
- **On-Demand Mode**  
	- Read/writes automatically scale up/down with your workloads  
	- No capacity planning needed  
	- Pay for what you use, more expensive  
	- Great for unpredictable workloads
## Accelerator-DAX
- Fully-managed, highly available, seamless **in-memory cache** for DynamoDB  
- Help solve read congestion by caching  
- Microseconds latency for cached data  
- Doesn’t require application logic modification (compatible with existing DynamoDB APIs)  
- 5 minutes TTL for cache (default)
## Streams
Ordered stream of item-level modifications (create/update/delete) in a table  
- **Stream records can be**:  
	- Sent to Kinesis Data Streams  
	- Read by AWS Lambda  
	- Read by Kinesis Client Library applications  
- Data Retention for up to 24 hours  
- **Use cases**:  
	- React to changes in real-time (welcome email to users)  
	- Analytics  
	- Insert into derivative tables  
	- Insert into ElasticSearch  
	- Implement cross-region replication
## Global-Tables
- Make a DynamoDB table accessible with low latency in multiple-regions  
- Active-Active replication  
- Applications can READ and WRITE to the table in any region  
- Must enable DynamoDB Streams as a pre-requisite
## TTL
- Auto delete items after an expiry timestamp
- **Use cases**:
	- Reduce stored data by keeping only current items
	- adhere to regulatory obligations (التقيد بالالتزامات التنظيمية)
## Indexes
- Global Secondary Indexes (GSI) & Local Secondary Indexes (LSI)  
- **High level**: allow to query on attributes other than the Primary Key
## Transactions
- A Transaction is written to both tables, or none
- *Such as a transaction between two bank accounts*
![](https://i.imgur.com/MNJ4A1K.png)
# Amazon-API-Gateway
- *AWS Lambda + API Gateway: No infrastructure to manage*  
- Support for the WebSocket Protocol  
- Handle API versioning (v1, v2...)  
- Handle different environments (dev, test, prod...)  
- Handle security (Authentication and Authorization)  
- Create API keys, handle request throttling  
- Swagger / Open API import to quickly define APIs  
- Transform and validate requests and responses  
- Generate SDK and API specifications  
- Cache API responses
## Integrations-high-level
- **Lambda Function**
	- Invoke Lambda function
	- Easy way to expose REST API backed by AWS Lambda
- **HTTP**
	- Expose HTTP Endpoint in the backend
	- Example: internal HTTP API on premise, Application Load Balancer...
	- Add rate limiting, caching, user authentications, API keys, etc...
- AWS Service
	- Expose any AWS through API Gateway
	- Example: start an AWS Step Function workflow, post a message to SQS  
	- Add authentication, deploy publicly, rate control...
## Endpoint-Types
- **Edge-Optimized (default)**: For global clients  
	- Requests are routed through the CloudFront Edge locations (improves latency)  
	- The API Gateway still lives in only one region  
- **Regional**:  
	- For clients within the same region  
	- Could manually combine with CloudFront (more control over the caching strategies and the distribution)  
- **Private**:  
	- Can only be accessed from your VPC using an interface VPC endpoint (ENI)  
	- Use a resource policy to define access
## Security
- Create an IAM policy authorization and attach to User / Role  
- API Gateway verifies IAM permissions passed by the calling application  
- Good to provide access within your own infrastructure  
- Leverages “Sig v4” capability *where IAM credential are in headers*
![](https://i.imgur.com/Th3vDwt.png) 
## Lambda-Authorizer
- Uses AWS Lambda to validate the token in header being passed  
- Option to cache result of authentication  
- Helps to use OAuth / SAML / 3rd party type of authentication  
- Lambda must return an IAM policy for the user
![](https://i.imgur.com/mk94M55.png)
# Amazon Cognito

- We want to give our users an identity so that they can interact with our application.  
- **Cognito User Pools**:  
	- Sign in functionality for app users  
	- Integrate with API Gateway  
- **Cognito Identity Pools** (Federated Identity):  
	- Provide AWS credentials to users so they can access AWS resources directly  
	- Integrate with Cognito User Pools as an identity provider  
- **Cognito Sync**:  
	- Synchronize data from device to Cognito.  
	-  **Note**: *May be deprecated and replaced by AppSync*
## Cognito-User-Pools-CUPS
- Create a serverless database of user for your mobile apps  
- Simple login: Username (or email) / password combination  
- Possibility to verify emails / phone numbers and add MFA  
- Can enable Federated Identities (Facebook, Google, SAML...)  
- Sends back a JSON Web Tokens (JWT)  
- Can be integrated with API Gateway for authentication
## Federated-Identity-Pools
- **Goal**:  
	- Provide direct access to AWS Resources from the Client Side  
- **How**:  
	- Log in to federated identity provider – or remain anonymous  
	- Get temporary AWS credentials back from the Federated Identity Pool  
	- These credentials come with a pre-defined IAM policy stating their permissions  
- **Example**:  
	- provide (temporary) access to write to S3 bucket using Facebook Login
![](https://i.imgur.com/3SxcxL7.png)

# Amazon-Serverless-Application-Model-SAM
- Framework for developing and deploying serverless applications  
- **All the configuration is YAML code**  
	- Lambda Functions  
	- DynamoDB tables  
	- API Gateway  
	- Cognito User Pools  
- SAM can help you to run Lambda, API Gateway, DynamoDB locally  
- SAM can use CodeDeploy to deploy Lambda functions