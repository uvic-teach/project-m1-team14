import re
import json
import random
import time

HEADERS = {
    "Content-Type": "application/json",
}

def is_valid_username(username: str):
    return re.search(r"^\w{3,20}$", username) is not None

def is_valid_sha256_hash(hash: str) -> bool:
   return re.search(r"^[a-fA-F0-9]{64}$", hash) is not None 

def failure(reason: str = ""):
    if len(reason) > 0:
        return {
            "statusCode": 400,
            "headers": HEADERS,
            "body": json.dumps({
                "reason": reason
            })
        }
    return {
        "statusCode": 400,
        "headers": HEADERS,
    }    

def success(token: str = ""):
    if len(token) > 0:
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({
                "token": token
            })
        }    

    return {
        "statusCode": 200,
        "headers": HEADERS
    }

def create_token(table_name: str, client: any, username: str) -> str:
    token = str(random.getrandbits(256))
    expiration = int(time.time()) + 86400
    client.put_item(
        TableName=table_name,
        Item={
            "token": {
                "S": token
            },
            "username": {
                "S": username
            },
            "expires": {
                "N": str(expiration)
            }
        }
    )
    return token