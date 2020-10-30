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
              'role_name', 'list_entities']
S_No = 1

filename = "iam_list_entities.csv"

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def list_iam_entities():
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
                    for role in page['Roles']:
                        list_of_managed_policies = client.list_attached_role_policies(
                            RoleName=role['RoleName'])
                        for managed_policy in list_of_managed_policies['AttachedPolicies']:
                            list_entities = client.list_entities_for_policy(
                                PolicyArn=managed_policy['PolicyArn'])
                            global S_No
                            writer.writerow(
                                [S_No, account, role['RoleName'], list_entities])
                            S_No += 1
                except ClientError as e:
                    print("Entities doesn't exist" + e)


if __name__ == "__main__":
    list_iam_entities()

file.close()
