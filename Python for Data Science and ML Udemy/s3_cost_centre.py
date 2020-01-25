import boto3

bucket_name = input("Enter the bucket name:")
account_number = input("Enter the account number:")

s3 = boto3.resource('s3')
bucket_tagging =s3.BucketTagging('bucket_name')
try:
    tag = bucket_tagging.put_bucket_tagging(
        Bucket=bucket,
        Tagging={
            'TagSet': [{'Key': str(k), 'Value': str(v)} for k, v in new_tags.items()]
        }
        )
        print(tag) 
else ClientError:
    print("There is an error")
