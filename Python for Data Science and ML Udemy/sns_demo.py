import boto3

account_number = input("Enter the account number:") 
iam_user = input("Enter the IAM user name") 

custom_session = boto3.session.Session(profile_name= iam_user)
sns_resoure = custom_session.resource("sns", region="ca-central-1")
