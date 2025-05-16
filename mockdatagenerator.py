import boto3
from faker import Faker
import random
import uuid
import time

# --- Configuration ---
DYNAMODB_TABLE_NAME = ''  #USe own table 
AWS_REGION = ''         #Use the region     
STREAM_INTERVAL_SECONDS = 3  #Put any number you want         

# --- AWS Credentials ---
#Note can save creds in env variable or aws secrets manager
AWS_ACCESS_KEY_ID = '' #Use the AWS credentials
AWS_SECRET_ACCESS_KEY = '' #Use the AWS credentials

# --- Initialize AWS and Faker ---
dynamodb = boto3.resource(
    'dynamodb',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)
table = dynamodb.Table(DYNAMODB_TABLE_NAME)
fake = Faker()

# --- Helper to generate email from name ---
def generate_email_from_name(name):
    first_name = name.split()[0].lower()
    last_name = name.split()[-1].lower()
    domain = random.choice(['example.com', 'mailhub.net', 'userdata.org'])
    return f"{first_name}.{last_name}@{domain}"

# --- Generate one item ---
def generate_mock_item():
    name = fake.name()
    email = generate_email_from_name(name)

    return {
        'id': str(uuid.uuid4()),            # Primary key
        'name': name,
        'email': email,
        'created_at': fake.iso8601(),
        'age': random.randint(18, 80),
        'address': fake.address(),
        'phone_number': fake.phone_number(),
    }

# --- Continuous Insertion Loop ---
def stream_data():
    print(f"Starting real-time mock data stream into '{DYNAMODB_TABLE_NAME}' (every {STREAM_INTERVAL_SECONDS}s)...\n")
    try:
        while True:
            item = generate_mock_item()
            table.put_item(Item=item)
            print(f"✔️ Inserted: {item['id']} ({item['email']}) at {item['created_at']}")
            time.sleep(STREAM_INTERVAL_SECONDS)
    except KeyboardInterrupt:
        print("\n⏹️ Stream stopped by user.")

# --- Main Execution ---
if __name__ == "__main__":
    stream_data()
