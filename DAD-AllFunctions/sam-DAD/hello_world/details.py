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
    # error handling if it's None...
    
    
    try:
        # create response
        response = ddb.get_item(
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
    # if successful, return 200 w/ item
    else:
        item_raw = response['Item']
        item = ddb_json.loads(item_raw)
        return {
            'statusCode': 200,
            'body': json.dumps(item),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
            }
        }