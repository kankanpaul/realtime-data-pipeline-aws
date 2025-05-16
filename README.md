# Data Projection with AWS Stack

This project demonstrates the process of ingesting, transforming, analyzing, and visualizing data using a set of AWS services. The system is designed to capture changes in data from a DynamoDB table and process it in real time, storing the results in Amazon S3 for further analysis with AWS Athena and local data visualization.

![alt text]([path/to/your/image.jpg](https://github.com/kankanpaul/realtime-data-pipeline-aws/blob/main/DE%20architecture%20diagram.png))


## Stack Overview

- **Python Mock Generator Script**: Generates mock data to populate the DynamoDB table.
- **DynamoDB**: A NoSQL database to store user profiles.
- **DynamoDB Streams**: Captures real-time changes (updates and deletions) to DynamoDB records.
- **Kinesis Stream**: Used to ingest real-time data changes from DynamoDB Streams.
- **EventBridge Pipe**: Connects DynamoDB to the Kinesis stream.
- **Kinesis Firehose**: Batches and stores the stream data in S3.
- **Lambda**: Used for transforming the streaming data before sending it to S3.
- **Athena**: A query service to analyze the data stored in S3.
- **S3**: Used for storing the raw streaming data and query results.

## Steps Followed

### 1. **Mock Data Generation**
   - A Python script was written to generate mock data for user profiles.
   - The mock data contains the following fields: `id`, `name`, `email`, `phone_number`, `created_at`, `age`, `address`.

### 2. **DynamoDB Table Setup**
   - A DynamoDB table named `user-profiles` was created to store the mock user data. The table uses `id` as the partition key.
   - DynamoDB Streams were enabled on the table to capture changes in the records (insert, update, delete).

### 3. **Enable DynamoDB Stream**
   - DynamoDB Streams were turned on to capture changes as they happen to the records in the `user-profiles` table.

### 4. **Kinesis Stream Setup**
   - A Kinesis stream (`kinesis-user-profiles`) was created to listen to the DynamoDB changes.
   - The Kinesis stream listens to the DynamoDB stream and ingests the records in real-time.

### 5. **EventBridge Pipe for Stream Ingestion**
   - An EventBridge pipe was created to connect DynamoDB to the Kinesis stream. This ensures that the records captured in DynamoDB are pushed to the Kinesis stream seamlessly.
   - The partition key was set to `eventID` to ensure that each shard in the stream receives different data.

### 6. **Kinesis Firehose for Batching Data**
   - The data from the Kinesis stream is sent to Kinesis Firehose for batching.
   - Firehose batches the streaming data and writes it to an S3 bucket.

### 7. **Transform Data Using Lambda**
   - A Lambda function was used to transform the data before sending it to the S3 bucket. The transformation step could involve parsing, cleaning, or aggregating the data, depending on the requirements.

### 8. **Data Stored in S3**
   - After processing, the data is stored in an S3 bucket in its raw form. A separate folder is created to store the query results.

### 9. **Crawler and JSON Classifier in Athena**
   - An AWS Glue Crawler was created to crawl the S3 bucket, using a custom JSON classifier path for the JSON data stored in S3.
   - The crawler classifies the data into a readable format for Athena.

### 10. **Athena for Querying Data**
   - After the data is classified, you can run SQL queries on it using **AWS Athena**.
   - Example queries were provided to analyze the data, such as finding users based on their age, counting users by city, and analyzing missing or invalid emails.

### 11. **Visualization Using Local Tools**
   - The data from S3 was exported and analyzed locally using Python libraries such as **matplotlib** and **seaborn** for visualization.
   - Basic visualizations like histograms and bar charts were created to analyze the distribution of user profiles.

## Technologies Used

- **Python**: For generating mock data and visualizing results.
- **AWS DynamoDB**: NoSQL database for storing user profiles.
- **AWS Kinesis**: For real-time stream processing.
- **AWS Lambda**: For data transformation.
- **AWS EventBridge**: For event-driven stream ingestion.
- **AWS Firehose**: For batch processing of streaming data.
- **AWS S3**: Storage for raw and transformed data.
- **AWS Glue**: Crawler for data classification.
- **AWS Athena**: Querying and analyzing data stored in S3.
- **matplotlib & seaborn**: Local Python libraries for creating visualizations.


