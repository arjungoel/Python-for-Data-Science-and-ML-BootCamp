#!/usr/bin/env python
import boto3
import csv
import os

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
    return boto3_session.client('cloudformation')


# To create header of the file
header_csv = ['S_NO', 'STACK_NAME', 'STACK_TERMINATION_PROTECTION_STATUS',
              'STACK_TAGS', 'DISABLE_ROLLBACK', 'STACK_DRIFT_INFO', 'STACK_STATUS']
S_NO = 1

# to create dynamic filename
filename = input("Enter the filename:")

# To store the attributes of the CloudFormation Stack
file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def cf_list_attributes():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_sts_client(account)
            for region_val in regions:
                # custom session
                session = boto3.session.Session()
                resource = session.resource(
                    service_name='cloudformation', region_name=region_val)

                # To list cloudformation stacks in a region in a given account
                for each_stack in resource.stacks.all():
                    STACK_NAME = each_stack.stack_name
                    STACK_TERMINATION_PROTECTION_STATUS = each_stack.enable_termination_protection
                    STACK_TAGS = each_stack.tags
                    DISABLE_ROLLBACK = each_stack.disable_rollback
                    STACK_DRIFT_INFO = each_stack.drift_information
                    STACK_STATUS = each_stack.stack_status

                    global S_NO

                    print(S_NO, STACK_NAME, STACK_TERMINATION_PROTECTION_STATUS,
                          STACK_TAGS, DISABLE_ROLLBACK, STACK_DRIFT_INFO, STACK_STATUS)
                    writer.writerow([S_NO, STACK_NAME, STACK_TERMINATION_PROTECTION_STATUS,
                                     STACK_TAGS, DISABLE_ROLLBACK, STACK_DRIFT_INFO, STACK_STATUS])
                    S_NO += 1


if __name__ == "__main__":
    cf_list_attributes()

file.close()
