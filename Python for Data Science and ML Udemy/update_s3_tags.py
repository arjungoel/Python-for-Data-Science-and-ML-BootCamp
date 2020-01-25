import boto3
from botocore.exceptions import ClientError
bucket_name = input("Enter the Bucket Name:")
bucket_cost_centre = input("Enter the Bucket cost center : ")
bucket_tagging = boto3.client('s3')
try:
    tag_set = bucket_tagging.get_bucket_tagging(Bucket=bucket_name)
    #print(tag_set['TagSet'])
    #print()
    for tag in tag_set['TagSet'] :
        if tag['Key'] == 'cost_center':
            tag['Value'] = bucket_cost_centre
            response = bucket_tagging.put_bucket_tagging(
                Bucket=bucket_name,
                Tagging={
                    'TagSet': tag_set['TagSet']
                }
            )
    tag_set = bucket_tagging.get_bucket_tagging(Bucket=bucket_name)
    print()
    print(tag_set['TagSet'])


except ClientError:
        print(bucket_name + ",does not have tags, add tag")
# s3-bucket-example-test001