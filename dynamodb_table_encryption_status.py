import boto3
import csv
import os
from botocore.exceptions import ClientError

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
    return boto3_session.client('dynamodb', region)


# To create header of the file
header_csv = ['S_No', 'account_id', 'table_name', 'key_arn']

# to create dynamic filename
filename = input("Enter the filename:")  # (e.g. dynamodb_encryption_type.csv)
file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def dynamodb_encryption_type():
    with open('./aws_accounts.txt', mode="r") as file:
        S_No = 1
        for account_number in file:
            account = account_number.strip()
            print(account_number)
            for region in regions:
                account = account_number.strip()
                if '*' in account or len(account) < 12:
                    continue
                account = account[0:12]
                client = get_sts_client(account, region)
                response = client.list_tables()
                try:
                    for table_name in response['TableNames']:
                        result = client.describe_table(
                            TableName=table_name
                        )
                        table_name = result['Table']['TableName']
                        if 'SSEDescription' in result['Table']:
                            encryption_type = result['Table']['SSEDescription']['SSEType']
                            arn = result['Table']['SSEDescription']['KMSMasterKeyArn']
                            print(
                                f"The table {table_name} has encryption type as {encryption_type} and the ARN is:{arn}")
                            writer.writerow(
                                [S_No, account, table_name, result['Table']['SSEDescription']['KMSMasterKeyArn']])
                            S_No += 1
                        else:
                            print(
                                f"The table {table_name} has encryption type as default and the KMS Master Key ARN is not applicable")
                            writer.writerow([S_No, account, table_name])
                            S_No += 1

                except ClientError as e:
                    print("Key Error" + e)


def main():
    return dynamodb_encryption_type()


if __name__ == "__main__":
    main()

file.close()
