import boto3
from dotenv import load_dotenv
load_dotenv()
# Create an S3 client object
s3 = boto3.client('s3')

# Use the list_buckets method to get a list of all S3 buckets in your account
response = s3.list_buckets()

# Print the name of each bucket in the response
for bucket in response['Buckets']:
    print(bucket['Name'])
