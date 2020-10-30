from utils.utils import get_iam_client
import boto3
from botocore.exceptions import ClientError
import csv
import os
import sys

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(THIS_DIR)
sys.path.append(ROOT)


# input the role name and taking the path of credentials file.
MY_ROLE_NAME = input("Enter the assigned role:")
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "C:/Downloads/credentials"


# To create header of the file
header_csv = ['S_No', 'account_id',
              'user_name', 'user_managed_policy', 'user_policy_arn', 'user_policy_version', 'user_inline_policy']
S_No = 1

filename = "iam_user_policies.csv"

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def list_iam_user_policies():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_iam_client(
                f"arn:aws:iam::{account}:role/{MY_ROLE_NAME}")
            paginator = client.get_paginator('list_users')
            for page in paginator.paginate():
                try:
                    for user_name in page['Users']:
                        # to list managed policies
                        list_of_managed_policies = client.list_attached_user_policies(
                            UserName=user_name['UserName'])
                        # to list inline policies
                        list_of_inline_policies = client.list_user_policies(
                            UserName=user_name['UserName'])
                        # merging output of managed and inline policies
                        list_of_user_policies = {**list_of_managed_policies,
                                                 **list_of_inline_policies}
                        # to list managed policy versions for roles
                        for policy in list_of_managed_policies['AttachedPolicies']:
                            versions = client.list_policy_versions(
                                PolicyArn=policy['PolicyArn'])
                            for version_number in versions['Versions']:
                                # get policy version for IAM role
                                get_policy_version_user = client.get_policy_version(
                                    PolicyArn=policy['PolicyArn'], VersionId=version_number['VersionId'])
                        for policy_name in list_of_user_policies['AttachedPolicies']:
                            print(
                                f"User {user_name['UserName']} is having managed policies {policy_name['PolicyName']} with version id  {get_policy_version_user} and is having inline policies {list_of_user_policies['PolicyNames']}")
                            global S_No

                            writer.writerow(
                                [S_No, account, user_name['UserName'], policy['PolicyName'], policy_name['PolicyArn'], get_policy_version_user, list_of_user_policies['PolicyNames']])
                            S_No += 1
                except ClientError as e:
                    print("Roles and Policies doesn't exist" + e)


if __name__ == "__main__":
    list_iam_user_policies()

file.close()
