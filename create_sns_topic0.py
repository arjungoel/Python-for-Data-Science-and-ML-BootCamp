import boto3
from botocore.exceptions import ClientError

account_number = input("Enter the account number:")
region = input ("Enter the name of the region:")
sns_topic_name = input("Enter the name of SNS topic:")


# to create an array of topics
topics = []

# Create an SNS Client
conn = boto3.client("sns", region_name=region)
conn.create_topic(Name=sns_topic_name)
try:
    if (sns_topic_name == topics ):
        topics.append(sns_topic_name)
except ClientError:
    print ("There is an error")