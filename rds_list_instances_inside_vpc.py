import boto3
import os
import csv
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
    return boto3_session.client('rds')


# To create header of the file
header_csv = ['S_No', 'identifier_name', 'vpcid']
S_No = 1

# to create dynamic filename
filename = input("Enter the filename:")  # (e.g. rds_inside_vpc.csv)

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def rds_inside_vpc():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_sts_client(account)
            response = client.describe_db_instances()
            for instance in response['DBInstances']:
                try:
                    identifier_name = instance['DBInstanceIdentifier']
                    subnet_group = client.describe_db_subnet_groups()
                    subnet_group_name = subnet_group['DBSubnetGroups']
                    for identifier_name, vpcid in enumerate(subnet_group_name):
                        if vpcid is not None:
                            print(
                                f"The rds identifier is:{instance['DBInstanceIdentifier']} and it belongs to subnet group: {vpcid['DBSubnetGroupName']} and it is in vpc: {vpcid['VpcId']}")
                        else:
                            print(
                                f"The rds identifier is:{instance['DBInstanceIdentifier']} and it belongs to subnet group: {vpcid['DBSubnetGroupName']}")
                except ClientError as e:
                    print("DB Subnet Group Name Error" + e)

                global S_No

                writer.writerow(
                    [S_No, instance['DBInstanceIdentifier'], vpcid['VpcId']])
                S_No += 1


def main():
    return rds_inside_vpc()


if __name__ == "__main__":
    main()

file.close()
