import boto3
from botocore.exceptions import ClientError

client = boto3.client(service_name='s3')
response = client.list_buckets()

# list s3 buckets and the tags associated with the bucket
for bucket in response['Buckets']:
    try:
        result = client.get_bucket_tagging(
            Bucket=bucket['Name']
            )
        value = result['TagSet']
        for tags in value:
            print(f"The bucket name is: {bucket['Name']} and the tags are: {tags['Key']}:{tags['Value']}")
    except ClientError as e:
        if e.response['Error']['Code'] == 'TagSetNotFoundError':
            print("TagSet Not Found Error" + e)
        else:
            print(f"The bucket name is: {bucket['Name']} has no tags")

# replace wrong tag with the right tag key
for bucket in response['Buckets']:
    if tags['Key'] in ('cost_center', 'costcenter', 'costcentre', 'cost_Center', 'cost_Centre'):
        update_tag = client.put_bucket_tagging(
            Bucket=bucket['Name'],
            Tagging={
                'TagSet': [
                    {
                        'Key': 'cost_centre',
                        'Value': tags['Value']
                    }
                ]
            }
        )
