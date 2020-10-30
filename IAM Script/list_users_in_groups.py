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
header_csv = ['S_No', 'account_id', 'group_name']
S_No = 1

filename = "list_groups_user.csv"

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def list_users_in_groups():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_iam_client(
                f"arn:aws:iam::{account}:role/{MY_ROLE_NAME}")
            # to list groups
            groups = client.list_groups()
            for group_name in groups['Groups']:
                try:
                    get_group_name = client.get_group(
                        GroupName=groups['Groups'])
                    print(f"The groups in account are: {get_group_name}")
                    global S_No
                    writer.writerow([S_No, account, {get_group_name}])
                    S_No += 1
                except ClientError as e:
                    print("Users or Groups doesn't exist" + e)


if __name__ == "__main__":
    list_users_in_groups

file.close()
