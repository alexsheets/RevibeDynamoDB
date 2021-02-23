import boto3
import json
import os

from dynamodb_json import json_util as ddb_json


ddb = boto3.client('dynamodb')


def lambda_handler(event, context):
    """
    """
    
    print("Event: ", event)
    print("Context: ", context)
    
    # Need an environment variable 'tableName' for the name of the DynamoDB table
    response = ddb.scan(
        TableName=os.environ.get('tableName'),
        ProjectionExpression='Id,Bio,#name',
        ExpressionAttributeNames={'#name': 'Name'}
    )
    
    print("Response: ", response)
    
    items_raw = response['Items']
    items = ddb_json.loads(items_raw)
    
    return {
        'statusCode': 200,
        'body': json.dumps(items),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        }
    }


