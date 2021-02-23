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
    
    body = event['body']
    # we make the body into json pairs here
    body_json = json.loads(body)
    
    # items = (list(body_json.items()))
    
    
    # try ADD rather than SET
    update_exp = 'SET {}'.format(','.join(f'#{key}= :{key}' for key in body_json))
    expression_attribute_values = {f':{key}': val for key, val in body_json.items()}
    expression_attribute_names = {f'#{key}': key for key in body_json}
    
    # update_vals = dict()
    
    # for key,val in body_json.items():
        # update_vals[f":{key}"] = val
 
    update_vals = ddb_json.dumps(expression_attribute_values, as_dict=True)

    # setup time
    date = datetime.now()
    timeStamp = date.strftime("%Y-%m-%d %H:%m:%S")
    
    id = event['pathParameters'].get('Id', None)
    
    # https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_UpdateItem.html
    response = ddb.update_item(
        TableName=os.environ.get('tableName'),
        Key={
            'Id': {'S': id}
        },
        UpdateExpression=update_exp,
        ExpressionAttributeNames=expression_attribute_names,
        ExpressionAttributeValues=update_vals,
        # can print the new values if we want
        ReturnValues="ALL_OLD"
    )

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }