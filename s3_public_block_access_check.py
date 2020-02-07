import boto3
from botocore.exceptions import ClientError

account_number = input("Enter the account number:")

# optional as s3 is a global service..
#region = input("Name the region in which bucket exists:")  

s3_client = boto3.client('s3')

#list of empty array...
buckets = []


def check_public_access_s3(bucket_name):
    public_block = s3_client.put_public_access_block(Bucket=bucket_name,
                                                     PublicAccessBlockConfiguration={
                                                         'BlockPublicAcls': True,
                                                         'IgnorePublicAcls': True,
                                                         'BlockPublicPolicy': True,
                                                         'RestrictPublicBuckets': True
                                                     })
    if (public_block == True):
        buckets.append(bucket_name)

    enableacl = s3_client.put_bucket_acl(Bucket=bucket_name,
                                         ACL='private'
                                         )
try:
    for each_bucket_info in s3_client.list_buckets().get('Buckets'):
        print(each_bucket_info.get('Name'))
        check_public_access_s3(each_bucket_info.get('Name'))
except ClientError:
    print("Enable Block Public Access")