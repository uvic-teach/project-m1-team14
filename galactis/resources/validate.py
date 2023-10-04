import os
import json
import time
import boto3
from galactis_common import is_valid_username, success, failure

USER_TABLE = os.environ["USER_TABLE"] 
TOKEN_TABLE = os.environ["TOKEN_TABLE"]


dynamo = boto3.client('dynamodb')

def handler(event, context):
    print(event)
    try:
        if event and "queryStringParameters" in event:
            print("loading params")
            username = event["queryStringParameters"]["username"]
            token = event["queryStringParameters"]["token"]
            if not is_valid_username(username):
                return failure()

            print(f"username is valid")
            current_time = int(time.time())
            resp = dynamo.get_item(
                TableName=TOKEN_TABLE,
                Key={
                    "token": {
                        "S": str(token)
                    }
                }
            )
            item = resp["Item"]
            print(item)
            if current_time < int(item["expires"]["N"]) and username == item["username"]["S"]:
                # if no exception was thrown by put_item then
                # it succeeded
                return success()
    except Exception as e:
        print(e)
        

    return failure()