import boto3
from botocore.exceptions import ClientError
import csv
import os

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


def get_sts_client(account):
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
    return boto3_session.client('iam')


# To create header of the file
header_csv = ['S_No', 'account_id', 'role_name', 'policy']
S_No = 1

# to create dynamic filename
filename = input("Enter the filename:")  # (e.g. iam_role_policies.csv)

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def iam_role_attached_policy():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_sts_client(account)
            paginator = client.get_paginator('list_roles')
            for page in paginator.paginate():
                try:
                    for role_name in page['Roles']:
                        list_of_policies_attached = client.list_attached_role_policies(
                            RoleName=role_name['RoleName'])
                        for name in list_of_policies_attached['AttachedPolicies']:
                            print(
                                f"Role {role_name['RoleName']} has policy {name['PolicyName']}")
                            global S_No

                            writer.writerow(
                                [S_No, account, role_name['RoleName'], name['PolicyName']])
                            S_No += 1

                except ClientError as e:
                    print("Policy doesn't exist" + e)


def main():
    return iam_role_attached_policy()


if __name__ == "__main__":
    main()

file.close()
