import boto3
from utils.utils import get_ec2_client, get_accounts
from dataclasses import dataclass
import os
import sys
import csv

THIS_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT = os.path.dirname(THIS_DIR)
sys.path.append(ROOT)

regions = ['ap-northeast-1', 'ap-southeast-1',
           'ca-central-1', 'us-east-1', 'us-east-2']

# To create header of the file
header_csv = ['S_No', 'account_id', 'account_name', 'region', 'zone', 'azid']
S_No = 1

filename = "az_across_accounts.csv"

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)

MY_ROLE_NAME = input("Enter the assigned role:")
os.environ['AWS_SHARED_CREDENTIALS_FILE'] = "C:/Downloads/credentials"
ACCOUNT_NUMBER = input(
    "Enter the account id from where we can list all the AWS accounts that exists in the organizations:")


@ dataclass(init=True)
class EC2_AZ(object):
    print("script evaluating results")

    def describe_az(self) -> None:
        accounts = get_accounts(
            f"arn:aws:iam::{ACCOUNT_NUMBER}:role/{MY_ROLE_NAME}")
        for account, account_name in accounts.items():
            print("account: account_name")
            for region_val in regions:
                self.ec2_client = boto3.client(
                    'ec2', region_name=region_val)
                response = self.ec2_client.describe_availability_zones()
                for az in response['AvailabilityZones']:
                    region = az['RegionName']
                    # Availability Zones that have the same AZ IDs map to the same physical location.
                    zone = az['ZoneName']
                    az_id = az['ZoneId']
                    print(f"{region} with {zone} having zone id {az_id}")
                    global S_No
                    writer.writerow(
                        [S_No, account, account_name, region, zone, az_id])
                    S_No += 1


ec2 = EC2_AZ()
ec2.describe_az()
file.close()
