import json
import boto3
import os

from botocore.exceptions import ClientError
from dynamodb_json import json_util as ddb_json

#--------------------------------------------------------------------------

ddb = boto3.client('dynamodb')

def lambda_handler(event, context):
    """
    """
    # debugging
    print("Event: ", event)
    print("Context: ", context)
    
    id = event['pathParameters'].get('Id', None)
    
    try:
        # create response
        response = ddb.delete_item(
            # get tableName from environment vars
            TableName=os.environ.get('tableName'),
            # key we want to delete will be id of event passed in
            Key={
                'Id': {'S': id}
            }
        )
        # print response
        print("Response ", response)
    # if exception, print
    except ClientError as exception:
        print(exception.response)
    # if successful, return 204 and Null body
    else:
        return {
            'statusCode': 204,
            'body': None,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            }
        }