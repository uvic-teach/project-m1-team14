import os
import hashlib
import json
import time
import random
import boto3
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
                if is_valid_username(username) and is_valid_sha256_hash(password):
                    print(f"username and password were valid")
                    data = dynamo.get_item(
                        TableName=USER_TABLE,
                        Key={
                            "username": {
                                "S": username
                            }
                        }
                    )
                    print(f"made call to db")
                    if data and "Item" in data and "username" in data["Item"]:
                        print(f"item exists already in db")
                        # item exists
                        existing_password = data["Item"]["password"]["S"]
                        m = hashlib.sha256(password.encode())
                        hashed = m.hexdigest()
                        if hashed == existing_password:
                            print(f"hashed password is equal to existing password")
                            # passwords match, create a new token
                            token, expiration = create_token(TOKEN_TABLE, dynamo, username)
                            print("no exception thrown by put_item, returning success")
                            # if no exception was thrown by put_item then
                            # it succeeded
                            return success(str(token), expiration)
    except Exception as e:
        print(e)
        

    return failure()