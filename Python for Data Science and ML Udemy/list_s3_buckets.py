import boto3
iam = input("Enter the IAM user/role name")
# Executing code from local host that's why create a session
custom_session = boto3.session.Session(profile_name = "iam")
s3_resource = custom_session.resource('s3')    # using resource...
print("Using Resource Object:")
for each_bucket_info in s3_resource.buckets.all():
    print(each_bucket_info.name)

# using client object...

s3_client = custom_session.client('s3')
print("Using Client Object:")
paginator = s3_client.get_paginator('list_objects')
#for each_bucket_info in s3_client.list_buckets().get('Buckets'):
#    print(each_bucket_info.get('Name'))