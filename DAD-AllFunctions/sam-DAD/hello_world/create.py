import json
import boto3
import os
from datetime import datetime
import uuid

from dynamodb_json import json_util as ddb_json

#--------------------------------------------------------------------------

ddb = boto3.client('dynamodb')

def lambda_handler(event, context):
    """
    """
    # debugging
    print("Event: ", event)
    print("Context: ", context)
    
    # have to return a status code
    if 'body' not in event:
        return {
            'statusCode': 500
        }
    
    body_json = event['body']
    body = json.loads(body_json)

    # setup time
    date = datetime.now()
    timeStamp = date.strftime("%Y-%m-%d %H:%m:%S")
    
    artist = body
    artist['Id'] = str(uuid.uuid4())
    artist['CreatedAt'] = timeStamp
    artist['UpdatedAt'] = timeStamp
    artist['Name']: body['Name']
    artist['Description']: body['Description']
    
    # item = {
    #     'Id': {'S': f"{uuid.uuid4()}"},
    #     'Name': {'S': body['Name']},
    #     'Bio': {'S': body['Bio']},
    #     'CreatedAt': {'S': timeStamp},
    #     'UpdatedAt': {'S': timeStamp},
    # }
    
    # convert our artist to an item using DynamoDB json
    item = ddb_json.dumps(artist, as_dict=True)
    
    response = ddb.put_item(
        TableName=os.environ.get('tableName'),
        Item=item
    )
    print("Response: ", response)

    return {
        'statusCode': 201,
        'body': json.dumps(artist),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        }
    }