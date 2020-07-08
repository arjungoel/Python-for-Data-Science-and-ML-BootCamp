import boto3
from botocore.exceptions import ClientError
import csv
import os

regions = ['ca-central-1', 'us-east-1',
           'us-east-2', 'ap-northeast-1', 'ap-southeast-1']

# input the role name and taking the path of credentials file.
MY_ROLE_NAME = input("Enter the assigned role:")
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "C:/Downloads/credentials"

TEMP_SESSION_NAME = "my_temp_session"
SESSION_DURATION_SECONDS = 3600


class Boto3STSService(object):
    def __init__(self, arn):
        sess = boto3.session.Session()
        sts_connection = sess.client('sts')
        assume_role_object = sts_connection.assume_role(
            RoleArn=arn,
            RoleSessionName=TEMP_SESSION_NAME,
            DurationSeconds=SESSION_DURATION_SECONDS
        )
        self.credentials = assume_role_object['Credentials']


def get_s3_client(account):
    arn = f"arn:aws:iam::{account}:role/{MY_ROLE_NAME}"
    tmp_credentials = Boto3STSService(arn).credentials
    tmp_access_key = tmp_credentials['AccessKeyId']
    tmp_secret_key = tmp_credentials['SecretAccessKey']
    security_token = tmp_credentials['SessionToken']
    boto3_session = boto3.session.Session(
        aws_access_key_id=tmp_access_key,
        aws_secret_access_key=tmp_secret_key,
        aws_session_token=security_token
    )
    return boto3_session.client('s3')


# To create header of the file
header_csv = ['S_No', 'account_number', 'bucket_name', 'encryption_status']
S_No = 1

# to create dynamic filename
filename = input("Enter the filename:")  # (e.g. s3_bucket_encryption.csv)

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def s3_bucket_encryption():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_s3_client(account)

            response = client.list_buckets()
            for bucket in response['Buckets']:
                try:
                    enc = client.get_bucket_encryption(Bucket=bucket['Name'])
                    rules = enc['ServerSideEncryptionConfiguration']['Rules']
                    print(
                        f"Bucket is:{bucket['Name']} and Encryption status:{rules}")
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                        print(f"Bucket with no sse {bucket['Name']}")

                global S_No

                #print(S_No, bucket, rules)
                writer.writerow([S_No, account, bucket['Name'], rules])
                S_No += 1


def main():
    return s3_bucket_encryption()


if __name__ == "__main__":
    main()

file.close()
