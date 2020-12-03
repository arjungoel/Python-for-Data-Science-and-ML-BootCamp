import getpass
from boto3 import session
TEMP_SESSION_NAME = None
SESSION_DURATION_SECONDS = 3600

def get_ec2_client(role_arn):
    creds = get_aws_key_and_token(role_arn)
    boto3_session = session.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )
    return boto3_session.client('ec2')


def get_accounts(role_arn) -> list:
    '''Appends all the accounts listed in operations into ACCOUNTS'''
    accounts = []
    creds = get_aws_key_and_token(role_arn)
    sess = session.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )
    accounts = {}
    org = sess.client('organizations')
    paginator = org.get_paginator('list_accounts')
    page_iterator = paginator.paginate()
    for page in page_iterator:
        for acct in page['Accounts']:
            accounts[acct['Id']] = acct['Name']
    return accounts
