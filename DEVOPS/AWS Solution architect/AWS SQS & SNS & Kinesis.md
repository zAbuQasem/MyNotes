# Navigation
- [**SQS–Standard Queue**](#SQS–Standard%20Queue)
	- [SQS–Producing Messages](#SQS–Producing%20Messages)
	- [SQS–Consuming Messages](#SQS–Consuming%20Messages)
	- [SQS–Multiple-EC2-Instances-Consumers](#SQS–Multiple-EC2-Instances-Consumers)
	- [SQS-Security](#SQS-Security)
	- [SQS–Message-Visibility-Timeout](#SQ%20–Message-Visibility-Timeout)
	- [Amazon-SQS–Dead-Letter-Queue](#Amazon-SQS–Dead-Letter-Queue)
	- [SQS-DLQ–Redrive-to-Source](#SQS-DLQ–Redrive-to-Source)
- 
# SQS–Standard Queue
- Fully managed service, used to decouple applications
- **Attributes**:  
	- Unlimited throughput, unlimited number of messages in queue  
	- Default retention of messages: 4 days, maximum of 14 days  
	- Low latency (<10 ms on publish and receive)  
	- Limitation of 256KB per message sent  
	- Can have duplicate messages (at least once delivery, occasionally)  
	- Can have out of order messages (best effort ordering)
![](https://i.imgur.com/a46UVxx.png)
## SQS–Producing Messages
- Produced to SQS using the SDK (SendMessage API)  
- The message is persisted in SQS until a consumer deletes it  
- Message retention: default 4 days, up to 14 day
- SQS standard: unlimited throughput
- **Example: send an order to be processed**  
	- Order id  
	- Customer id  
	- Any attributes you want
## SQS–Consuming Messages  
- Consumers (running on EC2 instances, servers, or AWS Lambda)...  
- Poll SQS for messages (receive up to 10 messages at a time)  
- Process the messages (example: insert the message into an RDS database)  
- Delete the messages using the DeleteMessage API
![](https://i.imgur.com/BsqkaiO.png)
## SQS–Multiple-EC2-Instances-Consumers  
- Consumers receive and process messages in parallel  
- At least once delivery  
- Best-effort message ordering  
- Consumers delete messages after processing them  
- We can scale consumers horizontally to improve throughput of processing
## SQS-Security 
- **Encryption**:  
	- In-flight encryption using HTTPS API  
	- At-rest encryption using KMS keys  
	- Client-side encryption if the client wants to perform encryption/decryption itself  
- **Access Controls**: IAM policies to regulate access to the SQS API
- **SQS Access Policies** (similar to S3 bucket policies)  
	- Useful for cross-account access to SQS queues  
	- Useful for allowing other services (SNS, S3...) to write to an SQS queue
## SQS–Message-Visibility-Timeout  
- After a message is polled by a consumer, it becomes invisible to other consumers  
- By default, the “message visibility timeout” is 30 seconds  
- That means the message has 30 seconds to be processed  
- After the message visibility timeout is over, the message is “visible” in SQL
- If a message is not processed within the visibility timeout, it will be processed twice  
- A consumer could call the ChangeMessageVisibility API to get more time  
- If visibility timeout is high (hours), and consumer crashes, re processing will take time  
- If visibility timeout is too low (seconds), we may get duplicates
## Amazon-SQS–Dead-Letter-Queue
- If a consumer fails to process a message within the Visibility Timeout... the message goes back to the queue!  
- We can set a threshold of how many times a message can go back to the queue  
- After the MaximumReceives threshold is exceeded, the message goes into a dead letter queue (DLQ)
- Make sure to process the messages in the DLQ before they expire:  
	- Good to set a retention of 14 days in the DLQ
## SQS-DLQ–Redrive-to-Source
- When our code is fixed, we can redrive the messages from the DLQ back into the source queue (or any other queue) in batches without writing custom code.
![](https://i.imgur.com/s64AF89.png)
