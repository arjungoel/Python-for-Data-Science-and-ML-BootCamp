# To check whether the CF termination status is enabled/not.

import boto3
from botocore.exceptions import ClientError

account_number = input("Enter the account number:")
region = ("Enter the region:")
stack_name = input("Enter the CF template/stack name:")


cloudformation = boto3.resource('cloudformation')
stack = cloudformation.Stack('stack_name')

enable_termination_protection = True

stacks = []
try:
    if (stack.enable_termination_protection == True):
        print(stacks.append(stack))
except ClientError:
    print("enable termination protection", stack_name)