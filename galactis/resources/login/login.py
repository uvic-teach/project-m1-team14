import os
import json
import hashlib
import re
import time
import random
import base64


import boto3

USER_TABLE = os.environ["USER_TABLE"] 
TOKEN_TABLE = os.environ["TOKEN_TABLE"]

HEADERS = {
    "Content-Type": "application/json",
}

dynamo = boto3.client('dynamodb')

def is_valid_sha256_hash(hash: str) -> bool:
   return re.search(r"^[a-fA-F0-9]{64}$", hash) is not None 

def failure():
    return {
        "statusCode": 400,
        "headers": HEADERS,
    }    

def success(token: str):
    return {
        "statusCode": 200,
        "headers": HEADERS,
        "body": json.dumps({
            "reason": token
        })
    }    

def handler(event, context):
    try:
        if "body" in event and event["body"]:
            body = json.loads(event["body"])

            if "username" in body and "password" in body:
                username = body["username"]
                password = body["password"]
                if is_valid_sha256_hash(password):
                    data = dynamo.get_item(
                        TableName=USER_TABLE,
                        Key={
                            "username": {
                                "S": username
                            }
                        }
                    )
                    if data and "Item" in data and "username" in data["Item"]:
                        # item exists
                        existing_password = data["Item"]["password"]["S"]
                        m = hashlib.sha256(password.encode())
                        hashed = m.hexdigest()
                        if hashed == existing_password:
                            # passwords match, create a new token
                            token = random.getrandombits(256)
                            expiration = int(time.time()) + 86400
                            res = dynamo.put_item(
                                TableName=TOKEN_TABLE,
                                Item={
                                    "token": {
                                        "S": token
                                    },
                                    "expires": {
                                        "N": expiration
                                    }
                                }
                            )
                            return success(base64.b64encode(token))
    except Exception as e:
        print(e)
        

    return failure()