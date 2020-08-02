import boto3
from botocore.exceptions import ClientError
import csv
import os
import json

regions = ['ap-northeast-1', 'ap-southeast-1',
           'ca-central-1', 'us-east-1', 'us-east-2']

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


def get_sts_client(account, region):
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
    return boto3_session.client('sqs', region)


# To create header of the file
header_csv = ['S_No', 'account_id', 'queue_name', 'tags']
S_No = 1

# to create dynamic filename
filename = input("Enter the filename:")  # (e.g. sqs_tags.csv)

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def sqs_queue_tags():
    with open('./aws_accounts.txt', mode="r") as file:
        S_No = 1
        for account_number in file:
            print(account_number)
            for region in regions:
                account = account_number.strip()
                if '*' in account or len(account) < 12:
                    continue
                account = account[0:12]
                client = get_sts_client(account, region)
                try:
                    if 'QueueUrls' in client.list_queues():
                        for url in client.list_queues()['QueueUrls']:
                            if 'Tags' in client.list_queue_tags(QueueUrl=url):
                                print(
                                    f"The queue {url.rsplit('/', 1)[1]} have tags {client.list_queue_tags(QueueUrl=url)['Tags']}")
                                writer.writerow(
                                    [S_No, account, url.rsplit('/', 1)[1], client.list_queue_tags(QueueUrl=url)['Tags']])
                                S_No += 1
                            else:
                                print(
                                    f" The queue {url.rsplit('/', 1)[1]} have no tags")
                                writer.writerow(
                                    [S_No, account, url.rsplit('/', 1)[1]])
                                S_No += 1

                except ClientError as e:
                    print("queue doesn't exist error" + e)


def main():
    return sqs_queue_tags()


if __name__ == "__main__":
    main()
