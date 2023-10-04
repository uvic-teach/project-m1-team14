import os
import hashlib
import json
import time
import random
import boto3
from botocore.exceptions import ClientError
from galactis_common import is_valid_username, is_valid_sha256_hash, success, failure, create_token

USER_TABLE = os.environ["USER_TABLE"] 
TOKEN_TABLE = os.environ["TOKEN_TABLE"]


dynamo = boto3.client('dynamodb')

def handler(event, context):
    try:
        if "body" in event and event["body"]:
            print("loading body")
            body = json.loads(event["body"])
            print(f"{body}")

            if "username" in body and "password" in body:
                print(f"username and password in body")
                username = body["username"]
                password = body["password"]
                
                if not is_valid_username(username):
                    return failure("invalid username")
                if not is_valid_sha256_hash(password):
                    return failure("invalid password")

                print(f"username and password were valid")
                m = hashlib.sha256(password.encode())
                hashed = m.hexdigest()
                
                try:
                    dynamo.put_item(
                        TableName=USER_TABLE,
                        Item={
                            "username": {
                                "S": username
                            },
                            "password": {
                                "S": hashed
                            },
                        },
                        ConditionExpression="attribute_not_exists(username)"
                    )
                except ClientError as e:
                    if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                        return failure("account already exists")

                token = create_token(TOKEN_TABLE, dynamo, username)
                print("no exception thrown by put_item, returning success")
                # if no exception was thrown by put_item then
                # it succeeded
                return success(str(token))
    except Exception as e:
        print(e)
        

    return failure()