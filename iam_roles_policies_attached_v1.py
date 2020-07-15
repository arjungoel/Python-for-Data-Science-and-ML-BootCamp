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


session = boto3.session.Session(profile_name=MY_ROLE_NAME)


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
            client = session.client('iam')
            paginator = client.get_paginator('list_roles')
            for page in paginator.paginate():
                try:
                    for role_name in page['Roles']:
                        list_of_policies_attached = client.list_attached_role_policies(
                            RoleName=role_name['RoleName'])
                        for policy in list_of_policies_attached['AttachedPolicies']:
                            print(
                                f"Role: {role_name['RoleName']} has policy: {policy['PolicyName']}")
                            global S_No

                            writer.writerow(
                                [S_No, account, role_name['RoleName'], policy['PolicyName']])
                            S_No += 1

                except ClientError as e:
                    print("Policy doesn't exist" + e)


def main():
    return iam_role_attached_policy()


if __name__ == "__main__":
    main()

file.close()
