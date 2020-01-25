import boto3

bucket_name = input("Enter the s3 bucket name:")
#account_number = input("Enter the Account Number:")
cost_centre = input("Enter the last cost centre:")

s3 = boto3.resource('s3')
bucket_tagging = s3.BucketTagging('bucket_name')

tags = bucket_tagging.put_bucket_tagging( Bucket=bucket,
        Tagging={
            'TagSet': [{'Key': str(k), 'Value': str(v)} for k, v in new_tags.items()]
        }
    ))
tags.append({'Key': 'cost_centre', 'Value':owner})
#Set_tag = bucket_tagging.put(Tagging={'TagSet':tags})
print(tag)
#print(Set_tag)
