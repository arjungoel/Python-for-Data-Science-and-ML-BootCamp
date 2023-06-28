import json
import boto3
from botocore.exceptions import ClientError

incorrect_tag = ['cost_center', 'cost_Center', 'cost_Centre', 'costcentre', 'costcenter', 'costCentre', 'costCenter']

def lambda_handler(event, context):
    client = boto3.client(service_name='s3')
    response = client.list_buckets()

    # list s3 buckets and the tags associated with the bucket
    for bucket in response['Buckets']:
        try:
            result = client.get_bucket_tagging(
                Bucket=bucket['Name']
                )
            values = result['TagSet']
            for value in values:
                for key, value in value.items():
                    current_value = key, value
                    updated_value = list(current_value)
                    for idx, item in enumerate(updated_value):
                        if 'cost' in item:
                            updated_value[idx] = "cost_centre"
                    #print(updated_value)
                    # new_dict = {value for value in updated_value}
                    # print(type(new_dict))
                    new_dict = {}
                    for index, element in enumerate(updated_value):
                        new_dict[index] = element
                    
                    #print(new_dict)
                    update_tag = client.put_bucket_tagging(
                        Bucket=bucket['Name'],
                        Tagging={
                            'TagSet': [
                                
                                    new_dict
                              
                            ]
                        }
                    )
                    print("succeed!")
                    
               
                
##############################################################################################################       
                # if value['Key'] in incorrect_tag:
                #     key = value['Key']
                #     new_key = value['Key'].replace(key, 'cost_centre')
                #     print(new_key)
                #     update_tag = client.put_bucket_tagging(
                #         Bucket=bucket['Name'],
                #         Tagging={
                #             'TagSet': [
                #                 {
                #                     'Key': new_key,
                #                     'Value': value['Value']
                #                 }
                                
                #             ]
                #         }
                #     )
                #     print("succeed!")
#################################################################################################################
  
                    # updated_value = value.update({"Key": new_key})
                    # print(updated_value)
                    #print(new_key)
                    
                    # update_tag = client.put_bucket_tagging(
                    #     Bucket=bucket['Name'],
                    #     Tagging={
                    #         'TagSet': [
                                
                    #             ]
                    #     }
                    # )
                    
        except ClientError as e:
            if e.response['Error']['Code'] == 'TagSetNotFoundError':
                print("TagSet Not Found Error" + e)
            else:
                print(f"The bucket name is: {bucket['Name']} has no tags")
