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
              'role_name', 'role_managed_policy', 'role_policy_arn', 'role_policy_version', 'role_inline_policy']
S_No = 1

filename = "iam_role_policies.csv"

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def list_iam_role_policies():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_iam_client(
                f"arn:aws:iam::{account}:role/{MY_ROLE_NAME}")
            paginator = client.get_paginator('list_roles')
            for page in paginator.paginate():
                try:
                    for role_name in page['Roles']:
                        print(role_name)
                        # to list customer managed policies
                        list_of_managed_policies = client.list_attached_role_policies(
                            RoleName=role_name['RoleName'])
                        # to list inline policies
                        list_of_inline_policies = client.list_role_policies(
                            RoleName=role_name['RoleName'])
                        # merging output of managed and inline policies
                        list_of_role_policies = {**list_of_managed_policies,
                                                 **list_of_inline_policies}
                        # to list managed policy versions for roles
                        for policy in list_of_managed_policies['AttachedPolicies']:
                            versions = client.list_policy_versions(
                                PolicyArn=policy['PolicyArn'])
                            for version_number in versions['Versions']:
                                # get policy version for IAM role
                                get_policy_version_role = client.get_policy_version(
                                    PolicyArn=policy['PolicyArn'], VersionId=version_number['VersionId'])
                        for policy_name in list_of_role_policies['AttachedPolicies']:
                            list_entities = client.list_entities_for_policy(
                                PolicyArn=policy['PolicyArn'])
                            print(list_entities)
                            print(
                                f"Role {role_name['RoleName']} is having managed policies {policy_name['PolicyName']} with ARN {policy_name['PolicyArn']} with version id {get_policy_version_role} and is having inline policies {list_of_role_policies['PolicyNames']}")
                            global S_No

                            writer.writerow(
                                [S_No, account, role_name['RoleName'], policy['PolicyName'], policy_name['PolicyArn'], get_policy_version_role, list_of_role_policies['PolicyNames']])
                            S_No += 1
                except ClientError as e:
                    print("Roles and Policies doesn't exist" + e)


if __name__ == "__main__":
    list_iam_role_policies()

file.close()
