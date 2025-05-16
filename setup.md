# AWS Data Pipeline Setup Guide

## 1. **Mock Data Generation**

This will generate mock data and can be inserted into DynamoDB.

python mock_data_generator.py
---

## 2. **DynamoDB Table Setup**

### Create DynamoDB Table:

1. Go to the DynamoDB service in the AWS console and create a new table.
2. Set the table name to `user-profiles`.
3. Set the **Partition Key** to `id` (string type).

### Enable DynamoDB Streams:

1. In the table settings, enable **DynamoDB Streams**. This will allow us to capture changes made to the DynamoDB table in real-time (inserts, updates, deletes).
2. Choose **New image** for stream view type (captures the state of the record after modification).

---

## 3. **Kinesis Stream Setup**

### Create Kinesis Stream:

1. Go to the **Kinesis** service in the AWS console and create a new stream.
2. Name the stream `kinesis-user-profiles`.
3. This stream will receive the change records from DynamoDB via the **EventBridge Pipe**.

---

## 4. **EventBridge Pipe Setup**

### Create EventBridge Pipe:

1. Go to the **EventBridge** service in the AWS console.
2. Create a new **EventBridge Pipe** to connect DynamoDB Streams to the Kinesis stream (`kinesis-user-profiles`).
3. Set the **Source** to DynamoDB Streams and the **Target** to the Kinesis stream.
4. Set the **Partition Key** to `eventID` to ensure that each shard receives different data.

---

## 5. **Kinesis Firehose for Data Batching**

### Create Kinesis Firehose Delivery Stream:

1. Go to the **Kinesis** service and create a new Firehose delivery stream.
2. Name the stream `kinesis-firehose-stream`.
3. Set the destination to **Amazon S3** to store batched data.
4. Set up the **S3 bucket** in your AWS account to store the data. You can create a new bucket or use an existing one.
5. This will batch and store streaming data into the S3 bucket.

---

## 6. **Lambda Function for Data Transformation**

### Create a Lambda Function:

1. Go to the **Lambda** service in the AWS console and create a new Lambda function.
2. Set up the function to trigger on the Kinesis Firehose stream and perform any necessary data transformation (such as cleaning or parsing).
3. The Lambda function should output the transformed data into the S3 bucket.

**Note**: For simplicity, if you're not performing transformations, you can skip Lambda and directly use Firehose to write to S3.

---

## 7. **S3 Bucket Setup**

### Create S3 Bucket:

1. Create an **S3 bucket** where data will be stored. You can either create a new bucket or use an existing one.
2. The bucket will store both the raw data from Kinesis Firehose and the transformed data.

### Create Folder for Athena Queries:

1. Inside the S3 bucket, create a folder to store the results of Athena queries. For example: `athena-queries/`.

---

## 8. **AWS Glue Crawler Setup**

### Create a Glue Crawler:

1. Go to the **AWS Glue** service and create a new crawler.
2. Set the data store to **S3** and point it to the S3 bucket where the raw data from Kinesis Firehose is stored.
3. Create a **JSON classifier** for the data (this is required to classify the incoming JSON data).
4. Set up the crawler to output the metadata to a new Glue database, for example: `dynamo-kinesis-lambda-catalog`.

### Run the Crawler:

1. Run the Glue Crawler to create a table based on the incoming data.
2. The crawler will classify the data and make it available for querying in **Athena**.

---

## 9. **Athena Setup**

### Create an Athena Table:

1. Go to the **Athena** service in the AWS console.
2. Ensure that the S3 bucket is linked to Athena so you can run queries on the data stored in S3.
3. Use the Glue database (`dynamo-kinesis-lambda-catalog`) created by the crawler to create a table for querying the data.

---

## Data Visualization with Python

### Python Script Example

To analyze and visualize data locally using **pandas**, **seaborn**, and **matplotlib**, you can use the following script:

```python
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load data (assume data is in CSV format for simplicity)
data = pd.read_csv("path_to_your_data.csv")

# Create a simple visualization
sns.histplot(data['age'])
plt.title("Age Distribution")
plt.show()

