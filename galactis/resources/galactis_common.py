import re
import json
import random
import time

HEADERS = {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
}

def is_valid_username(username: str):
    return re.search(r"^\w{3,20}$", username) is not None


def is_valid_password(password: str): 
    # minimum 8 characters, at least one number, one special character, and one letter
    # stolen from https://stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
    return re.search(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password)

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

def success(token: str = "", expiration: int = 0):
    if len(token) > 0:
        return {
            "statusCode": 200,
            "headers": HEADERS,
            "body": json.dumps({
                "token": token,
                "expiration": expiration,
            })
        }    

    return {
        "statusCode": 200,
        "headers": HEADERS
    }

def create_token(table_name: str, client: any, username: str) -> tuple:
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
    return (token, expiration)