import boto3
import csv
import os
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
    return boto3_session.client('lambda')


# To create header of the file
header_csv = ['S_No', 'func', 'vpcid']
S_No = 1

# to create dynamic filename
filename = input("Enter the filename:")  # (e.g. lambda_inside_vpc.csv)

file = open(filename, 'w', newline='\n')
writer = csv.writer(file, lineterminator='\n')
writer.writerow(header_csv)


def lambda_inside_vpc():
    with open('./aws_accounts.txt', mode="r") as file:
        for account_number in file:
            account = account_number.strip()
            if '*' in account or len(account) < 12:
                continue
            account = account[0:12]
            print(account)
            client = get_sts_client(account)
            response = client.list_functions()
            for function in response['Functions']:
                try:
                    func = client.get_function_configuration(
                        FunctionName=function['FunctionName'])
                    vpcid = func['VpcConfig']['VpcId']
                    if vpcid is not None:
                        print(
                            f"Function:{function['FunctionName']} and vpc: {vpcid}")
                    else:
                        print(function['FunctionName'])
                except KeyError:
                    print(
                        f"function not in vpc:{function['FunctionName']}")
                except ClientError as e:
                    print("[ERROR] Invoking Lambda Function" + e)

                global S_No

                #print(S_No, bucket, rules)
                writer.writerow([S_No, func, vpcid])
                S_No += 1


def main():
    return lambda_inside_vpc()


if __name__ == "__main__":
    main()

file.close()
