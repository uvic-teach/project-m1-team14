import requests
from random import randint
from os import environ
from datetime import timedelta
from redis import Redis
from rq import Queue

VALIDATE_URL = "https://fr1gi6xdtc.execute-api.us-west-2.amazonaws.com/prod/validate"

def handle_register(username: str, email: str, token: str) -> bool:
    if validate_request(username, token):
        next_availability = check_availability()
        schedule_notify(email, next_availability)
        return True
    else:
        return False

def validate_request(username: str, token: str) -> bool:
    api_key = environ.get("API_KEY")
    response = requests.get(VALIDATE_URL, params={"username": username, "token": token}, headers={"X-Api-Key": api_key})
    return response.status_code == 200

def check_availability() -> int:
    return randint(30, 180)

def schedule_notify(email: str, notify_seconds: int):
    queue = Queue(connection=Redis(host="cache"))
    queue.enqueue_in(timedelta(seconds=notify_seconds), func=notify, args=(email,))

def notify(email: str):
    print(f"emailing {email}")
