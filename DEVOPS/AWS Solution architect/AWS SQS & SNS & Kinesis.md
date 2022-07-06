# Navigation
- [**SQS–Standard Queue**](#SQS–Standard%20Queue)
	- [SQS–Producing-Messages](#SQS–Producing-Messages)
	- [SQS–Consuming-Messages](#SQS–Consuming-Messages)
	- [SQS–Multiple-EC2-Instances-Consumers](#SQS–Multiple-EC2-Instances-Consumers)
	- [SQS-Security](#SQS-Security)
	- [SQS–Message-Visibility-Timeout](#SQ%20–Message-Visibility-Timeout)
	- [Amazon-SQS–Dead-Letter-Queue](#Amazon-SQS–Dead-Letter-Queue)
	- [SQS-DLQ–Redrive-to-Source](#SQS-DLQ–Redrive-to-Source)
	- [Amazon-SQS–Delay Queue](#Amazon-SQS–Delay%20Queue)
	- [Amazon-SQS-Long-Polling](#Amazon-SQS-Long-Polling)
	- [Amazon-SQS–FIFO-Queue](#Amazon-SQS–FIFO-Queue)
- [**Kinesis-Overview**](#Kinesis-Overview)
	- [Kinesis-Data-Streams](#Kinesis-Data-Streams)
	- [Kinesis-Data-Firehose](#Kinesis-Data-Firehose)
	- [Kinesis-Data-Streams-vs-Firehose](#Kinesis-Data-Streams-vs-Firehose)
	- [Kinesis-Data-Analytics- SQL application](#Kinesis-Data-Analytics-%20SQL%20application)
# SQS–Standard-Queue
- Fully managed service, used to decouple applications
- **Attributes**:  
	- Unlimited throughput, unlimited number of messages in queue  
	- Default retention of messages: 4 days, maximum of 14 days  
	- Low latency (<10 ms on publish and receive)  
	- Limitation of 256KB per message sent  
	- Can have duplicate messages (at least once delivery, occasionally)  
	- Can have out of order messages (best effort ordering)
![](https://i.imgur.com/a46UVxx.png)
## SQS–Producing-Messages
- Produced to SQS using the SDK (SendMessage API)  
- The message is persisted in SQS until a consumer deletes it  
- Message retention: default 4 days, up to 14 day
- SQS standard: unlimited throughput
- **Example: send an order to be processed**  
	- Order id  
	- Customer id  
	- Any attributes you want
## SQS–Consuming-Messages  
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

## Amazon-SQS–Delay Queue  
- Delay a message (consumers don’t see it immediately) up to 15 minutes  
- Default is 0 seconds (message is available right away)  
- Can set a default at queue level  
- Can override the default on send using the DelaySeconds parameter
## Amazon-SQS-Long-Polling  
- When a consumer requests messages from the queue, it can optionally “wait” for messages to arrive if there are none in the queue  
- This is called Long Polling  
- LongPolling decreases the number of API calls made to SQS while increasing the efficiency and reducing latency of your application  
- The wait time can be between 1 sec to 20 sec (20 sec preferable)  
- Long Polling is preferable to Short Polling  
- Long polling can be enabled at the queue level or at the API level using WaitTimeSeconds
## Amazon-SQS–FIFO-Queue  
- FIFO = First In First Out (ordering of messages in the queue)
- Limited throughput: 300 msg/s without batching, 3000 msg/s with  
- Exactly-once send capability (by removing duplicates)  
- Messages are processed in order by the consumer 
# Kinesis-Overview  
- Makes it easy to collect, process, and analyze streaming data in real-time
- Ingest real-time data such as: Application logs, Metrics, Website clickstreams, IoT telemetry data...  
- **Kinesis Data Streams**: capture, process, and store data streams  
- **Kinesis Data Firehose**: load data streams into AWS data stores  
- **Kinesis Data Analytics**: analyze data streams with SQL or Apache Flink  
- **Kinesis Video Streams**: capture, process, and store video streams
## Kinesis-Data-Streams
- Retention between 1 day to 365 days  
- Ability to reprocess (replay) data  
- Once data is inserted in Kinesis, it can’t be deleted (immutability)  
- Data that shares the same partition goes to the same shard (ordering)  
- Producers: AWS SDK, Kinesis Producer Library (KPL), Kinesis Agent  
- **Consumers**:  
	- Write your own: Kinesis Client Library (KCL), AWS SDK  
	- Managed: AWS Lambda, Kinesis Data Firehose, Kinesis Data Analytics
- **Provisioned mode**:  
	- You choose the number of shards provisioned, scale manually or using API  
	- Each shard gets 1MB/s in (or 1000 records per second)  
	- Each shard gets 2MB/s out (classic or enhanced fan-out consumer)  
	- You pay per shard provisioned per hour  
- **On-demand mode**:  
	- No need to provision or manage the capacity  
	- Default capacity provisioned (4 MB/s in or 4000 records per second)  
	- Scales automatically based on observed throughput peak during the last 30 days  
	- Pay per stream per hour & data in/out per GB
## Kinesis-Data-Firehose
- Fully Managed Service, no administration, automatic scaling, serverless  
	- AWS: Redshift / Amazon S3 / ElasticSearch  
	- 3rd party partner: Splunk / MongoDB / DataDog / NewRelic / ...  
	- Custom: send to any HTTP endpoint  
- Pay for data going through Firehose  
- **Near Real Time**  
	- 60 seconds latency minimum for non full batches  
	- Or minimum 32 MB of data at a time  
- Supports many data formats, conversions, transformations, compression  
- Supports custom data transformations using AWS Lambda  
- Can send failed or all data to a backup S3 bucket
# Kinesis-Data-Streams-vs-Firehose
![](https://i.imgur.com/4R8M3ZH.png)
# Kinesis-Data-Analytics-(SQL-application)
- Perform real-time analytics on Kinesis Streams using SQL  
- Fully managed, no servers to provision  
- Automatic scaling  
- Real-time analytics  
- Pay for actual consumption rate  
- Can create streams out of the real-time queries  
- **Use cases**:  
	- Time-series analytics  
	- Real-time dashboards  
	- Real-time metrics
# Kinesis-vs-SQS-ordering
- Let’s assume 100 trucks, 5 kinesis shards, 1 SQS FIFO  
- **Kinesis Data Streams**:  
	- On average you’ll have 20 trucks per shard  
	- Trucks will have their data ordered within each shard  
	- The maximum amount of consumers in parallel we can have is 5  
	- Can receive up to 5 MB/s of data  
- **SQS FIFO**  
	- You only have one SQS FIFO queue  
	- You will have 100 Group ID  
	- You can have up to 100 Consumers (due to the 100 Group ID)  
	- You have up to 300 messages per second (or 3000 if using batching
# Amazon-SNS
- Send one message to many receivers
- The “event producer” only sends message to one SNS topic  
- As many “event receivers” (subscriptions) as we want to listen to the SNS topic notifications  
- Each subscriber to the topic will get all the messages (note: new feature to filter messages)  
- Up to 12,500,000 subscriptions per topic  
- 100,000 topics limit
- Security same as [**SQS-Security**](#SQS-Security)
## Amazon-SNS–FIFO Topic
- FIFO = First In First Out (ordering of messages in the topic)
- Similar features as SQS FIFO:  
- Ordering by Message Group ID (all messages in the same group are ordered)  
- Deduplication using a Deduplication ID or Content Based Deduplication  
- **Can only have SQS FIFO queues as subscribers**  
- Limited throughput (same throughput as SQS FIFO)
## SNS–Message-Filtering
- JSON policy used to filter messages sent to SNS topic’s subscriptions  
- If a subscription doesn’t have a filter policy, it receives every message
# Amazon-MQ
- Traditional applications running from on-premises may use open protocols such as: MQTT, AMQP, STOMP, Openwire, WSS  
- When migrating to the cloud, instead of re-engineering the application to use SQS and SNS, we can use Amazon MQ  
- Amazon MQ = managed Apache ActiveMQ  
- Amazon MQ doesn’t “scale” as much as SQS / SNS  
- Amazon MQ runs on a dedicated machine, can run in HA with failover  
- Amazon MQ has both queue feature (~SQS) and topic features (~SNS)
# Summary
![](https://i.imgur.com/DBVyHSn.png)