import os
import boto3
import csv
import logging
from pprint import pprint
from botocore.exceptions import ClientError

aws_regions = ["ap-northeast-1", "ap-southeast-1",
               "ca-central-1", "us-east-1", "us-east-2"]


# To generate Temporary Credentials
MY_ROLE_NAME = input("Enter the assigned role:")
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = r"C:\Downloads\credentials"


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
    logging.info(arn)
    tmp_credentials = Boto3STSService(arn).credentials
    tmp_access_key = tmp_credentials['AccessKeyId']
    tmp_secret_key = tmp_credentials['SecretAccessKey']
    security_token = tmp_credentials['SessionToken']
    boto3_session = boto3.session.Session(
        aws_access_key_id=tmp_access_key,
        aws_secret_access_key=tmp_secret_key,
        aws_session_token=security_token
    )
    return boto3_session


# To create header of the file
header_csv = ['S_No', 'Account', 'Region', 'InstanceId', 'InstanceType', 'AttachmentId', 'ENIStatus', 'NetworkInterfaceId',
              'SubnetId', 'VpcId', 'AvailabilityZone', 'PrivateIpAddress']
filename = "eni_service_details.csv"
file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def eni_details():
    with open('./aws_accounts.txt', mode="r") as file:
        S_No = 0
        for account_number in file:
            account = account_number.strip()
            for region in aws_regions:
                account = account_number.strip()
                if '*' in account or len(account) < 12:
                    continue
                account = account[0:12]
                print("getting details for ENI on account" + " " +
                      account + " on region " + region)
                boto3Session = get_sts_client(account, region)
                ec2 = boto3Session.client('ec2', region)
                instance = ec2.describe_instances()
                response = ec2.describe_network_interfaces()
                try:
                    for params in instance['Reservations']:
                        for param in params['Instances']:
                            instance_id = param['InstanceId']
                            instance_type = param['InstanceType']
                    for network_interface in response['NetworkInterfaces']:
                        if 'Attachment' in network_interface:
                            attachment_id = network_interface['Attachment']['AttachmentId']
                            eni_status = network_interface['Attachment']['Status']
                            network_interface_id = network_interface['NetworkInterfaceId']
                            subnet_id = network_interface['SubnetId']
                            vpc_id = network_interface['VpcId']
                            if 'AvailabilityZone' in network_interface:
                                availability_zone = network_interface['AvailabilityZone']
                            for ip_addresses in network_interface['PrivateIpAddresses']:
                                private_ip_address = ip_addresses['PrivateIpAddress']

                            # stores output in the csv file
                            S_No += 1
                            list_params = [S_No, account,
                                           region, instance_id, instance_type, attachment_id, eni_status, network_interface_id, subnet_id, vpc_id, availability_zone, private_ip_address]
                            writer.writerow(list_params)
                except ClientError as e:
                    print("Instance doesn't exist" + e)


def main():
    return eni_details()


if __name__ == "__main__":
    main()
