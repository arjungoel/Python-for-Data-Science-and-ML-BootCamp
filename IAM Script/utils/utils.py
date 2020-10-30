import getpass
from boto3 import session
TEMP_SESSION_NAME = None
SESSION_DURATION_SECONDS = 3600


def get_aws_key_and_token(arn: str) -> dict:
    '''
    Generate credentials for the role and account specified in the argument "arn". Fails unless env variable "AWS_SHARED_CREDENTIALS_FILE" is valid.

    The Default section of "AWS_SHARED_CREDENTIALS_FILE" must have SSO account credentials. Otherwise this all falls apart.
    '''
    global TEMP_SESSION_NAME
    if TEMP_SESSION_NAME == None:
        TEMP_SESSION_NAME = get_user()
    getpass.getuser()
    sess = session.Session()
    # using creds from DEFAULT section of credentials file
    sts_connection = sess.client('sts')
    assume_role_object = sts_connection.assume_role(  # assume a new role in a new account based on the "arn" argument
        RoleArn=arn,
        RoleSessionName=TEMP_SESSION_NAME,
        DurationSeconds=SESSION_DURATION_SECONDS
    )
    return assume_role_object['Credentials']


def get_user():
    user = getpass.getuser()
    if len(user) < 4:
        user = input('what is your acf2 login user? ')
    return user + 'su'


def get_s3_client(role_arn):
    creds = get_aws_key_and_token(role_arn)
    boto3_session = session.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )
    return boto3_session.client('s3')


def get_iam_client(role_arn):
    creds = get_aws_key_and_token(role_arn)
    boto3_session = session.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )
    return boto3_session.client('iam')
